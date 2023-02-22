from sys import exit
from requests import get, ReadTimeout
from bs4 import BeautifulSoup
from selenium import webdriver
from whois import whois

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

def get_screenshot(url: str):
    """
        This function will take a screenshot from a given URL.
    """
    driver = webdriver.Firefox()
    driver.get(url)
    filename = '/'.join(url.split('/')[2:3])[:30]
    driver.save_screenshot(f"{filename}.png")

def get_domain_informations(domain: str):
    """
        This function returns some informations about a domain.
    """
    domain_info = whois(domain)

    if not all(domain_info.get(var) is None for var in domain_info):
        result = f"""
____________________________________________________________________________________________________________________________

[+]Domain: {domain_info.domain},
[+]Status: {domain_info.get('status')},
[+]Registrar: {domain_info.get('registrar')},
[+]Update time: {domain_info.get('updated_date')},
[+]Expiration time: {domain_info.get('expiration_date')},
[+]Servers names: {domain_info.get('name_servers')},
[+]Emails: {domain_info.get('emails')}

 ____________________________________________________________________________________________________________________________
"""
        print(result)
    else:
        exit("\nTarget not valid.")
    return domain_info
