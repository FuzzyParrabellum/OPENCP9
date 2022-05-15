Présentation 

Cette application Django nommée LITReview permet à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande.

Instructions d'Installation

Tout d'abord, téléchargez ces différents fichiers dans un dossier que vous choisirez. Créez ensuite dans ce dossier un environnement virtuel nommé : venv

Par ex avec la commande : python -m venv venv

(La version de python utilisée pour créer cette application est la 3.9.2)

Utilisez la commande dans un éditeur de commande : pip install -r /path/to/requirements.txt où /path/to/requirements.txt est le chemin d'accès vers le fichier requirements.txt fourni dans ce repository

Après avoir activé l'environnement virtuel avec la commande : source venv/bin/activate  , vous pourrez ensuite lancer l'application LITReview en local avec la commande : python LITReview/manage.py runserver
Cette commande vous fournira un lien vous permettant de lancer l'application Django en local sur votre navigateur web.

Quelques exemples d'utilisateurs et de posts ont déjà été intégrés dans la base de donnée fournie dans ce repository. Vous pouvez notamment vous connecter avec les identifiants arsene ou alice avec comme mot de passe arsenepassword et alicepassword ou les suivre après avoir crée un compte pour pouvoir voir leurs posts.
