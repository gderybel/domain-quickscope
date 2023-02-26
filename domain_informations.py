from os import path, makedirs,cpu_count
from socket import gethostbyname, error as sock_error
from queue import Queue
from threading import Thread
from time import sleep
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

    try:
        driver.screenshot(filepath)
    except TimeoutException:
        return None

    return filepath

def get_domain_information(domain: dict, driver: Browser, requested_domain_screenshot: str) -> Domain | None:
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
    try:
        domain_info = whois(domain.get('domain'))
    except parser.PywhoisError:
        return None

    try:
        driver.get(domain.get('domain'))
        sleep(0.5)
    except TimeoutException:
        pass
    except WebDriverException:
        return None

    if any(item is not None for item in domain_info.values()):
        screenshot = get_screenshot(domain.get('domain'), driver)
        domain_object = Domain(
            domain_info.domain,
            domain.get('domain'),
            domain_info.org,
            domain_info.registrar,
            domain_info.creation_date[0] if isinstance(domain_info.creation_date, list) else domain_info.creation_date,
            domain_info.updated_date[0] if isinstance(domain_info.updated_date, list) else domain_info.update_date,
            domain_info.expiration_date[0] if isinstance(domain_info.expiration_date, list) else domain_info.expiration_date,
            domain_info.emails,
            domain_info.country,
            screenshot,
            domain.get('method'),
            check_images_similarity(requested_domain_screenshot, screenshot)
        )
        return domain_object
    else:
        screenshot = get_screenshot(domain.get('domain'), driver)
        domain_object = Domain(
            None,
            domain.get('domain'),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            screenshot,
            domain.get('method'),
            check_images_similarity(requested_domain_screenshot, screenshot)
        )
        return domain_object

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

def get_resolvable_domains(domains: list[dict], number_of_threads: int = round(cpu_count() * 0.6)) -> list[dict]:
    """This functions sort domains in list which are resolvable

    Parameters
    ----------
    domains : list[dict]
        Input list of domains to check
    threads : int, optional
        Number of threads to engage, default is 60% of your cpu count (rounded)

    Returns
    -------
    list[dict]
        Output list of domains resolvable
    """
    queue = Queue()

    resolvable_domains = []

    def worker():
        while True:
            domain = queue.get()
            if domain is None:
                break
            if is_resolvable(domain.get('domain')):
                resolvable_domains.append(domain)
            queue.task_done()

    for domain in domains:
        queue.put(domain)

    threads = []
    for _ in range(number_of_threads):
        thread = Thread(target=worker)
        thread.start()
        threads.append(thread)

    queue.join()

    for _ in range(number_of_threads):
        queue.put(None)
    for thread in threads:
        thread.join()

    print(f"{len(resolvable_domains)} are accessible.\n")

    return resolvable_domains

def get_domains_objects(domains: list[dict], requested_domain_screenshot: str, number_of_threads: int = round(cpu_count() * 0.6)) -> list[Domain]:
    """Get domains objects with whois information, screenshot, similarity, method, ...

    Parameters
    ----------
    domains : list[dict]
        Domains to fetch
    requested_domain_screenshot : str
        Original request screenshot
    number_of_threads : int, optional
        Number of threads to engage, default is 60% of your cpu count (rounded)

    Returns
    -------
    list[Domain]
        List of Domain objects
    """
    domains_objects = []
    count = 0
    def thread_function(thread_domains):
        driver = Browser()
        nonlocal count
        for current_domain in thread_domains:
            count += 1
            print(f"Fetching {count}/{len(domains)} : {current_domain.get('domain').ljust(max(len(domain['domain']) for domain in domains))}", end="\r")
            domain_object = get_domain_information(current_domain, driver, requested_domain_screenshot)
            if domain_object:
                domains_objects.append(domain_object)
        driver.kill()

    batch_size = len(domains) // number_of_threads + (len(domains) % number_of_threads > 0)

    threads = []
    for i in range(number_of_threads):
        start_index = i * batch_size
        end_index = min((i + 1) * batch_size, len(domains))
        thread_domains = domains[start_index:end_index]

        thread = Thread(target=thread_function, args=(thread_domains,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return domains_objects

def check_images_similarity(image1 :str | None, image2: str | None) -> float |None:
    """This function will check similarity between two photos using SSIM algorithm.

    This algorithm compares the structural information of the two images,
    such as luminance, contrast, and structure.

    Parameters
    ----------
    image1 : str | None
        Path to image 1
    image2 : str | None
        Path to image 2

    Returns
    -------
    float
        Percentage of similarity
    """
    if image1 is None or image2 is None:
        return None

    image_obj1 = io.imread(image1, as_gray=True)
    image_obj2 = io.imread(image2, as_gray=True)

    ssim = metrics.structural_similarity(image_obj1, image_obj2)

    if ssim < 0:
        ssim = 0

    return round(ssim*100,2)
