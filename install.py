import getpass
import keyring
import logging
import os
import requests
import shutil

from keyring.backends import Windows
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException
from webdriver_manager.firefox import GeckoDriverManager

from time import sleep
from subprocess import Popen, PIPE, run, CalledProcessError

from module_freeboxos import get_website_title

local_appdata = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
app_dir = local_appdata / "select_freeboxos"
log_dir = app_dir / "logs"
log_file = log_dir / "select_freeboxos.log"
config_file = app_dir / "config.py"

log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(log_file),
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("module_freeboxos")

answers = ["oui", "non"]
opciones = ["1", "2", "3"]
opcion = 5
https = False

print("\nBienvenu dans le programme d'installation pour enregistrer "
      "automatiquement les vidéos qui vous correspondent dans votre "
      "Freebox.\nVous pouvez vous connecter à Freebox OS soit par internet, "
      "soit par votre réseau local. Par mesure de sécurité, le programme "
      "utilisera uniquement des connexions par HTTPS pour se connecter par "
      "internet. La connexion par le réseau local se fera en HTTP et n'est donc "
      "pas sécurisé. Ceci ne pose pas de problème si votre PC est fixe et "
      "qu'il reste toujours connecté à votre domicile dans votre réseau "
      "local. Dans le cas contraire, il est conseillé de configurer "
      "l'accès à distance à Freebox OS de manière sécurisée, avec un nom de domaine personnalisé: "
      "https://www.universfreebox.com/article/36003/Tuto-Accedez-a-Freebox-OS-a-distance-de-maniere-securisee-avec-un-nom-de-domaine-personnalise\n"
      "En plus de sécuriser votre connexion par HTTPS, ceci vous permettra de vous "
      "connecter en déplacement.\n"
      )

while opcion not in opciones:
    opcion = input("Merci de choisir une des options suivantes:\n\n1) J'ai "
                   "configuré l'accès à Freebox OS hors de mon domicile et "
                   "je choisis de sécuriser ma connexion par HTTPS.\n\n2) Mon "
                   "PC restera toujours connecté au réseau local de ma "
                   "Freebox et je ne veux pas configurer l'accès à "
                   "à Freebox OS hors de mon domicile.\n\n3) Je "
                   "désire quitter le programme d'installation.\n\n"
                   "Choisissez entre 1 et 3: ")

if opcion == "1":

    FREEBOX_SERVER_IP = input(
        "\nVeuillez saisir l'adresse à utiliser pour l'accès distant de "
        "votre Freebox.\nCelle-ci peut ressembler à "
        "https://votre-sous-domaine.freeboxos.fr:55412\n"
        "Veillez à choisir le port d'accès distant sécurisé (HTTPS et "
        "non HTTP) pour sécuriser la connexion: \n"
    )
    FREEBOX_SERVER_IP = FREEBOX_SERVER_IP.replace("https://", "")
    FREEBOX_SERVER_IP = FREEBOX_SERVER_IP.replace("http://", "")
    FREEBOX_SERVER_IP = FREEBOX_SERVER_IP.rstrip("/")

    url = f"https://{FREEBOX_SERVER_IP}/login.php"

    try:
        response = requests.head(url, timeout=5)
        http_response = response.status_code
    except requests.RequestException as e:
        http_response = 000  # or handle the exception as needed
        print(f"Request failed: {e}")



    while http_response != 200:
        FREEBOX_SERVER_IP = input("\nLa connexion à la Freebox Server a "
            "échoué.\n\nMerci de saisir de nouveau l'adresse à utiliser pour "
            "l'accès distant de votre Freebox.\nCelle-ci peut ressembler à "
            "https://votre-sous-domaine.freeboxos.fr:55412\n"
            "Veillez à choisir le port d'accès distant sécurisé (HTTPS et "
            "non HTTP) pour sécuriser la connexion: \n")
        FREEBOX_SERVER_IP = FREEBOX_SERVER_IP.replace("https://", "")
        FREEBOX_SERVER_IP = FREEBOX_SERVER_IP.replace("http://", "")
        FREEBOX_SERVER_IP = FREEBOX_SERVER_IP.rstrip("/")
        url = f"https://{FREEBOX_SERVER_IP}/login.php"

        try:
            response = requests.head(url, timeout=5)
            http_response = response.status_code
        except requests.RequestException as e:
            http_response = 000  # or handle the exception as needed
            print(f"Request failed: {e}")

