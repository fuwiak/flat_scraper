from utils import today_str


def check_if_row_exists(cursor, ad_id, table_f):
    cursor.execute(f'SELECT ad_id FROM {table_f} WHERE ad_id = {ad_id}')
    try:
        ad_id = cursor.fetchone()[0]
        print(f"Ad {ad_id} found in the database.")
        return True
    except TypeError:
        print(f"{ad_id} not found in the database.")
        return False


def check_if_price_changed(cursor, ad_id, ad_price, table_p):
    """
    Check if the price from the website is the same as the latest price
    from the database
    """
    cursor.execute(f'SELECT price FROM {table_p} '
                   f'WHERE flat_id = {ad_id} '
                   f'ORDER BY date DESC, price_id DESC '
                   f'LIMIT 1')
    old_price = cursor.fetchone()[0]

    if int(old_price) != int(ad_price):
        print(f"Price has changed {old_price} -> {ad_price}")
        return True
    else:
        print("Price is still the same.")
        return False


def update_price(cursor, ad_id, ad_price, conn, table_p):
    today = today_str()
    cursor.execute(f"INSERT INTO {table_p} VALUES("
                   "NULL, "
                   f"{ad_id}, "
                   f"{ad_price}, "
                   f"\'{today}\' "
                   ")")
    conn.commit()
