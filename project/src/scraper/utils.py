import re
from datetime import datetime


def today_str():
    return datetime.today().strftime('%Y-%m-%d')


def info_scraped_today(cursor):
    """Print how many ads were scraped today
    and how many there are in the whole database"""
    today = today_str()
    cursor.execute(f"SELECT count(*) FROM flats WHERE date_scraped = '{today}'")
    ads_today = cursor.fetchone()[0]

    cursor.execute(f"SELECT count(*) FROM flats")
    all_ads = cursor.fetchone()[0]

    cursor.execute(f"SELECT count(flat_id) FROM prices "
                   f"WHERE flat_id in (SELECT flat_id "
                                       f"FROM prices "
                                       f"GROUP BY flat_id "
                                       f"HAVING count(flat_id) => 2) "
                   f"and date = '{today}' ")
    price_changes = cursor.fetchone()[0]

    print("_"*100)
    return(f"\n\tNew ads today: {ads_today:,}\n"
           f"\tOverall: {all_ads:,}\n"
           f"\tPrice changes today: {price_changes}\n")


def get_ad_price(flat):
    price = flat.css('span.ad-price::text').get()
    price = re.sub("[^\d\.,]", "", price)
    return price


def get_page_address(flat):
    address = flat.css('a::attr("href")').get()
    address = f'https://www.gumtree.pl{address}'
    return address


def get_page_info(next_page: str) -> None:
    """Print page number and which district we are scraping now"""
    page = re.findall(r"page-\d+", next_page)[0]
    page_num = page.split('-')[-1]
    district = next_page.split('/')[2].upper()

    print(f"\n\n{' '*15}({district} | NEXT PAGE: {page_num}){' '*15}\n")


def get_next_page(response):
    next_page = response.css('a.arrows.icon-right-arrow.icon-angle-right-gray').attrib['href']
    return next_page


def check_rent_buy(page_address):
    if "do-wynajecia" in page_address:
        return ["flats_rent", "prices_rent"]
    elif "sprzedam-i-kupie" in page_address:
        return ["flats_buy", "prices_buy"]

