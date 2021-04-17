import yaml
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

from project.src.analysis.utils import load_df_to_csv


def main():

    df = pd.read_csv('./data/flats_rent.csv')

    plt.hist(df['area_category'])
    plt.savefig("mygraph.png")


if __name__ == "__main__":
    # load_df_to_csv()
    main()
