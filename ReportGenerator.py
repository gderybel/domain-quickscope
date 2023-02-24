from datetime import datetime

def report_generation(domains :list):
    """
        This function will generate a report showing every similar
        websites based on Dorks and similar domain names.

        The output will be in HTML and will contains the following content :
        - URL
        - Title
        - Screenshot
        - Whois informations, with relevent indicators
    """
    HEAD = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Domain Report</title>
    <style>
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
            background-color: #f9f9f9;
        }

        .card {
        display: flex;
        flex-wrap: wrap;
        width: fit-content;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        margin-left: auto;
        margin-right: auto;
        margin-top: 20px;
        }

        .card div {
            margin: 20px;
        }

        .image-container {
        display: flex;
        justify-content: right;
        max-width: 500px;
        }

        .image-container img {
        width: 100%;
        border-radius: 5px;
        }

        .content {
        margin: auto;
        }

        .content h2 {
        font-size: 24px;
        margin-bottom: 10px;
        }

        .content ul {
        list-style: none;
        margin: 0;
        padding: 0;
        }

        .content li {
        margin-bottom: 5px;
        }
    </style>
  </head>

  <body>
    """

    TAIL = """
  </body>
</html>"""

    full_content = ""
    for domain in domains:
        content = f"""
        <div class="card">
        <div class="image-container">
            <img src="{domain.screenshot}" alt="card image">
        </div>
        <div class="content">
        <h2>{domain.name}</h2>
            <ul>
                <li><strong>URL:</strong> <a href="{domain.url}">{domain.url}</a></li>
                <li><strong>Organization:</strong> {domain.organization}</li>
                <li><strong>Registrar:</strong> {domain.registrar}</li>
                <li><strong>Creation date:</strong> {domain.creation_date}</li>
                <li><strong>Update date:</strong> {domain.update_date}</li>
                <li><strong>Expiration date:</strong> {domain.expiration_date}</li>
                <li><strong>Emails:</strong> {domain.emails}</li>
                <li><strong>Country:</strong> {domain.country}</li>
            </ul>
        </div>
    </div>
        """
        full_content += content

    current_time = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    with open(f"domain_report_{current_time}.html", 'w', encoding='UTF-8') as file:
        file.write(HEAD)
        file.write(full_content)
        file.write(TAIL)
