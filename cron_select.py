# import importlib.util
import logging
import json
import keyring
import os
import requests
import sys

from keyring.backends import Windows
from pathlib import Path
from subprocess import Popen, PIPE, run
from datetime import datetime
from logging.handlers import RotatingFileHandler


local_appdata = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
app_dir = local_appdata / "select_freeboxos"
log_dir = app_dir / "logs"
log_file = log_dir / "select_freeboxos.log"

max_bytes = 10 * 1024 * 1024  # 10 MB
backup_count = 5
log_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)

log_format = '%(asctime)s %(levelname)s %(message)s'
log_datefmt = '%d-%m-%Y %H:%M:%S'
formatter = logging.Formatter(log_format, log_datefmt)

log_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(log_handler)

logger.setLevel(logging.INFO)

config_path = app_dir / "config.json"

try:
    with config_path.open(encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    logger.error("Missing config.json file")
    sys.exit(1)
except json.JSONDecodeError:
    logger.error("Invalid JSON in config.json")
    sys.exit(1)

CRYPTED_CREDENTIALS = bool(config.get("CRYPTED_CREDENTIALS", False))

MEDIA_EMAIL = config.get("MEDIA_EMAIL")
MEDIA_PASSWORD = config.get("MEDIA_PASSWORD")

def get_file_modification_time(file_path):
    try:
        mod_time = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mod_time)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None

def remove_items(INFO_PROGS, INFO_PROGS_LAST, PROGS_TO_RECORD):
    # Remove items already set to be recorded
    try:
        with open(INFO_PROGS, 'r') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        logger.error(
        "No info_progs.json file. Need to check curl command or "
        "internet connection. Exit programme."
        )
        exit()
    except json.decoder.JSONDecodeError:
        logger.error(
        "JSONDecodeError in info_progs.json file. Need to check curl command or "
        "internet connection. Exit programme."
        )
        exit()

    try:
        with open(INFO_PROGS_LAST, 'r') as f:
            items_to_remove = json.load(f)
    except FileNotFoundError:
        items_to_remove = []

    modified_data = [item for item in source_data if item not in items_to_remove]

    with open(PROGS_TO_RECORD, 'w') as f:
        json.dump(modified_data, f, indent=4)

API_URL = "https://www.media-select.fr/api/v1/progweek"
INFO_PROGS = app_dir / "info_progs.json"
INFO_PROGS_LAST =  app_dir / "info_progs_last.json"
PROGS_TO_RECORD = app_dir / "progs_to_record.json"

file_path = str(INFO_PROGS)

to_download_info = False

try:
    mod_time = os.path.getmtime(file_path)
    time_file = datetime.fromtimestamp(mod_time)
    size_file = os.path.getsize(file_path)
    time_diff = datetime.now() - time_file
except FileNotFoundError:
    logger.warning(f"File not found: {file_path}")
    to_download_info = True
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=False)
    to_download_info = True


info_progs_last_mod_time = get_file_modification_time(INFO_PROGS_LAST)

if info_progs_last_mod_time is None or info_progs_last_mod_time.date() < datetime.now().date():
    if to_download_info or time_diff.total_seconds() > 1800 or size_file == 0:
        if CRYPTED_CREDENTIALS:
            keyring.set_keyring(Windows.WinVaultKeyring())
            try:
                username = keyring.get_password("media-select", "username")
                password = keyring.get_password("media-select", "password")

                if username is None or password is None:
                    logger.error("Credentials not found in keyring. Please set them before proceeding.")
                    raise ValueError("Missing credentials in keyring.")
            except keyring.errors.KeyringError as e:
                logger.error(f"Keyring access error: {e}", exc_info=False)
                raise ValueError("Failed to access the keyring.")
        else:
            username = MEDIA_EMAIL
            password = MEDIA_PASSWORD

        try:
            response = requests.get(
                        API_URL,
                        auth=(username, password),
                        headers={"Accept": "application/json; indent=4"},
                        timeout=10,
                    )

            response.raise_for_status()

            with open(INFO_PROGS, "w") as f:
                f.write(response.text)

            logger.info("Data downloaded with requests successfully.")

        except requests.RequestException as e:
            logger.error(f"API request failed: {e}", exc_info=False)
        except ValueError as e:
            logger.error(f"Error: {e}", exc_info=False)

        remove_items(INFO_PROGS, INFO_PROGS_LAST, PROGS_TO_RECORD)

        try:
            from freeboxos import run_freebox_operations
            run_freebox_operations()
        except Exception as e:
            logger.exception(f"run_freebox_operations() failed: {e}", exc_info=False)

