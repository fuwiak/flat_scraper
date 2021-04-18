import re
from datetime import datetime


def today_str():
    return datetime.today().strftime('%Y-%m-%d')


def info_scraped_today(cursor):
    """Print how many ads were scraped today
    and how many there are in the whole database"""
    today = today_str()

    def query_flats_stats(table):
        cursor.execute(f"SELECT count(*) "
                       f"FROM {table} "
                       f"WHERE date_scraped = '{today}'")
        return cursor.fetchone()[0]

    def query_price_changes(table):
        cursor.execute(f"SELECT count(flat_id) FROM {table} "
                       f"WHERE flat_id in ("
                            f"SELECT flat_id "
                            f"FROM {table} "
                            f"GROUP BY flat_id "
                            f"HAVING count(flat_id) >= 2) "
                       f"and date = '{today}' ")
        return cursor.fetchone()[0]

    def get_all_ads(table):
        cursor.execute(f"SELECT count(*) FROM {table}")
        return cursor.fetchone()[0]

    ads_today_buy = query_flats_stats('flats_buy')
    ads_today_rent = query_flats_stats('flats_rent')

    price_changes_buy = query_price_changes('prices_buy')
    price_changes_rent = query_price_changes('prices_rent')

    all_ads_buy = get_all_ads('prices_buy')
    all_ads_rent = get_all_ads('prices_rent')

    print("_"*100)
    return(f"\n\tNew ads today (buy): {ads_today_buy:,}\n"
           f"\tPrice changes today (buy): {price_changes_buy}\n"
           f"\tOverall (buy): {all_ads_buy:,}\n"
           "\n"
           f"\n\tNew ads today (rent): {ads_today_rent:,}\n"
           f"\tPrice changes today (rent): {price_changes_rent}\n"
           f"\tOverall (rent): {all_ads_rent:,}\n")


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

