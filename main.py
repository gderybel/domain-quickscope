from time import time
from dorks_links import get_dorks_links
from domain_informations import get_domain_title, get_related_domain_names, get_domain_informations
from browser import Browser
from report_generator import report_generation

domain = input('Enter a domain or a webpage to test (e.g. : chanel.com) : ')

start = time()

driver = Browser()

title = get_domain_title(domain, driver)

dorks_results = get_dorks_links(title=title)

related_domains = get_related_domain_names(domain)

all_domains = related_domains + dorks_results

del related_domains, dorks_results, title

domains_object_list = []
COUNT = 0
for current_domain in all_domains:
    COUNT +=1
    print(f"Fetching {COUNT}/{len(all_domains)} : {current_domain.get('domain').ljust(max(len(domain['domain']) for domain in all_domains))}", end="\r")
    domain_object = get_domain_informations(current_domain.get('domain'), current_domain.get('method'), driver)
    if domain_object:
        domains_object_list.append(domain_object)
print()
driver.kill()
del driver, COUNT, domain_object, all_domains

report_generation(domains_object_list)
print(f"\nThe program took {int(time() - start)} seconds to execute.")