elif opcion == "2":

    print("\nVous avez choisi de vous connecter à votre Freebox par votre "
          "réseau local.")

    print("\nLe programme va maintenant se connecter avec l'adresse IP "
          "192.168.1.254 pour déterminer si celui-ci est celui de la Freebox server\n")

    FREEBOX_SERVER_IP = "192.168.1.254"

    url = "http://" + FREEBOX_SERVER_IP

    title = get_website_title(url)

    option = 5
    repeat = False
    out_prog = "nose"

    while title != "Freebox OS":
        print("\nLa connexion à la Freebox Server a échoué.\n\nMerci de vérifier "
                "que vous êtes bien connecté au réseau local de votre Freebox "
                "(cable ethernet ou wifi).")
        if repeat:
            print("\nLe programme a détecté une nouvelle fois que le routeur "
                  "est différent de celui de la Freebox server.\n")
        if title is not None:
            print("\nLe programme a détecté comme nom possible de votre "
                  "routeur la valeur suivante: " + title + "\n")
        else:
            print("\nLe programme n'a pas détecté le nom de votre routeur.\n")
        if repeat:
            while out_prog.lower() not in answers:
                out_prog = input("Voulez-vous continuer de tenter de vous "
                                "connecter? (repondre par oui ou non): ")
        if out_prog.lower() == "non":
            print('\nSortie du programme.\n')
            exit()

        print("Merci de vérifier que vous êtes bien connecté au réseau local "
              "de votre Freebox serveur. \n")
        while option not in opciones:
            option = input(
                "Après avoir fait vérifier la connexion, vous pouvez choisir une "
                "de ces 3 options pour continuer:\n\n1) Vous n'étiez pas "
                "connecté au réseau local de votre Freebox serveur "
                "précédemment et vous voulez tenter de nouveau de vous "
                "connecter\n\n2) Vous êtiez sûr d'être connecté au réseau "
                "local de votre Freebox serveur. Vous avez vérifié l'adresse "
                "ip de la Freebox server dans la fenêtre 'Paramètres de la "
                "Freebox' après avoir clické sur 'Mode réseau' et celle-ci "
                "est différente de 192.168.1.254.\n\n3) "
                "Vous voulez utiliser le nom d'hôte mafreebox.freebox.fr qui "
                "fonctionnera sans avoir besoin de vérifier l'adresse IP de "
                "la freebox server. Il faudra cependant veiller à ne pas "
                "utiliser de VPN avec votre PC/Mac pour pouvoir vous "
                "connecter.\n\nChoisissez entre 1 et 3: "
            )
        if option == "1":
            print("\nLe programme va se connecter avec l'adresse IP "
                "192.168.1.254 pour déterminer si celui-ci est celui de la Freebox server\n")

            FREEBOX_SERVER_IP = "192.168.1.254"

        elif option == "2":
            FREEBOX_SERVER_IP = input(
                "\nVeuillez saisir l'adresse IP de votre Freebox: "
            )
        else:
            FREEBOX_SERVER_IP = "mafreebox.freebox.fr"

        option = "5"

        print("\nNouvelle tentative de connexion à la Freebox:\n\nVeuillez patienter.")
        print("\n---------------------------------------------------------------\n")

        url = "http://" + FREEBOX_SERVER_IP
        title = get_website_title(url)

        repeat = True
        out_prog = "nose"

else:
    print("Merci d'avoir utilisé le programme d'installation pour enregistrer "
          "automatiquement les vidéos qui vous correspondent dans votre "
          "Freebox.\n\nAu revoir!")
    exit()

if opcion == "1":
    https = True

print("Le programme peut atteindre la page de login de Freebox OS. Il "
    "va maintenant tenter de se connecter à Freebox OS avec votre "
    " mot de passe:")

