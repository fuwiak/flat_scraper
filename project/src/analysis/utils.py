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

    df_to_merge = (f"SELECT * "
                   f"FROM prices_rent "
                   f"WHERE price_id in (SELECT max(price_id) "
                   f"FROM prices_rent "
                   f"GROUP BY flat_id)")

    df = pd.read_sql_query(
        f"SELECT * ,"
        "CASE "
        "     WHEN flat_area <= 20 THEN 'less20' "
        "     WHEN flat_area <= 30 THEN '20_30' "
        "     WHEN flat_area <= 40 THEN '30_40' "
        "     ELSE 'more40' "
        "END as area_category "
        f"FROM flats_rent "
        f"INNER JOIN ({df_to_merge}) as prices "
        f"ON flats_rent.ad_id = prices.flat_id",
        conn)

    assert len(df) > 0, "No data loaded from the database"

    df.to_csv('./data/flats_rent.csv')
