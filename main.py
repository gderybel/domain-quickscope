from DorksLinks import get_dorks_link
from DomainInformations import get_domain_title


domain = input('Enter the webpage to test (e.g. : https://www.chanel.com/fr/) : ')

title = get_domain_title(domain=domain)
print(f"""
The title found is "{title}".
""")

link_results = get_dorks_link(title=title)
for link in link_results:
    print(link)
