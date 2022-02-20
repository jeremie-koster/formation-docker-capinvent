# TP 1

## But du TP 

Exécuter une image Docker qui expose une API. Cette API retourne le résultat d'une classification faite sur une image passé en input.

Remarque : il suffit de donner le nom de l'image en input du call API car l'on spécifiera un volume sur lequel l'API pourra aller chercher l'image en question.

![Alt text](./assets/schema_tp1_docker.png?raw=true "schema TP1")


## Instruction
1. Construire le Dockerfile en partant d'une image contenant tensorflow 2.3.0 (FROM tensorflow/tensorflow:2.3.0)
2. Installer les requirements
3. Copier le code source depuis l’environnement local vers le conteneur.
4. Setup la command qui sera exécutée lors de l’exécution du conteneur : https://fastapi.tiangolo.com/tutorial/first-steps/ 
5. Build l’image, ne pas oublier de nommer notre image : https://docs.docker.com/engine/reference/commandline/build/
6. Run l’image avec les bon paramètres, ne pas oublier de mapper les ports et les volumes : https://docs.docker.com/engine/reference/commandline/run/
7. Tester l’api avec les commandes suivantes :

```
python 
import request
requests.post('http://0.0.0.0:<exposed_port>/prediction',json={'name':'<image_name>’})
```

8. Once you are done, you can stop and delete all your containers with : 
    `
    docker container stop $(docker container ls -aq) && docker system prune -af --volumes
    `