script_dir = Path(__file__).resolve().parent
geckodriver_path = script_dir / "geckodriver.exe"

service = Service(executable_path=GeckoDriverManager().install())

options = webdriver.FirefoxOptions()
options.add_argument("--ignore-ssl-errors=yes")
options.add_argument("--ignore-certificate-errors")
options.add_argument("start-maximized")
options.add_argument("--headless")

try:
    driver = webdriver.Firefox(service=service, options=options)
except SessionNotCreatedException as e:
    print("A SessionNotCreatedException occured. Exit programme.")
    logging.error(
        "A SessionNotCreatedException occured. Exit programme."
    )
    exit()

try:
    if https:
        driver.get("https://" + FREEBOX_SERVER_IP + "/login.php")
    else:
        driver.get("http://" + FREEBOX_SERVER_IP + "/login.php")
except WebDriverException as e:
    if 'net::ERR_ADDRESS_UNREACHABLE' in e.msg:
        print("The programme cannot reach the address " + FREEBOX_SERVER_IP + " . Exit programme.")
        logging.error(
            "The programme cannot reach the address " + FREEBOX_SERVER_IP + " . Exit programme."
        )
        driver.quit()
        exit()
    else:
        print("A WebDriverException occured. Exit programme.")
        logging.error(
            "A WebDriverException occured. Exit programme."
        )
        driver.quit()
        exit()



go_on = True
not_connected = True
answer_hide = "maybe"
n = 0

while not_connected:
    if answer_hide.lower() == "oui":
        freebox_os_password = input(
            "\nVeuillez saisir votre mot de passe admin de la Freebox: "
        )
    else:
        freebox_os_password = getpass.getpass(
            "\nVeuillez saisir votre mot de passe admin de la Freebox: "
        )
    print(
        "\nVeuillez patienter pendant la tentative de connexion à "
        "Freebox OS avec votre mot de passe.\n"
    )
    sleep(4)
    login = driver.find_element("id", "fbx-password")
    sleep(1)
    login.clear()
    sleep(1)
    login.click()
    sleep(1)
    login.send_keys(freebox_os_password)
    sleep(1)
    login.send_keys(Keys.RETURN)
    sleep(6)

    try:
        login = driver.find_element("id", "fbx-password")
        try_again = input(
            "\nLe programme install.py n'a pas pu se connecter à Freebox OS car "
            "le mot de passe ne correspond pas à celui enregistré dans "
            "la Freebox.\nVoulez-vous essayer de nouveau?(oui ou non): "
        )
        if try_again.lower() == "oui":
            if answer_hide.lower() != "oui":
                while answer_hide.lower() not in answers:
                    answer_hide = input(
                        "\nVoulez-vous afficher le mot de passe que vous saisissez "
                        "pour que cela soit plus facile? (répondre par oui ou non): "
                    )
            n += 1
            if n > 6:
                print(
                    "\nImpossible de se connecter à Freebox OS avec ce mot de passe. "
                    "Veuillez vérifier votre mot de passe de connexion admin en vous "
                    "connectant à l'adresse http://mafreebox.freebox.fr/login.php puis "
                    "relancez le programme install.py. "
                )
                driver.quit()
                go_on = False
                break
        else:
            driver.quit()
            go_on = False
            break
    except:
        print("Le mot de passe correspond bien à votre compte admin Freebox OS")
        not_connected = False
        sleep(2)
        driver.quit()

max_sim_recordings = 0
title_answer = "no_se"
change_max_rec = "no_se"
record_logs = "no_se"

