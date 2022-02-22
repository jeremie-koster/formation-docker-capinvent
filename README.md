# TP 3 : Docker run as root

Le but de ce Tp est de démontrer que run une image Docker as root peut être problématique. Nous allons ouvrir un terminal en mode
root, attention à ne pas faire n'importe quoi (pas de rm -rf ;) ).
## Instructions

### 1 Création du fichier secret avec root usr.

1. Nous allons créer un fichier secret.txt à l'emplacement /Users/ (que l'on supprimera a la find e ce TP). Ce folder est noramlement en read_only, donc on
    ne peut pas écrire dessus avec notre usr actuel. Essayez les commandes ci dessous, vous devriez avoir "Permission denied"

    ```
    cd /Users/
    echo "top secret stuff" >> ./secrets.txt 
    ```

    Pour créer ce fichier nous allons donc passer en mode root avec la commande "sudo -s":

    ```
    sudo -s
    cd /Users/
    echo "top secret stuff" >> ./secrets.txt 
    chmod 0600 secrets.txt
    exit 
    ```

    la commande "chmod 0600" permet de restreindre les droits d 'accès au fichier au root seulement.

2. Essayez de lire le fichier avec votre usr : 

    `
    cat secrets.txt 
    `

    Vous devriez avoir "Permission denied", et ceci est normal.


### Essayons avec Docker...

1. Build l'image et run l'image :
    `
    docker run -v /:/hostOS -it --rm docker_tp3
    `
2. run dans le shell
    `
    whoami
    `
3. Essayez d'afficher le contenu avec la commande cat. Le contenu est il affiché ?? Vous pouvez potentiellement voir "Operation denied", ce message est du à une sécurité supplémentaire sur mac qu'il faut accorder au niveau application: le point important est que l'erreur n'est plus la même --> on n'a plus l'erreur "Permission denied"


### Bonne pratique, run docker image depuis un usr.

Il existe deux solutions pour cela : 
1. En utilisnt le paramètre --user depuis la commande run : : --user <uid>
    pour trouver votre uid, il suffit de tapper id dans votre temrinal. ex : 

    ```
    lmichelis@MacBookPro-lmichelis-FVFXX1F4HV29 /Users % id
    uid=501(lmichelis)
    ```

2. En définissant les utilisateur de l'app direcetmeent dans le dockerfile 
    ```
    RUN groupadd -g 999 appuser && \
        useradd -r -u 999 -g appuser appuser
    USER appuser
    ```

### Supprimer le fichier secrets.txt

```
sudo -s 
cd /Users/
rm secrets.txt 
exit
```




