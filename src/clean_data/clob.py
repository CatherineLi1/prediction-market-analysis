import json
import pandas as pd


def read_json_to_df(slug):
    with open(f"data/raw/clob/{slug}.json", "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df


def clean_data(df):
    columns_keep = ['timestamp', 'size', 'price', 'outcome', 'outcomeIndex']
    df = df[columns_keep]
    df["time_utc"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
    df["time_est"] = df["time_utc"].dt.tz_convert("US/Eastern")
    df[["time_est"]+columns_keep[1:]].to_csv(f"data/clean/{slug}.csv", index=False)


if __name__=="__main__":
    webpage_url = "https://polymarket.com/sports/nfl/games/week/15/nfl-sea-ne-2026-02-08"
    slug = webpage_url.split('/')[-1]

    df = read_json_to_df(slug)
    clean_data(df)
