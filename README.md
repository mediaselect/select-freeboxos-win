# 🖥️ Installation de Select FreeboxOS (Windows)
# select-freeboxos-win v2.0.0:

## Instructions d'installation:

Voir les instructions d'installation détaillés sur la page de votre compte à l'adresse www.media-select.fr

Ce programme lance automatiquement un script Python à chaque démarrage de Windows.

## 🔧 Prérequis

- Python 3 doit être installé sur votre machine : [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Droits administrateur nécessaires

## 📦 Installation

1. **Téléchargez** et **décompressez** l'archive `select-freeboxos-win-master.zip` (par exemple dans `Téléchargements`).

2. **Ouvrez PowerShell en tant qu’administrateur** :
   - Démarrer > Rechercher "PowerShell"
   - Clic droit > Exécuter en tant qu'administrateur

3. **Accédez au dossier extrait** :
   ```powershell
   cd "$HOME\Downloads\select-freeboxos-win-master"

4. **Lancez le script d’installation** :
    ```powershell
    .\setup.ps1

## Sécurité et modes de connexion

Ce programme automatise l’accès à l’interface **Freebox OS** afin de programmer
des enregistrements TV sans intervention manuelle.
Il manipule des **identifiants administrateur sensibles**. Une attention
particulière est donc portée à la sécurité.


### Modes de connexion

Le programme peut fonctionner dans trois contextes distincts :

#### 🟢 Mode local (recommandé)
- Exécution sur un ordinateur **toujours présent sur le réseau domestique**
- Connexion directe à la Freebox via le réseau local
- HTTP autorisé uniquement dans ce contexte

Conditions :
- réseau privé et de confiance
- machine non utilisée hors du domicile

#### 🟡 Mode distant sécurisé
- Exécution possible depuis des réseaux externes
- **HTTPS obligatoire**
- Communications chiffrées
- Risque maîtrisé

Ce mode est requis si l’ordinateur est portable ou utilisé en déplacement.

#### 🔴 Mode distant non sécurisé (déconseillé / bloqué)
- Connexion HTTP depuis Internet ou un réseau public
- Exposition possible du mot de passe administrateur

Ce mode est **automatiquement bloqué** par le programme.

### Protection automatique

Par défaut, le programme active un **mode de sécurité stricte** :

- Les connexions HTTP sont autorisées uniquement lorsque la Freebox
résout vers une adresse IP privée (réseau local).
- Si l’adresse détectée est publique et que HTTPS est désactivé,
le programme s’arrête pour éviter l’exposition du mot de passe.
