from time import sleep
from DorksLinks import get_dorks_link
from DomainInformations import get_domain_title, get_related_domain_names, get_domain_informations
from Browser import Browser
from ReportGenerator import report_generation

domain = input('Enter a domain or a webpage to test (e.g. : https://www.chanel.com/fr/, chanel.com) : ')

browser = Browser()

title = get_domain_title(domain, browser)
print(f"""
The title found is "{title}".
""")

dorks_results = get_dorks_link(title=title)

related_domains = get_related_domain_names(domain)

all_domains = related_domains + dorks_results

domains_object_list = []
sleep(20)
for current_domain in all_domains:
    domain_object = get_domain_informations(current_domain, browser)
    domains_object_list.append(domain_object)
browser.kill()

report_generation(domains_object_list)
