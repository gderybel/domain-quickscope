from os import path, makedirs
from socket import gethostbyname, error as sock_error
from selenium.common.exceptions import TimeoutException, WebDriverException
from whois import whois, parser
from skimage import io, metrics
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

def get_domain_informations(domain_name: str, finding_method: str, driver: Browser, requested_domain_screenshot: str) -> Domain | None:
    """This function returns some informations about a domain.

    Parameters
    ----------
    domain_name : str
        The domain to fetch
    finding_method : str
        The method used to guess that name
    driver : Browser
        The browser to make requests with
    requested_domain_screenshot : str
        Path to screenshot of the original domain

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
        screenshot = get_screenshot(domain_name, driver)
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
            screenshot,
            finding_method,
            check_images_similarity(requested_domain_screenshot, screenshot)
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
    
    for permutation in permutations:
        permutation.update(domain=f"http://{permutation.get('domain')}")

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

def check_images_similarity(image1 :str, image2: str) -> float:
    """This function will check similarity between two photos using SSIM algorithm.

    This algorithm compares the structural information of the two images,
    such as luminance, contrast, and structure.

    Parameters
    ----------
    image1 : str
        Path to image 1
    image2 : str
        Path to image 2

    Returns
    -------
    float
        Percentage of similarity
    """
    image1 = io.imread(image1, as_gray=True)
    image2 = io.imread(image2, as_gray=True)

    ssim = metrics.structural_similarity(image1, image2)

    if ssim < 0:
        ssim = 0

    return round(ssim*100,2)
