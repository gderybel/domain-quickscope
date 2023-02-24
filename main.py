from DorksLinks import get_dorks_link
from DomainInformations import get_domain_title, get_related_domain_names, get_domain_informations
from Browser import Browser
from ReportGenerator import report_generation

domain = input('Enter a domain or a webpage to test (e.g. : chanel.com) : ')

browser = Browser()

title = get_domain_title(domain, browser)
print(f"""
The title found is "{title}".
""")

dorks_results = get_dorks_link(title=title)

related_domains = get_related_domain_names(domain)

all_domains = related_domains + dorks_results

domains_object_list = []
count = 0
for current_domain in all_domains:
    count +=1
    print(f"Fetching {current_domain}... {count}/{len(all_domains)}", end="\r")
    domain_object = get_domain_informations(current_domain, browser)
    if domain_object:
        domains_object_list.append(domain_object)
browser.kill()

report_generation(domains_object_list)
