from datetime import datetime

class Domain:
    """ 
        This class represent a Domain object with every whois informations
    """
    def __init__(
        self,
        name: str,
        url: str,
        organization: str,
        registrar: str,
        creation_date: datetime,
        update_date: datetime,
        expiration_date: datetime,
        emails: list,
        country: str,
        screenshot: str,
        method: str,
        similarity
    ):
        self.name = name
        self.url = url if url.startswith('http') else f"http://{url}"
        self.organization = organization
        self.registrar = registrar
        self.creation_date = creation_date if isinstance(creation_date, datetime) else None
        self.update_date = update_date if isinstance(update_date, datetime) else None
        self.expiration_date = expiration_date if isinstance(expiration_date, datetime) else None
        self.emails = ', '.join(emails) if isinstance(emails, list) else emails
        self.country = country
        self.screenshot = screenshot
        self.method = method
        self.similarity = similarity
