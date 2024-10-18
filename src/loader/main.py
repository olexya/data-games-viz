from python_on_whales import docker
import time
import requests
import os
import json
import dotenv

dotenv.load_dotenv()

# Attend que kestra soit en ligne
# Max 10 essais avec 1 seconde d'intervale entre chaque
i = 0
while not sum([container.name == "kestra" for container in docker.ps()]):
    i += 1
    if i % 10 == 0:
        exit(1)
    time.sleep(1)

# Permet de supprimer une liste de flow
def delete_flow(host: str, flows: str):
    response = requests.delete(
        f"http://{host}:8080/api/v1/flows/delete/by-ids",
        headers={
            "Content-Type": "application/json"
        },
        data=json.dumps(flows)
    )
    return response

# Permet de lister les flows
def list_flow(host: str, namespace: str) -> None:
    response = requests.get(
        f"http://{host}:8080/api/v1/flows/{namespace}"
    )
    return response

# Créer un flow
def send_flow(host: str, file_name: str):
    with open(file_name, "rb") as file:
        response = requests.post(
            f"http://{host}:8080/api/v1/flows/import",
            files={
                "fileUpload": (f"{file_name}", file.read(), "application/x-yaml"),
            },
        )
    return response

# Envoyer un fichier dans un espace de travail
def send_file(host: str, file_name: str, namespace: str, uri):
    with open(file_name, "rb") as file:
        response = requests.post(
            f"http://{host}:8080/api/v1/namespaces/{namespace}/files",
            files={
                "fileContent": (f"{file_name}", file.read(), "application/x-yaml"),
            },
            params={
                "path": uri
            }
        )
    return response

# Créer un dossier dans un espace de travail
def send_directory(host: str, namespace: str, uri):
    response = requests.post(
        f"http://{host}:8080/api/v1/namespaces/{namespace}/files/directory",
        params={
            "path": uri
        }
    )
    return response

# Exclut les fichiers inutiles
def check_type(filename):
    for extention in [".sql", ".yml", ".txt", ".py"]:
        if filename.endswith(extention):
            return True
    return False

# Upload directory et son contenu dans kestra
def upload_directory(host: str, directory_name: str, namespace: str):
    length = len(directory_name) + 1
    for root, directories, files in os.walk(directory_name):
        for filename in files:
            if check_type(filename):
                path = f"{root}/{filename}"
                send_file(host, path, namespace, path[length:])
        for directory in directories:
            path = f"{root}/{directory}"
            send_directory(host, namespace, path[length:])

# Démarre une taches
def start_task(host: str, namespace: str, task_name: str) -> None:
    requests.post(
        f"http://{host}:8080/api/v1/executions/{namespace}/{task_name}",
        params = {
            "wait": True
        }
    )

# Host pour démarrer en local
# host = "localhost"

# Host pour démarrer depuis le docker kestra
host = os.getenv("HOST")

namespace = os.getenv("KESTRA_NAMESPACE")

# Setup workspace

## Supprime tout les flows créé lors du premier lancement de kestra
response = list_flow(host, "tutorial")
list_flow = []
for flow in response.json():
    list_flow.append({
        "namespace": flow.get("namespace"),
        "id": flow.get("id"),
    })
response = delete_flow(host, list_flow)

## Envoie le flow
response = send_flow(host, "/home/src/loader/kestra/kestra.yaml")

## Var env
send_file(host, "/home/src/loader/.env", namespace, "./.env")

## Envoie les fichiers de configuration des outils manager par kestra
upload_directory(host, "/home/src/get-data", namespace)
upload_directory(host, "/home/src/dbt", namespace)

## Démarrer le flow
start_task(host, namespace, "get-data")

## Affiche la fin du script
print("End")