if go_on:
    while title_answer.lower() not in answers:
        title_answer = input(
            "\nVoulez-vous utiliser le nommage de TV-select "
            "pour nommer les titres des programmes? Si vous répondez oui, alors "
            "les titres seront composés du titre du programme, de son numéro "
            "d'idendification dans MEDIA-select puis de la recherche "
            "correspondante. Si vous répondez non, le nommage de Freebox OS "
            "sera utilisé (dans ce cas des erreurs peuvent apparaitre si la "
            "différence de temps (marge avant le début du film) est trop "
            "grande): "
        )
    print("\n\nLe nombre maximum de flux simultanés autorisé par Free est "
          "limité à 2 selon l'assistance de Free:\n"
          "https://assistance.free.fr/articles/gerer-et-visionner-mes-enregistrements-72\n"
          "Cependant, cette limite semble venir du faible débit de l'ADSL et il "
          "est possible d'enregistrer un plus grand nombre de vidéos "
          "simultanément si vous avez la fibre optique.\n")
    while change_max_rec.lower() not in answers:
        change_max_rec = input("Voulez-vous augmenter le nombre maximum "
                        "d'enregistrements simultanés autorisés par "
                        "le programme? (répondre par oui ou non): ")

    if change_max_rec.lower() == "oui":
        while max_sim_recordings <= 0:
            max_sim_recordings = input(
                "\nVeuillez saisir le nombre de vidéos simultanément enregistrées "
                "autorisé par le programme: "
            )
            try:
                max_sim_recordings = int(max_sim_recordings)
            except ValueError:
                max_sim_recordings = 0
                print(
                    "\nVeuillez saisir un nombre entier supérieur à 0 pour le "
                    "nombre de vidéos simultanément enregistrées par le "
                    "programme."
                )
    else:
        max_sim_recordings = 2

    while record_logs.lower() not in answers:
        record_logs = input(
            "\n\nAutorisez-vous l'application à collecter et envoyer des journaux "
            "d'erreurs anonymisés pour améliorer les performances et corriger les "
            "bugs? (répondre par oui ou non) : ").strip().lower()

    config_file = app_dir / "config.py"
    template_conf_file = script_dir / "config_template.py"

    if not os.path.exists(config_file):
        shutil.copy(template_conf_file, config_file)
        os.chmod(config_file, 0o640)

    crypted = "no_se"

    while crypted.lower() not in answers:
        crypted = input("\nVoulez vous chiffrer les identifiants de connexion à "
                        "l'application web MEDIA-select.fr ainsi que le mot de passe "
                        "admin à Freebox OS? Si vous répondez oui, "
                        "il faudra penser à débloquer Windows Credential Manager (ou tout "
                        "autre backend disponible sur votre système d'exploitation) à chaque "
                        "nouvelle session afin de permettre l'accès aux "
                        "identifiants par l'application select-freeboxos. Si vous "
                        "répondez non, les identifiants de connexion seront stockés "
                        f"en clair dans le fichier {config_file} ."
                        "(répondre par oui ou non) : ").strip().lower()

    print("\nConfiguration des tâches cron du programme MEDIA-select:\n")

    response = requests.head("https://media-select.fr")
    http_response = response.status_code

    if http_response != 200:
        print(
            "\nLa box MEDIA-select n'est pas connectée à internet. Veuillez "
            "vérifier votre connection internet et relancer le programme "
            "d'installation.\n\n"
        )
        go_on = False

    if go_on:
        username_mediaselect = input(
            "Veuillez saisir votre identifiant de connexion (adresse "
            "email) sur MEDIA-select.fr: "
        )
        password_mediaselect = getpass.getpass(
            "Veuillez saisir votre mot de passe sur MEDIA-select.fr: "
        )

        http_status = 403

        while http_status != 200:

            response = requests.head("https://www.media-select.fr/api/v1/progweek", auth=(username_mediaselect, password_mediaselect))
            http_status = response.status_code

            if http_status != 200:
                try_again = input(
                    "Le couple identifiant de connexion et mot de passe "
                    "est incorrect.\nVoulez-vous essayer de nouveau?(oui ou non): "
                )
                answer_hide = "maybe"
                if try_again.lower() == "oui":
                    username_mediaselect = input(
                        "Veuillez saisir de nouveau votre identifiant de connexion (adresse email) sur MEDIA-select.fr: "
                    )
                    while answer_hide.lower() not in answers:
                        answer_hide = input(
                            "Voulez-vous afficher le mot de passe que vous saisissez "
                            "pour que cela soit plus facile? (répondre par oui ou non): "
                        )
                    if answer_hide.lower() == "oui":
                        password_mediaselect = input(
                            "Veuillez saisir de nouveau votre mot de passe sur MEDIA-select.fr: "
                        )
                    else:
                        password_mediaselect = getpass.getpass(
                            "Veuillez saisir de nouveau votre mot de passe sur MEDIA-select.fr: "
                        )
                else:
                    go_on = False
                    break
        if go_on:
            params = ["ADMIN_PASSWORD",
                    "FREEBOX_SERVER_IP",
                    "MEDIA_SELECT_TITLES",
                    "MAX_SIM_RECORDINGS",
                    "SENTRY_MONITORING_SDK",
                    "CRYPTED_CREDENTIALS",
                    "MEDIA_EMAIL",
                    "MEDIA_PASSWORD"
                    ]

            with open(config_file, "w") as conf:
                https_present = False
                for param in params:
                    if "ADMIN_PASSWORD" in param:
                        if crypted.lower() == "oui":
                            conf.write('ADMIN_PASSWORD = "XXXXXXX"\n')
                        else:
                            conf.write('ADMIN_PASSWORD = "' + freebox_os_password + '"\n')
                    elif "FREEBOX_SERVER_IP" in param:
                        if crypted.lower() == "oui":
                            conf.write('FREEBOX_SERVER_IP = "XXXXXXX"\n')
                        else:
                            conf.write('FREEBOX_SERVER_IP = "' + FREEBOX_SERVER_IP + '"\n')
                    elif "MEDIA_SELECT_TITLES" in param:
                        if title_answer.lower() == "oui":
                            conf.write("MEDIA_SELECT_TITLES = True\n")
                        else:
                            conf.write("MEDIA_SELECT_TITLES = False\n")
                    elif "MAX_SIM_RECORDINGS" in param:
                        conf.write("MAX_SIM_RECORDINGS = " + str(max_sim_recordings) + "\n")
                    elif "HTTPS" in param:
                        https_present = True
                        if https:
                            conf.write("HTTPS = True\n")
                        else:
                            conf.write("HTTPS = False\n")
                    elif "SENTRY_MONITORING_SDK" in param:
                        if record_logs.lower() == "oui":
                            conf.write("SENTRY_MONITORING_SDK = True\n")
                        else:
                            conf.write("SENTRY_MONITORING_SDK = False\n")
                    elif "CRYPTED_CREDENTIALS" in param:
                        if crypted.lower() == "oui":
                            conf.write("CRYPTED_CREDENTIALS = True\n")
                        else:
                            conf.write("CRYPTED_CREDENTIALS = False\n")
                    elif "MEDIA_EMAIL" in param:
                        if crypted.lower() == "oui":
                            conf.write('MEDIA_EMAIL = "XXXXXXX"\n')
                        else:
                            conf.write('MEDIA_EMAIL = "' + username_mediaselect + '"\n')
                    elif "MEDIA_PASSWORD" in param:
                        if crypted.lower() == "oui":
                            conf.write('MEDIA_PASSWORD = "XXXXXXX"\n')
                        else:
                            conf.write('MEDIA_PASSWORD = "' + password_mediaselect + '"\n')
                    else:
                        conf.write(param + "\n")
                if not https_present:
                    if https:
                        conf.write("HTTPS = True\n")
                    else:
                        conf.write("HTTPS = False\n")


            if crypted.lower() == "oui":
                print("\nVous avez choisi de chiffrer vos identifiants et ceux-ci seront donc stockés de "
                    "manière sécurisée dans le Gestionnaire d'informations d'identification de Windows. "
                    "Assurez-vous que votre session Windows est correctement déverrouillée à chaque "
                    "démarrage pour permettre au programme select_freeboxos d'y accéder automatiquement.\n")

                keyring.set_keyring(Windows.WinVaultKeyring())
                keyring.set_password("media-select", "username", username_mediaselect)
                keyring.set_password("media-select", "password", password_mediaselect)
                keyring.set_password("freeboxos", "username", FREEBOX_SERVER_IP)
                keyring.set_password("freeboxos", "password", freebox_os_password)
