from requests import get, ReadTimeout
from bs4 import BeautifulSoup

def get_domain_title(domain: str):
    """
        This function returns the title of a webpage.
    """
    try:
        response = get(domain, timeout=5)
    except ReadTimeout:
        exit('The script was unable to contact this url, please try with another one.\n')
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string.strip()
    return title