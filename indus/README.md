# Processus


# Environnement de dev conteunerisé

## Quick start


### Prérequis (peut-etre à ajuster)

- VM ou VM Serveur vierge avec docker/compose
- installation de git (avec accès placide)
- un accès à artifactory

### Clone du répo git

git clone ...

Verifier que les fichiers Dockerfile et *.docker-compose.yml situés dans /indus/docker correspondent bien au besoin (Package, Mongo, MailHog...)

### Connexion répository docker artifactory

````
docker login ASCS-docker-stages.artifactory.ascs.fr
````

(utilisation des credentials artifactory 'reader-token')

### Alias (optionel mais la suite du quickstart l'utilise)

un petit alias est assez pratique : 
````
alias dc="docker-compose --project-directory . -f ./indus/docker/dev.docker-compose.yml -p dc_env"
````
### Définition des variables d'env de build

set les variables d'environnement necessaires au build :


````
export ASCS_READER_PASSWORD=TO_REPLACE
export ASCS_PYPI_REGISTRY_URL=https://artifactory.ascs.fr/artifactory/api/pypi/ASCS-pypi-stages-local
export ASCS_DOCKER_REGISTRY_URL=ASCS-docker-stages.artifactory.ascs.fr
export BUILD_TIME_ENV="
POETRY_HTTP_BASIC_ASCS_PYPI_USERNAME=ASCS-reader
POETRY_HTTP_BASIC_ASCS_PYPI_PASSWORD=TO_REPLACE
ASCS_PYPI_REGISTRY_URL=$ASCS_PYPI_REGISTRY_URL
"
````

- soit via un export (exécution des lignes si dessus dans un shell)
- soit en sourcant un fichier qui contient ces lignes (. fichier.env)


## Build de l'image de l'env de dev

le step est necessaire seulement 
- à l'initialisation de l'env de dev 
- pour prise en compte si modification des fichiers docker ou indus

avec le dossier courant étant à la racine de la copie de travail git:

````
dc build
````

``--project-directory .`` : comme le compose file n'est pas positionné a la racine du projet, positionne le répertoire de travail à la racine du projet

``--progress=plain`` : facilite les debug et affiche toutes les traces du build

``-p dc_env`` : utilisation d'un groupe compose dc_env : permet de partager le volume de dev avec les autres containers (évite d'installer les modules à chaque clone de projet)

### Définition des variables d'env de run


set les variables d'environnement necessaires au build dans le fichier .env à la racine de la copie git.
attention ces variables sont au format .env docker compose et ne doivent pas être encadrées de quotes

ex: ``variable=[ {"json_key": "json_value" } ]``

full ex :

````
# .env compose file format (do not add quotes arround values)

API_V1_STR=/api/v1
ACCESS_TOKEN_EXPIRE_MINUTES=1440
SERVER_HOST=0.0.0.0
BACKEND_CORS_ORIGINS=["http://localhost"]

PROJECT_NAME=Ascs CMS
PROJECT_VERSION=<VERSION>
PROJECT_DESCRIPTION=CMS

DATABASE_NAME=ascs_cms
#DATABASE_URL=DATABASE_URL_DEV
DATABASE_URL=mongodb://ascs_cms:ascs_cms@mongo:27017/ascs_cms

# SMTP
SMTP_SENDER=sendmaster@ascs.fr
SMTP_PORT=25
#SMTP_HOST=smtp.server.local
````


### Run de l'image de l'env de dev

avec le dossier courant étant à la racine de la copie de travail git:

````
dc up
````

ajouter l'option ``-d`` pour détacher le compose si nécessaire

### Run du module

#### console

````
dc run -it dev_container python3 /app/app/main.py
+ python3 /app/app/main.py
2024-01-05 13:17:03,747 - database.py:15 - [INFO] [core] - Database Client Initializing
2024-01-05 13:17:03,920 - routers_loader.py:30 - [INFO] [core] - Import all routers from components
2024-01-05 13:17:06,729 - server.py:76 - [INFO] Started server process [10]
2024-01-05 13:17:06,729 - on.py:46 - [INFO] Waiting for application startup.
2024-01-05 13:17:06,779 - base.py:454 - [INFO] Adding job tentatively -- it will be properly scheduled when the scheduler starts
2024-01-05 13:17:06,780 - base.py:895 - [INFO] Added job "full_workflow_for_a_day" to job store "default"
2024-01-05 13:17:06,780 - base.py:181 - [INFO] Scheduler started
2024-01-05 13:17:06,781 - on.py:60 - [INFO] Application startup complete.
2024-01-05 13:17:06,782 - server.py:218 - [INFO] Uvicorn running on http://0.0.0.0:7000 (Press CTRL+C to quit)
````

#### mode ide

se connecter dans le container avec l'IDE, l'application est installée dans ``/app``

# Update du fichier lock (si il n'est pas directement déjà monté dans le container, voir volumes compose)

dans le cas ou on dois ajouter/supprimer des dépendances (poetry add etc..) il faut bien reprendre les fichiers pyproject.toml et poetry.lock qui ont étés modifiés dans le container

````
dc cp dev_container:/app/pyproject.toml  .
[+] Copying 1/0
 ✔ dev_container copy dev_container:/app/pyproject.toml to . Copied                                                                                                                        0.0s 

dc cp dev_container:/app/poetry.lock  .
[+] Copying 1/0
 ✔ dev_container copy dev_container:/app/poetry.lock to . Copied    
 ````

## Refresh du poetry.lock (si docker cp ou docker-compose cp n'est pas disponible)

après un build de l'image passé correctement :

````
docker run --entrypoint=/bin/bash -it $(docker image ls -q | head -1) -c "cat /app/poetry.lock" > ./poetry.lock
````
