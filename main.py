from time import time
from dorks_links import get_dorks_links
from domain_informations import get_domain_title, get_related_domain_names, get_resolvable_domains, get_domains_objects, get_screenshot
from browser import Browser
from report_generator import report_generation

domain = input('Enter a domain to test (e.g. : chanel.com) : ')

start = time()

driver = Browser()
title = get_domain_title(domain, driver)
screenshot = get_screenshot(f"http://{domain}", driver)
driver.kill()

dorks_results = get_dorks_links(title)
related_domains = get_related_domain_names(domain)
all_domains = related_domains + dorks_results

res_domains = get_resolvable_domains(all_domains)
domains_objects = get_domains_objects(res_domains, screenshot)

report_generation(domains_objects)
print(f"\n\nThe program took {int(time() - start)} seconds to execute.")
