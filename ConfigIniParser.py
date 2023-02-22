from configparser import ConfigParser

def parse_credentials(config_file = "config.ini"):
    """
    Parse credentials to authenticate with Google API.
    """
    config = ConfigParser()

    config.read(config_file)

    API_KEY = config["Keys"]["api_key"]
    SEARCH_ENGINE_ID = config["Keys"]["search_engine_id"]

    return API_KEY, SEARCH_ENGINE_ID
