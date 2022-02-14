# But du TP 

Déployer une image Docker qui expose une API. Cette API retourne une prédiction faite sur un nom d'image passé en input.


Instruction
1. Construire le Dockerfile depuis une image content tensorflow 2.3.0 (FROM ): 
2. Installer les requirements
3. Copier le code source depuis l’environnement local vers le conteneur.
4. Setup la command qui sera exécutée lors de l’exécution du conteneur.
5. Build l’image (ne pas oublier d’utiliser le paramètre –t pour nommer notre image)
6. Run l’image avec les bon paramètres (indice –p pour exposer le port, -v pour faire le mapping du volume)
7. Tester l’api avec les commandes suivantes :
>>> python 
>>> import request
>>> requests.post('http://0.0.0.0:8000/prediction',json={'name':'tailed_frog.jpeg’})
