from configparser import ConfigParser

def parse_credentials(config_file: str = "config.ini") -> tuple[str]:
    """Parse credentials to authenticate with Google API.

    Parameters
    ----------
    config_file : str, optional
        The config file location, by default "config.ini"

    Returns
    -------
    tuple[str]
        A tuple containing API key and the search engine ID
    """
    config = ConfigParser()

    config.read(config_file)

    api_key = config["Keys"]["api_key"]
    search_engine_id = config["Keys"]["search_engine_id"]

    return api_key, search_engine_id
