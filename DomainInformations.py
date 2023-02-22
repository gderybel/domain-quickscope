from sys import exit as sysexit
from os import path, makedirs
from requests import get, ReadTimeout
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from whois import whois
import dnstwist
from Browser import Browser


def get_domain_title(domain: str):
    """
        This function returns the title of a webpage.
    """
    try:
        response = get(domain, timeout=5)
    except ReadTimeout:
        sysexit('The script was unable to contact this url, please try with another one.\n')
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string.strip()
    return title

def get_screenshot(url: str, browser: Browser):
    """
        This function will take a screenshot from a given URL.
    """
    dir_path = 'domain_output'
    if not path.exists(dir_path):
        makedirs(dir_path)
    
    try:
        browser.get(url)
    except TimeoutException:
        pass

    filename = '/'.join(url.split('/')[2:3])[:30]

    browser.screenshot(f"{dir_path}/{filename}.png")

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
        sysexit("\nTarget not valid.")
    return domain_info

def get_related_domain_names(domain: str):
    """
        This function will return a list of domain names that are
        looking like the given one.
    """
    print("Looking for related domain names...\n")
    dnstwist_result = dnstwist.run(domain=domain, format=None, registered=True)
    related_domains = []
    for result in dnstwist_result:
        related_domains.append(result['domain'])
    
    print(f"{len(related_domains)} domain(s) was/were found.\n")

    return related_domains
