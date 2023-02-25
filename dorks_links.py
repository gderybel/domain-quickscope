from urllib.parse import quote
from requests import get
from config_parser import parse_credentials

def get_dorks_links(title: str) -> list[dict]:
    """This function will find every website that have the same title than 
    the given one. It uses Google Dorks with Google API.

    I use Google API, because, some captcha might appears, which is blocking.
    Also, a Too Many Requests exception is thrown when using request & bs4.

    This API is limiting at 100 requests per day.

    Parameters
    ----------
    title : str
        Title to look for

    Returns
    -------
    list[dict]
        List of links found based on Google Dorks
    """
    api_key, search_engine_id = parse_credentials()

    print("Executing google dorks...\n")

    if title == "":
        return None

    query = quote(f"allintitle:\"{title}\"")
    num = 10
    start = 1

    dorks_links = []

    while True:
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&num={num}&start={start}"

        response = get(url, timeout=5)

        data = response.json()
        if 'error' in data and data['error']['message'] == 'API key not valid. Please pass a valid API key.':
            exit("The given API key is not known.")

        if 'items' in data:
            for item in data['items']:
                dorks_links.append({'domain':item['link'], 'method':'dorks'})
            start+=num
        else:
            break

    print(f"{len(dorks_links)} link(s) was/were found using the same title.\n")

    return dorks_links
