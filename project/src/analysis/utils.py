import yaml
import psycopg2
import pandas as pd


def load_df_to_csv():
    with open(r'../scraper/config.yaml') as f:
        params = yaml.load(f, Loader=yaml.FullLoader)

    try:
        postgres_setup = params["postgres_setup"]
        conn = psycopg2.connect(postgres_setup)
    except psycopg2.Error:
        raise Exception

    df_to_merge = ("SELECT * "
                   "FROM prices_rent "
                   "WHERE price_id in (SELECT max(price_id) "
                   "FROM prices_rent "
                   "GROUP BY flat_id)")

    df = pd.read_sql_query(
        "SELECT * ,"
        "CASE "
        "     WHEN flat_area <= 20 THEN 'less20' "
        "     WHEN flat_area <= 30 THEN '20_30' "
        "     WHEN flat_area <= 40 THEN '30_40' "
        "     ELSE 'more40' "
        "END as area_category, "
        "CASE "
        "     WHEN flat_area <= 27 THEN 'Yes' "
        "     ELSE 'No' "
        "END as small_flat, "
        "CAST(ROUND(prices.price/flat_area,2) as decimal(10,2)) as price_per_m "
        "FROM flats_rent "
        f"INNER JOIN ({df_to_merge}) as prices "
        "ON flats_rent.ad_id = prices.flat_id "
        "WHERE flat_area > 0",
        conn)

    assert len(df) > 0, "No data loaded from the database"

    df.to_csv('./data/flats_rent.csv')
