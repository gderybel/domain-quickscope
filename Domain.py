from datetime import datetime

class Domain:
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
        screenshot: str
    ):
        self.name = name
        self.url = url if url.startswith('http') else f"http://{url}"
        self.organization = organization
        self.registrar = registrar
        self.creation_date = creation_date
        self.update_date = update_date
        self.expiration_date = expiration_date
        self.emails = ', '.join(emails) if isinstance(emails, list) else emails
        self.country = country
        self.screenshot = screenshot
