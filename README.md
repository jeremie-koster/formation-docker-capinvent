# TP 2 : Docker-compose 

## Objectif

Le bit de ce TP est d'éxécuter plusieurs images Docker interdépendantes entre elles :
- une API qui s'occupera du training de notre modèle. 
- une image hébergeant un serveur mlflow. Ce serveur loguera les paramètres de notre entrainements ainsi que notre modèle. Il est important de noter que le train ici sera fake --> on se contentera de load le modèle et directement le save dans mlflow.
- une image contenant un bucket s3 qui servira au serveur mlflow afin de loger les artifacts (VOUS NE FEREZ RIEN LA DESSUS? CE SERA DEJA FAIT)
- une image contenant une base sql quis ert aussi au serveur mlflow (VOUS NE FEREZ RIEN LA DESSUS? CE SERA DEJA FAIT)
- une API qui servira à exposer notre modèle : elle récupèrera le modèle sur le serveur mlflow et fera nos precitions.


## Instructions

### Training_api

Nous allons faire cela en 2 temps, la première étape est d'entrainer le modèle et s'assurer que tout est bien log dans mlflow. Pour cela nous allons nous servir de Docker-compose. Veuillez suivre les instructions ci-dessous :

1. Construire le Dockerfile de la training_api
2. Compléter le file docker-compose-training.yaml
    - ne pas toucher aux services db et s3.
    - compléter le network pour le service mlflow et traing_api.
    - compléter les ports pour mlflow et training-api.
    - compléter le param "depends_on" pour mlflow et training_api.
    - compléter les commandes pour training_api.
3. run 
    `
    docker compose -f docker-compose-training.yaml --env-file ./.env up --build --no-deps
    `
4. tester l'url http://0.0.0.0:8000. Pour lancer le "fake train", il suffit d'appeler http://0.0.0.0:8000/train.
5. Check qu'un run mlflow s'est bien sauvegardé dans le bucket local (buckets).
6. Aller sur l'url de mlflow et setup manuellement un de vos modèle en stage "Production".


### Serving_api

Nous allons maintenant nous occuper de l'api qui va effectuer les prédictions.

1. Construire le Dockerfile de la serving_api
2. Compléter le file docker-compose-predict.yaml
    - ne pas toucher aux services db et s3.
    - compléter le network pour le service mlflow et traing_api et serving_api.
    - compléter les ports pour mlflow et training-api et serving_api.
    - compléter le param "depends_on" pour mlflow et training_api et predict_api.
    - compléter le volume pour le serving_api.
3. run 
    `
    docker compose -f docker-compose-predict.yaml --env-file ./.env up --build --no-deps
    `
4. tester l'url http://0.0.0.0:8001. Pour tester la prediciton, il suffit d'appeler http://0.0.0.0:8001/prediction de la manière suivante :

```
python
import requests
res = requests.post("http://0.0.0.0:8001/prediction", json={"name": "pandas.png"})
res.json()
```
5. Expérez et priez que ça marche, sinon débrouillez vous.

6. Une fois le tout terminé : 

    `
    docker container stop $(docker container ls -aq) && docker system prune -af --volumes
    `
