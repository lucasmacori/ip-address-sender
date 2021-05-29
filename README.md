# ip-address-sender
Un script Python envoyant un mail et mettant à jour la configuration d'un site Wordpress lorsque l'adresse IP du FAI change

# Installation
## Pré-requis
Python 3.X ou supérieur
Il est nécéssaire d'installer les paquets suivants sur le serveur avant de pouvoir utiliser le script
Connecteur MySQL pour Python: **https://dev.mysql.com/downloads/connector/python/*
Requests (paquet installable avec Pip): **pip install requests**

## Configuration du fichier SH
Modifiez le fichier main.sh pour pouvoir exécuter le script python depuis cron

# Exécution du script
Le script Python peut-être directment avec la commande suivante:
``` bash
python3 /chemin/vers/le/script.py # Sur linux
python /chemin/vers/le/script.py # Sur Windows
```

# Exécution planifié via Cron (Linux seulement)
Exécutez la commande suivante pour planifier une tâche sur cron:
``` bash
crontab -e

# Dans Cron, vous pouvez écrire la ligne suivante pour lancer le script SH toutes les heures
0 * * * * /chemin/vers/le/script.sh
```
