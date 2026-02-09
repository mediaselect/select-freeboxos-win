===============================================
INSTALLATION DE SELECT_FREEBOXOS (Windows)
===============================================
select-freeboxos-win v2.0.0

Ce programme permet de lancer automatiquement un script Python à chaque démarrage de Windows.

PRÉREQUIS :
------------
- Python 3 doit être installé sur votre machine (https://www.python.org/downloads/)
- Vous devez avoir les droits d'administrateur

ÉTAPES D'INSTALLATION :
-----------------------

1. Téléchargez et décompressez le fichier `select-freeboxos-win-master.zip` où vous voulez (par exemple dans le dossier Téléchargements).

2. Ouvrez PowerShell en tant qu'administrateur :
   - Cliquez sur le bouton Démarrer
   - Tapez "powershell"
   - Faites un clic droit sur "Windows PowerShell" et choisissez "Exécuter en tant qu'administrateur"

3. Dans PowerShell, naviguez dans le dossier décompressé :
   Exemple si vous l'avez mis dans Téléchargements :
   cd "$HOME\Downloads\select-freeboxos-win-master"

4. Lancez le script d'installation :
   .\setup.ps1

SECURITE ET MODES DE CONNEXION
=============================

Ce programme automatise l’accès à l’interface Freebox OS afin de programmer
des enregistrements TV sans intervention manuelle.

Il manipule des identifiants administrateur sensibles. Une attention
particulière est donc portée à la sécurité.


MODES DE CONNEXION
------------------

Le programme peut fonctionner dans trois contextes distincts :


MODE LOCAL (RECOMMANDE)
----------------------
- Exécution sur un ordinateur toujours présent sur le réseau domestique
- Connexion directe à la Freebox via le réseau local
- HTTP autorisé uniquement dans ce contexte

Conditions requises :
- réseau privé et de confiance
- machine ne quittant jamais le domicile


MODE DISTANT SECURISE
--------------------
- Exécution possible depuis des réseaux externes
- HTTPS obligatoire
- Communications chiffrées
- Risque maîtrisé

Ce mode est requis si l’ordinateur est portable ou utilisé en déplacement.


MODE DISTANT NON SECURISE (BLOQUE)
---------------------------------
- Connexion HTTP depuis Internet ou un réseau public
- Exposition possible du mot de passe administrateur

Ce mode est automatiquement bloqué par le programme.


PROTECTION AUTOMATIQUE
---------------------

Par défaut, le programme active un mode de sécurité stricte :

- Les connexions HTTP sont autorisées uniquement lorsque la Freebox
résout vers une adresse IP privée (réseau local).
- Si l’adresse détectée est publique et que HTTPS est désactivé,
le programme s’arrête pour éviter l’exposition du mot de passe.
