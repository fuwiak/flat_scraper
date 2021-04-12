import yaml
import logging
import scrapy
import psycopg2

from scraping_ads import add_flat
from update_flat_info import check_if_row_exists, check_if_price_changed, \
                             update_price
from utils import get_ad_price, get_page_address, info_scraped_today, \
                  get_next_page, get_page_info, check_rent_buy

logging.getLogger('scrapy').setLevel(logging.WARNING)

with open(r'config.yaml') as f:
    params = yaml.load(f, Loader=yaml.FullLoader)


class FlatSpider(scrapy.Spider):
    name = "flat_spider"

    start_urls = params["start_urls"]

    def parse(self, response):
        i = 1
        try:
            conn = psycopg2.connect(
                'postgresql://postgres:mab@localhost:5432/flats_database')
            cursor = conn.cursor()
        except psycopg2.Error:
            raise Exception

        for flat_ad in response.css('div.tileV1'):
            print("\n" + "-"*100 + " " + str(i))
            i += 1

            page_address = get_page_address(flat_ad)
            table_f, table_p = check_rent_buy(page_address)
            ad_price = get_ad_price(flat_ad)
            ad_id = page_address.split('/')[-1][3:12]

            if check_if_row_exists(cursor, ad_id, table_f):
                if check_if_price_changed(cursor, ad_id, ad_price, table_p):
                    update_price(cursor, ad_id, ad_price, conn, table_p)
            else:
                add_flat(page_address, cursor, conn)
        try:
            next_page = get_next_page(response)
            get_page_info(next_page)
            conn.close()

            if next_page is not None:
                yield response.follow(next_page, self.parse)

        except KeyError:
            print(info_scraped_today(cursor))
            print("Reached 50th page.")
