import requests

from bs4 import BeautifulSoup


def get_url_title_and_description(url: str) -> tuple[str, str]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string

        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag.get('content') if description_tag else "No description available"

        return title, description
    except requests.exceptions.RequestException as e:
        print(e)
        return "No title available", "No description available"
