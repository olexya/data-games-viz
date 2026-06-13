import time
import sys
import requests
import os
import json
import dotenv
from datetime import datetime, timezone

dotenv.load_dotenv()

# Hôte de l'API Kestra. Par défaut le nom de service compose `kestra`
# (réseau interne) : fonctionne sur Mac / Windows / Linux sans host.docker.internal.
host = os.getenv("KESTRA_HOST", "kestra")
namespace = os.getenv("KESTRA_NAMESPACE")

# Kestra 1.x : l'API est versionnée par tenant (`main` par défaut en OSS) et
# protégée par Basic Auth (toujours requise depuis 1.x).
tenant = os.getenv("KESTRA_TENANT", "main")
auth = None
_user = os.getenv("KESTRA_BASIC_AUTH_USERNAME")
_password = os.getenv("KESTRA_BASIC_AUTH_PASSWORD")
if _user and _password:
    auth = (_user, _password)

# Session HTTP partagée (auth appliquée à toutes les requêtes).
session = requests.Session()
if auth:
    session.auth = auth

# Base d'API tenant-aware : http://host:8080/api/v1[/<tenant>]
_tenant_segment = f"/{tenant}" if tenant else ""
API = f"http://{host}:8080/api/v1{_tenant_segment}"


# Attend que l'API Kestra soit réellement prête (pas seulement le conteneur démarré).
# Poll HTTP avec backoff jusqu'à un timeout généreux.
def wait_for_kestra(timeout: int = 300):
    deadline = time.time() + timeout
    url = f"{API}/flows/{namespace}"
    last = None
    while time.time() < deadline:
        try:
            response = session.get(url, timeout=5)
            # 200/404 = API prête et auth OK ; 401 = pas encore initialisée / mauvais creds.
            if response.status_code in (200, 404):
                print(f"Kestra API prête (status {response.status_code}).")
                return
            last = f"status {response.status_code}"
        except requests.RequestException as exc:
            last = str(exc)
        time.sleep(3)
    raise SystemExit(f"Kestra API indisponible/non authentifiée après {timeout}s ({last}).")


# Permet de supprimer une liste de flow
def delete_flow(flows):
    return session.delete(
        f"{API}/flows/delete/by-ids",
        headers={"Content-Type": "application/json"},
        data=json.dumps(flows),
    )

# Permet de lister les flows d'un namespace
def list_flow(ns: str):
    return session.get(f"{API}/flows/{ns}")

# Créer/importer un flow
def send_flow(file_name: str):
    with open(file_name, "rb") as file:
        return session.post(
            f"{API}/flows/import",
            files={"fileUpload": (file_name, file.read(), "application/x-yaml")},
        )

# Envoyer un fichier dans un espace de travail (namespace files)
def send_file(file_name: str, ns: str, uri):
    with open(file_name, "rb") as file:
        return session.post(
            f"{API}/namespaces/{ns}/files",
            files={"fileContent": (file_name, file.read(), "application/x-yaml")},
            params={"path": uri},
        )

# Créer un dossier dans un espace de travail
def send_directory(ns: str, uri):
    return session.post(
        f"{API}/namespaces/{ns}/files/directory",
        params={"path": uri},
    )

# Exclut les fichiers inutiles
def check_type(filename):
    for extention in [".sql", ".yml", ".txt", ".py"]:
        if filename.endswith(extention):
            return True
    return False

# Upload directory et son contenu dans kestra
def upload_directory(directory_name: str, ns: str):
    length = len(directory_name) + 1
    for root, directories, files in os.walk(directory_name):
        for filename in files:
            if check_type(filename):
                path = f"{root}/{filename}"
                send_file(path, ns, path[length:])
        for directory in directories:
            path = f"{root}/{directory}"
            send_directory(ns, path[length:])

# Démarre une exécution de flow (inputs optionnels via multipart form-data)
def start_task(ns: str, task_name: str, inputs: dict = None) -> None:
    files = {key: (None, str(value)) for key, value in (inputs or {}).items()}
    session.post(
        f"{API}/executions/{ns}/{task_name}",
        params={"wait": True},
        files=files or None,
    )


# Âge (en heures) de la dernière exécution RÉUSSIE de get-data, ou None si aucune.
def last_success_age_hours(ns: str):
    try:
        response = session.get(
            f"{API}/executions/search",
            params={"namespace": ns, "size": 20, "sort": "state.startDate:desc"},
            timeout=10,
        )
        for execution in (response.json().get("results") or []):
            if execution.get("state", {}).get("current") == "SUCCESS":
                start = execution["state"]["startDate"].replace("Z", "+00:00")
                delta = datetime.now(timezone.utc) - datetime.fromisoformat(start)
                return delta.total_seconds() / 3600
    except (requests.RequestException, ValueError, KeyError):
        return None
    return None


# Attend la disponibilité (et l'authentification) de l'API avant toute opération.
wait_for_kestra()

# Données déjà fraîches ? On évite de re-télécharger Steam + reconstruire dbt
# inutilement à chaque `docker compose up` (le loader est un job one-shot relancé).
# Surcharge : FORCE_RELOAD=true pour forcer, RELOAD_MAX_AGE_HOURS pour le seuil.
force_reload = os.getenv("FORCE_RELOAD", "").lower() in ("1", "true", "yes")
max_age_hours = float(os.getenv("RELOAD_MAX_AGE_HOURS", "24"))
if not force_reload:
    age = last_success_age_hours(namespace)
    if age is not None and age < max_age_hours:
        print(f"Données déjà chargées il y a {age:.1f}h (< {max_age_hours}h) ; "
              "rechargement ignoré (FORCE_RELOAD=true pour forcer).")
        sys.exit(0)

# Setup workspace

## Supprime les flows de démo créés au premier lancement de kestra (namespace tutorial)
response = list_flow("tutorial")
flows_to_delete = []
try:
    for flow in response.json():
        flows_to_delete.append({
            "namespace": flow.get("namespace"),
            "id": flow.get("id"),
        })
except (ValueError, TypeError):
    flows_to_delete = []
if flows_to_delete:
    delete_flow(flows_to_delete)

## Envoie le flow
send_flow("/home/src/loader/kestra/kestra.yaml")

## Var env
send_file("/home/src/loader/.env", namespace, "./.env")

## Envoie les fichiers de configuration des outils manager par kestra
upload_directory("/home/src/get-data", namespace)
upload_directory("/home/src/dbt", namespace)

## Démarrer le flow (NUMBER_APP optionnel pour un run rapide ; défaut = défaut du flow)
inputs = {}
number_app = os.getenv("NUMBER_APP")
if number_app:
    inputs["number_app"] = number_app
start_task(namespace, "get-data", inputs)

## Affiche la fin du script
print("End")
