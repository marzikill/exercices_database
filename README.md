Base de donnée d'exercices de mathématique des professeurs du Lycée Paul Lapie.

Adresse : http://www.pisurquatre.xyz/recherche

Contributeurs :
 - Fanny BUFFET DELMAS
 - Philippe CAMUS 
 - Florian PICARD

# Prérequis 

Les paquets `flask`, `flask-sqlalchemy`, `flask-migrate` et `sqlite` doivent être installés. 

# app

Application Flask
 - `models.py` : création de la base de donnée (champs)
 - `routes.py` : logique et architecture du site

## templates

Fichier de templates utilisés par flask : servent à rendre des pages construites au client.

## static

Fichier javascript, css utilisé pour le site.

# Fichiers à la racine

 - `db_build.py` : fichier d'ajout à la base de donnée. Vide la base de donnée puis la ré-initialise à l'aide des scripts d'extraction par professeurs du dossier `extractors` 
 - `exercice.py` : fichier représentant l'application flask
 - `test_db.py` : fichier pour les bidouilles sur la base de donnée : effectuer les opérations "à la main" à des fins de débogagge.
 - `config.py` : fichier de configuration de la base de donnée.
 - `wsgi.ini`, `wsgi.py` : fichier de config de `uwsgi`.


