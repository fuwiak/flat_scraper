import requests
import re
import psycopg2
from bs4 import BeautifulSoup

from utils import today_str


def get_price(soup) -> int:
    '''Extracts price of the flat'''
    try:
        results = soup.find('div', class_="vip-title clearfix")
        price = results.find('span', class_='amount')
        return int(re.sub("[^\d\.,]", "", price.text))
    except AttributeError or ValueError:
        return 0


def get_description(soup) -> str:
    '''Extracts description of the flat'''
    try:
        results = soup.find(id="wrapper")
        description = results.find('span', class_='pre')
        description = description.text.replace('\"', '\'').replace('\\', '')
        return description
    except AttributeError or ValueError:
        return 'NA'


def get_add_title(soup) -> str:
    '''Extracts title of the ad'''
    results = soup.find('div', class_="vip-title clearfix")
    title = results.find('span', class_='myAdTitle').text.replace('\'', '')
    return title


def extract_num_rooms(text: str) -> int:
    '''Extracting number of rooms and looking for word "Kawalerka" == studio'''
    if "Kawalerka" in text:
        return 1
    return int(re.sub("[^\d]", "", text))


def change_date_str(text: str) -> str:
    '''
    Changing date format for more efficient sorting
    from dd/mm/yyyy to yyyy-mm-dd
    '''
    dd,mm,yyyy = text.split('/')
    return f"{yyyy}-{mm}-{dd}"


def get_attributes(soup) -> dict:
    '''Other attributes are optional to fill out. This function gathers them'''
    results = soup.find(id="wrapper")
    attributes = results.find('ul', class_='selMenu')
    attributes_all = attributes.find_all('div', class_='attribute')

    attr_dict = {}

    for elem in attributes_all:

        attr_name = (elem.find('span', class_='name')).text
        attr_val = (elem.find('span', class_='value')).text

        if attr_name not in attr_dict:
            if attr_name in ['Liczba pokoi', 'Liczba łazienek']:
                attr_val = extract_num_rooms(attr_val)
            if attr_name == 'Data dodania':
                attr_val = change_date_str(attr_val)
            attr_dict[attr_name] = attr_val

    return attr_dict


keys_dict = {
    'Data dodania': 'date_posted',
    'Lokalizacja': 'location',
    'Na sprzedaż przez': 'seller',
    'Rodzaj nieruchomości': 'property_type',
    'Liczba pokoi': 'num_rooms',
    'Liczba łazienek': 'num_bathrooms',
    'Wielkość (m2)': 'flat_area',
    'Parking': 'parking',
    'Palący': 'smoking',
    'Przyjazne zwierzakom': 'animals'}


def get_flat_info(page_address) -> dict:
    page = requests.get(page_address)
    soup = BeautifulSoup(page.content, 'html.parser')

    ad_id = page_address.split('/')[-1][3:12]
    price = get_price(soup)
    title = get_add_title(soup)
    today = today_str()
    description = get_description(soup)

    flat = {'ad_id': ad_id,
            'title': title,
            'date_posted': 'NA',
            'date_scraped': today,
            'location': 'NA',
            'price': price,
            'seller': 'NA',
            'property_type': 'NA',
            'num_rooms': 0,
            'num_bathrooms': 1,
            'flat_area': 0,
            'parking': 'Brak',
            'description': description,
            'page_address': page_address,
            'smoking': 'NA',
            'animals': 'NA'
            }

    attributes = get_attributes(soup)

    for key, value in attributes.items():
        if key in keys_dict:
            key = keys_dict[key]
            flat[key] = value

    return flat


def add_flat(page_address, cursor, conn):
    print("Adding a new flat")
    flat = get_flat_info(page_address)

    if "do-wynajecia" in page_address:
        table_flats = "flats_rent"
        table_prices = "prices_rent"
        if_rent = f",\'{flat['smoking']}\', \'{flat['animals']}\'"
    elif "sprzedam-i-kupie" in page_address:
        table_flats = "flats_buy"
        table_prices = "prices_buy"
        if_rent = ""

    input_flat = (f"INSERT INTO {table_flats} VALUES ("
                  f"{flat['ad_id']}, "
                  f"\'{flat['title']}\', "
                  f"\'{flat['date_posted']}\', "
                  f"\'{flat['date_scraped']}\', "
                  f"\'{flat['location']}\', "
                  f"\'{flat['seller']}\', "
                  f"\'{flat['property_type']}\', "
                  f"{flat['num_rooms']}, "
                  f"{flat['num_bathrooms']}, "
                  f"{flat['flat_area']}, "
                  f"\'{flat['parking']}\', "
                  f"\'{flat['description']}\', "
                  f"\'{flat['page_address']}\' "
                  f"{if_rent}"
                  ")")
    cursor.execute(input_flat)
    conn.commit()

    input_price = (f"INSERT INTO {table_prices} (flat_id, price, date) "
                   f"VALUES("
                   f"{flat['ad_id']}, "
                   f"{flat['price']}, "
                   f"\'{flat['date_scraped']}\' "
                   ")")

    cursor.execute(input_price)
    conn.commit()


if __name__ == "__main__":
    try:
        conn = psycopg2.connect('postgresql://postgres:mab@localhost:5432/flats_database')
        cursor = conn.cursor()
    except psycopg2.Error as e:
        raise Exception

    # ad_link = 'https://www.gumtree.pl/a-mieszkania-i-domy-do-wynajecia/krakow/2-pokoje-mieszkanie-krakow-osiedle-na-lotnisku-16-wysokie-broniewskiego-bienczyce-bez-prowizji/1009105174600911318987609'
    ad_link = 'https://www.gumtree.pl/a-mieszkania-i-domy-sprzedam-i-kupie/krakow/mieszkanie-krakow-stare-miasto-75m2-nr-spek+ms+1353+1/1009184789870912121700109'

    flat_example = get_flat_info(ad_link)
    print(flat_example)

    add_flat(ad_link, cursor, conn)


