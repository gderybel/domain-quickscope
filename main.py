from DorksLinks import get_dorks_link
from DomainInformations import get_domain_title, get_related_domain_names, get_domain_informations
from Browser import Browser
from ReportGenerator import report_generation
from time import time

domain = input('Enter a domain or a webpage to test (e.g. : chanel.com) : ')

start = time()

browser = Browser()

title = get_domain_title(domain, browser)
print(f"""
The title found is "{title}".
""")

dorks_results = get_dorks_link(title=title)

related_domains = get_related_domain_names(domain)

all_domains = related_domains + dorks_results

del related_domains, dorks_results, title

domains_object_list = []
count = 0
for current_domain in all_domains:
    count +=1
    print(f"Fetching {count}/{len(all_domains)} : {current_domain.ljust(len(max(all_domains, key=len)))}", end="\r")
    domain_object = get_domain_informations(current_domain, browser)
    if domain_object:
        domains_object_list.append(domain_object)
print()
browser.kill()
del browser, count, domain_object, all_domains

report_generation(domains_object_list)
print(f"\nThe program took {int(time() - start)} seconds to execute.")