from collections import Counter
import pandas as pd
import streamlit as st

"""

1)@st.cache do czego to sluzy?
2) dlaczego nie ma kodu w funkcjach
3) Trzymajmy sie jakies conwencji :https://github.com/fuwiak/faster_ds/tree/master/info_for_dev
4) type hinting https://realpython.com/lessons/type-hinting/
5) conwecja komitow

"""


@st.cache
def load_data():
    return pd.read_csv('project/src/analysis/data/flats_rent.csv')


df_flats = load_data()

df_flats['month'] = df_flats['date'].apply(lambda x: x.split('-')[1])
df_flats = df_flats[df_flats['flat_area'] > 0]

st.title("Small flats for rent in Poland")

date_first = min(df_flats['date_scraped'])
date_last = max(df_flats['date_scraped'])
st.write(f"Ads scraped between {date_first} and {date_last}")
st.write(f"We have {len(df_flats)} unique flats")

count_area = Counter(df_flats["area_category"])
df_flats['count'] = 1

st.subheader('Number of flats per size')
filter_data = df_flats[['area_category', 'count']]
filter_data = filter_data.set_index("area_category")
st.bar_chart(filter_data[['count']])


list_districts = list(set(df_flats['location']))
list_districts.append("All locations")


district = st.selectbox('Which location do you want to see', list_districts)

if district != 'All locations':
    st.write(df_flats[df_flats['location'] == district])


st.subheader("Smallest flats (less than 20 metres)")
smallest = df_flats[df_flats['area_category'] == "less20"]
st.write(smallest[["title", "location", "flat_area", "price", "price_per_m"]])


st.subheader("Historia zmian cen mieszkań")
area_cat_list = list(set(df_flats['area_category']))
area = st.selectbox('How big should the flat be', area_cat_list)

pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('precision', 2)

if district != 'all':
    grouped_df = df_flats[df_flats['area_category'] == area]

    grouped_df = grouped_df[['location', 'month', 'price_per_m']]
    grouped_df = grouped_df.groupby(['location', 'month'])['price_per_m'].mean().astype(int)
    st.table(grouped_df)
