# TP 1

## But du TP 

Le but du TP est de mettre en pratique les notions acquises lors de la formation Docker.

Le TP consiste à :

- construire le Dockerfile d'une application d'inférence de ML basique
- de builder et run le conteneur en appliquant le mapping de port et le montage d'un volume
- de tester le bon fonctionnement du conteneur.

L'application expose une API (FastAPI) qui effectue de la classification d'objets à partir d'une image.

Les images utilisées pour tester l'API sont dans le dossier `examples/`. Ce dossier devra être monté comme volume dans le conteneur de façon à ce que l'API puisse y accéder.

**Remarque** : lors du test de l'API, il suffira de donner le nom de l'image située dans le dossier du volume monté (`examples/` par défaut) en input de l'appel API. L'API va chercher l'image dans le chemin monté dans le conteneur défini par la variable d'environnement `DOCKER_VOLUME_PATH`.

![Alt text](./assets/schema_tp1_docker.png?raw=true "schema TP1")


## Instructions

1. Construire le Dockerfile en partant d'une image de base python 3.12 (FROM --platform=linux/arm64 python:3.12). Il faudra :
    
- Installer les requirements
- Copier le code source depuis l’environnement local vers le conteneur
- Exposer le bon port
- Setup la command qui sera exécutée lors de l’exécution du conteneur : `uvicorn app.main:app --host 0.0.0.0 --port 8000`

2. Build l’image, ne pas oublier de nommer notre image : https://docs.docker.com/engine/reference/commandline/build/.
    

3. Run l’image avec les bon paramètres, ne pas oublier de mapper les ports et les volumes : https://docs.docker.com/engine/reference/commandline/run/


4. Tester l’api avec les commandes suivantes :

```
python 
import requests
res = requests.post('http://0.0.0.0:8001/prediction',json={'name':'<image_name>’})
res.json()
```
Ou bien (plus simple) en vous rendant sur le endpoint de la doc Swagger `http://0.0.0.0:8001/docs`

8. Une fois terminé, vous pouvez arrêter et supprimer le conteneur, les images et les volumes non utilisés : 

```
docker container stop $(docker container ls -aq) && docker system prune -af --volumes
```

### Bonus

L'API va chercher l'image (dont le nom est fourni lors de l'appel API) dans le chemin de montage du volume dans le conteneur défini par la variable d'environnement `DOCKER_VOLUME_PATH`. Par défaut, la valeur attribuée est `/examples`.

Le bonus du TP consiste à monter le dossier des images à un autre emplacement dans le conteneur et à modifier la variable d'environnement `DOCKER_VOLUME_PATH` dans le Dockerfile.
