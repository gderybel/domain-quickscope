from os import path, makedirs
from selenium.common.exceptions import TimeoutException, WebDriverException
from whois import whois, parser
from Browser import Browser
from Domain import Domain
from permutation import generate_permutations


def get_domain_title(domain: str, browser: Browser):
    """
        This function returns the title of a webpage.
    """
    if not domain.startswith("http"):
        domain = f"http://{domain}"
    title = browser.get_title(domain)
    return title

def get_screenshot(url: str, browser: Browser):
    """
        This function will take a screenshot from a given URL.
    """
    dir_path = 'domain_output'
    if not path.exists(dir_path):
        makedirs(dir_path)

    if not url.startswith("http"):
        url = f"http://{url}"

    filename = '/'.join(url.split('/')[2:3])[:30]

    filepath = f"{dir_path}/{filename}.png"

    browser.screenshot(filepath)

    return filepath

def get_domain_informations(domain: str, browser: Browser):
    """
        This function returns some informations about a domain.
    """

    try:
        domain_info = whois(domain)
    except parser.PywhoisError:
        return None

    try:
        browser.get(domain)
    except (TimeoutException, WebDriverException):
        return None

    if any(item is not None for item in domain_info.values()):
        domain__object = Domain(
            domain_info.domain,
            domain,
            domain_info.org,
            domain_info.registrar,
            domain_info.creation_date[0] if isinstance(domain_info.creation_date, list) else domain_info.creation_date,
            domain_info.updated_date[0] if isinstance(domain_info.updated_date, list) else domain_info.update_date,
            domain_info.expiration_date[0] if isinstance(domain_info.expiration_date, list) else domain_info.expiration_date,
            domain_info.emails,
            domain_info.country,
            get_screenshot(domain, browser)
        )
        return domain__object
    else:
        return None

def get_related_domain_names(domain: str):
    """
        This function will return a list of domain names that are
        looking like the given one.
    """
    print("Looking for related domain names...\n")
    permutations = generate_permutations(domain)
    permutations = [f"http://{permutation}" for permutation in permutations]

    print(f"{len(permutations)} domain(s) was/were found.\n")

    return permutations
