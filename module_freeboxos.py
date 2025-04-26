import requests
import logging
import subprocess
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def get_website_title(url):
    """Get the title of a website."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title").string.strip()
        return title
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return None

