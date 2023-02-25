from os import path, makedirs
from socket import gethostbyname, error as sock_error
from selenium.common.exceptions import TimeoutException, WebDriverException
from whois import whois, parser
from browser import Browser
from domain import Domain
from permutation import generate_permutations


def get_domain_title(domain_name: str, driver: Browser) -> str:
    """This function returns the title of a webpage.

    Parameters
    ----------
    domain_name : str
        Domain to fetch
    driver : Browser
        Browser to make request with

    Returns
    -------
    str
        Title of the website
    """
    if not domain_name.startswith("http"):
        domain_name = f"http://{domain_name}"
    title = driver.get_title(domain_name)

    print(f"""
The title found is "{title}".
""")

    return title

def get_screenshot(url: str, driver: Browser) -> str:
    """This function will take a screenshot from a given URL.

    Parameters
    ----------
    url : str
        Url to fetch
    driver : Browser
        Browser to make request with

    Returns
    -------
    str
        Filepath of the screenshot
    """
    dir_path = 'domain_output'
    if not path.exists(dir_path):
        makedirs(dir_path)

    if not url.startswith("http"):
        url = f"http://{url}"

    filename = '/'.join(url.split('/')[2:3])[:30]

    filepath = f"{dir_path}/{filename}.png"

    driver.screenshot(filepath)

    return filepath

def get_domain_informations(domain_name: str, driver: Browser) -> Domain | None:
    """This function returns some informations about a domain.

    Parameters
    ----------
    domain_name : str
        The domain to fetch
    driver : Browser
        The browser to make requests with

    Returns
    -------
    Domain | None
        A domain object with information if the domain was found, else None
    """

    if not is_resolvable(domain_name):
        return None

    try:
        domain_info = whois(domain_name)
    except parser.PywhoisError:
        return None

    try:
        driver.get(domain_name)
    except (TimeoutException, WebDriverException):
        return None

    if any(item is not None for item in domain_info.values()):
        domain_object = Domain(
            domain_info.domain,
            domain_name,
            domain_info.org,
            domain_info.registrar,
            domain_info.creation_date[0] if isinstance(domain_info.creation_date, list) else domain_info.creation_date,
            domain_info.updated_date[0] if isinstance(domain_info.updated_date, list) else domain_info.update_date,
            domain_info.expiration_date[0] if isinstance(domain_info.expiration_date, list) else domain_info.expiration_date,
            domain_info.emails,
            domain_info.country,
            get_screenshot(domain_name, driver)
        )
        return domain_object
    else:
        return None

def get_related_domain_names(domain_name: str) -> list[str]:
    """This function will return a list of domain names that are
       looking like the given one.

    Parameters
    ----------
    domain_name : str
        The domain to look for permutations

    Returns
    -------
    list[str]
        A list of permutations
    """
    print("Looking for related domain names...\n")
    permutations = generate_permutations(domain_name)
    permutations = [f"http://{permutation}" for permutation in permutations]

    print(f"{len(permutations)} domain(s) was/were found.\n")

    return permutations

def is_resolvable(domain_name: str) -> bool:
    """This function check is a domain name can be resolved

    Parameters
    ----------
    domain : str
        The domain to resolve

    Returns
    -------
    bool
        Returns True if domain was resolved and False if it was not
    """
    try:
        gethostbyname(domain_name.split('/', 3)[2])
        return True
    except sock_error:
        return False
