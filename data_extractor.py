import requests
from bs4 import BeautifulSoup


def get_cases():
    page = requests.get('https://www.worldometers.info/coronavirus/')
    soup = BeautifulSoup(page.content, 'html.parser')

    total_table_row = [table_data.get_text() for table_data in soup.find('td', string='World').parent.findChildren('td')]
    total_name, total_cases, total_new, _, _, total_recovered, _, total_active = total_table_row[1:9]

    poland_table_row_tags = soup.find(lambda tag: tag.name in ('td', 'a') and 'Poland' in tag.text).parent.find_all('td')
    poland_table_row = [table_data.get_text() for table_data in poland_table_row_tags]

    poland_name, poland_cases, poland_new, _, _, poland_recovered, _, poland_active = poland_table_row[1:9]

    return {
        'World': {
            'name': total_name,
            'cases': total_cases,
            'new': total_new,
            'recovered': total_recovered,
            'active': total_active
        },
        'Poland': {
            'name': poland_name,
            'cases': poland_cases,
            'new': poland_new,
            'recovered': poland_recovered,
            'active': poland_active
        }
    }


if __name__ == '__main__':
    from pprint import pprint

    pprint(get_cases())
