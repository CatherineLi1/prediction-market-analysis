import datetime as dt
import pandas as pd
import os
import matplotlib.pyplot as plt


def combine_historical_data(slug):
    path = f"data/clean/{slug}"
    candidates = [name for name in os.listdir(path)]
    df = pd.DataFrame()
    for c in candidates:
        if c=="combined.csv": continue
        df_c = pd.read_csv(f"{path}/{c}")
        df_c = df_c[["time_utc", "p"]]
        df_c["Nominee"] = c.split('.')[0]
        if df.empty:
            df = df_c
            continue
        df = pd.concat([df, df_c], axis=0)
    df = df.reset_index(drop=True)
    df.sort_values("time_utc").to_csv(f"{path}/combined.csv", index=False)
    return df

def prep_graphing_data(df):
    top5_nominees = df.groupby("Nominee")['p'].sum().nlargest(5).index.to_list()
    df = df[df["Nominee"].isin(top5_nominees)]
    df.sort_values("time_utc", inplace=True)
    return df

def graph_history(df, slug):
    plt.figure(figsize=(12,6))
    for nominee in df["Nominee"].unique():
        df_n = df[df["Nominee"]==nominee]
        plt.plot(pd.to_datetime(df_n["time_utc"]), df_n["p"], label=nominee)
    plt.xlabel("Date")
    plt.ylabel("Probability")
    plt.title(' '.join(slug.split('-')).title())
    plt.legend()
    os.makedirs(f"results/{slug}", exist_ok=True)
    plt.savefig(f"results/{slug}/History.png")

def graph_history_area(df, slug):
    pass

def graph_jan2026(df, slug):
    plt.figure(figsize=(12,6))
    jan2026_start = dt.datetime(2026,1,1)
    jan2026_end = dt.datetime(2026,1,31)
    df_jan2026 = df[(pd.to_datetime(df["time_utc"]) >= jan2026_start) & (pd.to_datetime(df["time_utc"]) <= jan2026_end)]
    for nominee in df_jan2026["Nominee"].unique():
        df_n = df_jan2026[df_jan2026["Nominee"]==nominee]
        plt.plot(pd.to_datetime(df_n["time_utc"]), df_n["p"], label=nominee)
    
    # First spike - Trump: Keep Hassett as is
    v1 = pd.to_datetime("2026-01-16 16:00:00", utc=True)
    plt.axvline(v1, linestyle=":", color="red", alpha=0.5) # label=""
    plt.text(v1-pd.Timedelta(days=6), plt.ylim()[1] - 0.05, "Trump: Keep Hassett as is", verticalalignment="top")

    # Second spike - Trump: Nominate Warsh
    v2 = pd.to_datetime("2026-01-30 12:25:00", utc=True) # 7:25am EST = 12:25pm UTC
    plt.axvline(v2, linestyle=":", color="red", alpha=0.5)
    plt.text(v2-pd.Timedelta(days=6), plt.ylim()[1] - 0.05, "Trump: Nominate Warsh", verticalalignment="top")

    plt.xlabel("Date")
    plt.ylabel("Probability")
    plt.title(' '.join(slug.split('-')).title() + " - January 2026")
    plt.legend()
    os.makedirs(f"results/{slug}", exist_ok=True)
    plt.savefig(f"results/{slug}/January2026.png")

def graph_jan302026(df, slug):
    plt.figure(figsize=(12,6))
    start = dt.datetime(2026,1,29)
    end = dt.datetime(2026,2,1)
    df_jan302026 = df[(pd.to_datetime(df["time_utc"]) >= start) & (pd.to_datetime(df["time_utc"]) <= end)]
    for nominee in df_jan302026["Nominee"].unique():
        df_n = df_jan302026[df_jan302026["Nominee"]==nominee]
        plt.plot(pd.to_datetime(df_n["time_utc"]), df_n["p"], label=nominee)
    
    # Trump: Nominate Warsh
    v2 = pd.to_datetime("2026-01-30 12:25:00", utc=True) # 7:25am EST = 12:25pm UTC
    plt.axvline(v2, linestyle=":", color="red", alpha=0.5)
    plt.text(v2-pd.Timedelta(hours=6), plt.ylim()[1] - 0.35, "Trump: Nominate Warsh", verticalalignment="top")

    plt.xlabel("Date")
    plt.ylabel("Probability")
    plt.title(' '.join(slug.split('-')).title() + " - January 30, 2026")
    plt.legend()
    os.makedirs(f"results/{slug}", exist_ok=True)
    plt.savefig(f"results/{slug}/January302026.png")


if __name__=="__main__":
    webpage_url = "https://polymarket.com/event/who-will-trump-nominate-as-fed-chair"
    slug = webpage_url.split('/')[-1]
    
    if os.path.exists(f"data/clean/{slug}/combined.csv"): 
        df = pd.read_csv(f"data/clean/{slug}/combined.csv")
    else:
        df = combine_historical_data(slug)

    df = prep_graphing_data(df)
    # graph_history(df, slug)
    graph_history_area(df, slug) # Not implemented
    # graph_jan2026(df, slug)
    # graph_jan302026(df, slug)
