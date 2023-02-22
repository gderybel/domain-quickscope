from time import sleep
from DorksLinks import get_dorks_link
from DomainInformations import get_domain_title, get_related_domain_names, get_screenshot
from Browser import Browser

domain = input('Enter the webpage to test (e.g. : https://www.chanel.com/fr/) : ')

title = get_domain_title(domain=domain)
print(f"""
The title found is "{title}".
""")

dorks_results = get_dorks_link(title=title)
for link in dorks_results:
    print(link)

related_domains = get_related_domain_names(domain)

all_domains = related_domains + dorks_results

sleep(20)
browser = Browser()
for current_domain in all_domains:
    if not current_domain.startswith('http'):
        current_domain = f"http://{current_domain}"
    get_screenshot(current_domain, browser)
browser.kill()
