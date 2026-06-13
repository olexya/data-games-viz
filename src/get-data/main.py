import src.init
import pandas
import sqlalchemy
import alive_progress
import requests
import argparse
import time
import dotenv
import os
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--app", type=int)
args = parser.parse_args()

dotenv.load_dotenv()

engine = sqlalchemy.create_engine(f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('POSTGRES_DB')}")
schema = os.getenv("SCHEMA")
with engine.connect() as connection:
    connection.execute(sqlalchemy.text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
    connection.commit()
    src.init.create(engine)
    # Idempotence : repartir d'un état propre à chaque exécution.
    # games_info.steam_appid étant clé primaire, un append en relance lèverait
    # une IntegrityError ; on tronque donc les deux tables avant de recharger.
    connection.execute(sqlalchemy.text(
        f"TRUNCATE TABLE {schema}.games_info, {schema}.games_metadata RESTART IDENTITY"
    ))
    connection.commit()


def table_columns(table):
    # Colonnes réellement définies dans la table (schéma fixe de src.init).
    with engine.connect() as conn:
        rows = conn.execute(sqlalchemy.text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema = :s AND table_name = :t"
        ), {"s": schema, "t": table}).fetchall()
    return {row[0] for row in rows}


# L'API Steam renvoie des champs variables selon les jeux (ex. abonnements :
# price_overview_recurring_sub). On restreint donc l'insertion aux colonnes connues
# de la table : les champs supplémentaires sont ignorés (sinon to_sql lèverait
# « column ... does not exist »).
GAMES_INFO_COLUMNS = table_columns("games_info")
GAMES_METADATA_COLUMNS = table_columns("games_metadata")

def to_meta(id, data):
    meta = []
    for elt in data.items():
        meta.append({
            "id": id,
            "name": elt[0],
            "value": elt[1]
        })
    return meta

def flatten(id, data, name = "") -> dict:
    out = {}
    meta = []

    if type(data) is dict:
        for item in data:
            result = flatten(id, data[item], name + item + '_')
            if item == "ratings":
                out.update({item: "In metadata table"})
                meta.extend(to_meta(id, result[0]))
            else:
                out.update(result[0])
            meta.extend(result[1])
    elif type(data) is list:
        for i, item in enumerate(data):
            result = flatten(id, item, name + str(i) + '_')
            out.update({name[5:-1]: "In metadata table"})
            meta.extend(to_meta(id, result[0]))
            # meta.update(result[1]) # Non vérifié
    elif type(data) == str:
        out[name[5:-1]] = data.replace("\r\n", "\\r\\n")
    else:
        out[name[5:-1]] = str(data)
    return out, meta

STEAM_APPLIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
STEAM_APPDETAILS_URL = "https://store.steampowered.com/api/appdetails"

# Liste de repli : si l'endpoint GetAppList est indisponible (Steam le retire/altère
# régulièrement), on retombe sur un catalogue connu d'app IDs populaires. L'ingestion
# reste fonctionnelle et déterministe (utilise l'endpoint appdetails, lui stable).
FALLBACK_APP_IDS = [
    10, 20, 30, 40, 50, 60, 70, 80, 130, 220, 240, 280, 300, 320, 340, 360,
    380, 400, 420, 440, 500, 550, 570, 620, 630, 730, 1840, 2000, 2100, 2200,
    2280, 2300, 2400, 2500, 2600, 2620, 2630, 2640, 2700, 3590, 4000, 4700,
    8190, 8500, 8930, 9900, 10090, 10180, 12100, 12110, 12120, 12200, 12210,
    17390, 17460, 17470, 22300, 22320, 22330, 22350, 22370, 22380, 22600,
    33930, 35140, 38600, 39140, 47780, 49520, 55230, 200510, 218620, 221100,
    227300, 230410, 236850, 251570, 252490, 271590, 292030, 304930, 359550,
    367520, 377160, 413150, 431960, 444090, 489830, 578080, 582010, 588650,
    620980, 632360, 646570, 739630, 813780, 945360, 1085660, 1091500, 1172470,
    1245620, 1326470, 1551360, 1599340, 1817070, 1938090, 2050650,
]


def valid_response(response):
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Réponse HTTP {response.status_code} pour {response.url}")

def get_game_list():
    # Tente l'endpoint officiel ; bascule sur la liste de repli en cas d'échec.
    try:
        data = valid_response(requests.get(STEAM_APPLIST_URL, timeout=30))
        df = pandas.DataFrame(data["applist"]["apps"])
        if len(df):
            return df
        print("GetAppList a renvoyé une liste vide ; bascule sur la liste de repli.")
    except Exception as exc:  # noqa: BLE001
        print(f"GetAppList indisponible ({exc}) ; bascule sur la liste de repli.")
    return pandas.DataFrame({"appid": FALLBACK_APP_IDS})

def get_game_info(app_id, retries=3):
    # Renvoie le bloc d'info pour app_id, ou None si l'API échoue (app ignorée).
    # Gère le rate-limit Steam (429) avec un backoff progressif.
    for attempt in range(retries):
        try:
            response = requests.get(STEAM_APPDETAILS_URL, params={"appids": app_id}, timeout=30)
            if response.status_code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            if response.status_code != 200:
                return None
            return response.json().get(str(app_id))
        except (requests.RequestException, ValueError):
            return None
    return None

def to_sql(info, meta):
    if len(info):
        data = pandas.DataFrame(info)
        # Ne garder que les colonnes connues de la table (ignore les champs Steam variables).
        data = data[[c for c in data.columns if c in GAMES_INFO_COLUMNS]]
        data.to_sql("games_info", engine, schema=schema, if_exists='append', index=False)
    if len(meta):
        data = pandas.DataFrame(meta)
        data = data[[c for c in data.columns if c in GAMES_METADATA_COLUMNS]]
        data.to_sql("games_metadata", engine, schema=schema, if_exists='append', index=False)

def info_game():
    games_df = get_game_list()
    # int() : éviter numpy.int64 (non adaptable par psycopg2) pour les jeux
    # renvoyant success=False où steam_appid provient de cette liste.
    appids = [int(row[0]) for row in games_df.values]

    # args.app : -1 = tout le catalogue, sinon les N+1 premières apps.
    if args.app is not None and args.app >= 0:
        appids = appids[: args.app + 1]

    # Le goulot d'étranglement est la latence HTTP (1 requête/app, pas de bulk Steam).
    # On parallélise les appels (avec backoff 429) : ~6x plus rapide qu'en séquentiel.
    workers = max(1, int(os.getenv("STEAM_WORKERS", "8")))

    all_game_info = []
    all_metadata = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = zip(appids, executor.map(get_game_info, appids))
        for count, (app_id, game_info) in enumerate(
            alive_progress.alive_it(results, total=len(appids))
        ):
            if game_info is None:
                # API indisponible pour cette app : on l'ignore sans casser le run.
                continue
            data = flatten(app_id, game_info)
            if data[0]["ss"] == "False":
                all_game_info.append({
                    "success": False,
                    "steam_appid": app_id
                })
            else:
                del data[0]["ss"]
                data[0]["success"] = True
                all_game_info.append(data[0])
                all_metadata.extend(data[1])
            # Insertion par lots pour borner la mémoire sur de gros catalogues.
            if (count + 1) % 100 == 0:
                to_sql(all_game_info, all_metadata)
                all_game_info = []
                all_metadata = []
    to_sql(all_game_info, all_metadata)

if __name__ == "__main__":
    info_game()
