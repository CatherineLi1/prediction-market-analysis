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
        df_c["Team"] = c.split('.')[0]
        if df.empty:
            df = df_c
            continue
        df = pd.concat([df, df_c], axis=0)
    df = df.reset_index(drop=True)
    df.sort_values("time_utc").to_csv(f"{path}/combined.csv", index=False)
    return df

def prep_graphing_data(df):
    top5_nominees = df.groupby("Team")['p'].sum().nlargest(5).index.to_list()
    df = df[df["Team"].isin(top5_nominees)]
    df.sort_values("time_utc", inplace=True)
    return df

def graph_history(df, slug):
    plt.figure(figsize=(12,6))
    for team in df["Team"].unique():
        df_n = df[df["Team"]==team]
        plt.plot(pd.to_datetime(df_n["time_utc"]), df_n["p"], label=team)
    plt.xlabel("Date")
    plt.ylabel("Probability")
    plt.title(' '.join(slug.split('-')).title())
    plt.legend()
    os.makedirs(f"results/{slug}", exist_ok=True)
    plt.savefig(f"results/{slug}/History.png")

def graph_history_area(df, slug):
    df_graph = df.pivot(index="time_utc", columns="Team", values="p").reset_index()

    plt.figure(figsize=(12,6))
    plt.stackplot(df_graph["time_utc"], df_graph["Patriots"], df_graph["Seahawks"], labels=df["Team"].unique())
    plt.xlabel("Date")
    plt.ylabel("Probability")
    plt.title(' '.join(slug.split('-')).title())
    plt.legend()
    os.makedirs(f"results/{slug}", exist_ok=True)
    plt.savefig(f"results/{slug}/ProbabilityStackPlot.png")

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
    webpage_url = "https://polymarket.com/sports/nfl/games/week/15/nfl-sea-ne-2026-02-08"
    slug = webpage_url.split('/')[-1]
    
    if os.path.exists(f"data/clean/{slug}/combined.csv"): 
        df = pd.read_csv(f"data/clean/{slug}/combined.csv")
    else:
        df = combine_historical_data(slug)

    df = prep_graphing_data(df)
    graph_history(df, slug)
    graph_history_area(df, slug) # Not implemented
    # graph_jan302026(df, slug)
