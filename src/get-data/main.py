import src.init
import pandas
import sqlalchemy
import alive_progress
import requests
import argparse
import time
import dotenv
import os

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--app", type=int)
args = parser.parse_args()

dotenv.load_dotenv()

engine = sqlalchemy.create_engine(f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('POSTGRES_DB')}")
with engine.connect() as connection:
    connection.execute(sqlalchemy.text(f"CREATE SCHEMA IF NOT EXISTS {os.getenv('SCHEMA')}"))
    connection.commit()
    src.init.create(engine)

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

def valid_response(response):
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Erreur lors de la requête GET:", response)

def get_game_list():
    data = valid_response(requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2"))
    return pandas.DataFrame(data["applist"]["apps"])

def get_game_info(app_id):
    params = { "appids": app_id }
    data = valid_response(requests.get("https://store.steampowered.com/api/appdetails", params))
    return data[str(app_id)]

def to_sql(info, meta):
    if len(info):
        data = pandas.DataFrame(info)
        data.to_sql("games_info", engine, schema=os.getenv("SCHEMA"), if_exists='append', index=False)
    if len(meta):
        data = pandas.DataFrame(meta)
        data.to_sql("games_metadata", engine, schema=os.getenv("SCHEMA"), if_exists='append', index=False)

def info_game():
    games_df = get_game_list()

    all_game_info = []
    all_metadata = []
    for index, row in alive_progress.alive_it(enumerate(games_df.values)):
        game_info = get_game_info(row[0])
        data = flatten(row[0], game_info)
        if data[0]["ss"] == "False":
            all_game_info.append({
                "success": False,
                "steam_appid": row[0]
            })
        else:
            del data[0]["ss"]
            data[0]["success"] = True
            all_game_info.append(data[0])
            all_metadata.extend(data[1])
        if (index + 1) % 100 == 0:
            to_sql(all_game_info, all_metadata)
            all_game_info = []
            all_metadata = []

        if args.app == -1:
            time.sleep(1.3)

        if index > args.app:
            break
    to_sql(all_game_info, all_metadata)

if __name__ == "__main__":
    info_game()
