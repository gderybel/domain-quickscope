import requests
from urllib.parse import quote
from ConfigIniParser import parse_credentials

def get_dorks_link(title: str):
    """
        This function will find every website that have the same title than 
        the given one. It uses Google Dorks with Google API.

        I use Google API, because, some captcha might appears, which is blocking.
        Also, a Too Many Requests exception is thrown when using request & bs4.
    """
    API_KEY, SEARCH_ENGINE_ID = parse_credentials()

    query = quote(f"allintitle:\"{title}\"")
    num = 10
    start = 1

    dorks_links = []

    while True:
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&num={num}&start={start}"

        response = requests.get(url, timeout=5)

        data = response.json()

        if 'items' in data:
            for item in data['items']:
                dorks_links.append(item['link'])
            start+=num
        else:
            break

    print(f"{len(dorks_links)} was/were found using the same title.")

    return dorks_links