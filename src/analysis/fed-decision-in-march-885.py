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
        df_c["Decision"] = c.split('.')[0]
        if df.empty:
            df = df_c
            continue
        df = pd.concat([df, df_c], axis=0)
    df = df.reset_index(drop=True)
    df.sort_values("time_utc").to_csv(f"{path}/combined.csv", index=False)
    return df

def prep_graphing_data(df):
    top5_nominees = df.groupby("Decision")['p'].sum().nlargest(5).index.to_list()
    df = df[df["Decision"].isin(top5_nominees)]
    df.sort_values("time_utc", inplace=True)
    return df

def graph_history(df, slug):
    plt.figure(figsize=(12,6))
    for decision in df["Decision"].unique():
        df_n = df[df["Decision"]==decision]
        plt.plot(pd.to_datetime(df_n["time_utc"]), df_n["p"], label=decision)
    plt.xlabel("Date")
    plt.ylabel("Probability")
    plt.title(' '.join(slug.split('-')).title())
    plt.legend()
    os.makedirs(f"results/{slug}", exist_ok=True)
    plt.savefig(f"results/{slug}/History.png")

def graph_history_area(df, slug):
    df_graph = df.pivot(index="time_utc", columns="Decision", values="p").reset_index()

    bps25_down = df_graph["25 bps decrease"].iloc[1:]
    bps25_up = df_graph["25+ bps increase"].iloc[1:]
    bps50_down = df_graph["50+ bps decrease"].iloc[1:]
    no_change = df_graph["No change"].iloc[1:]
    plt.figure(figsize=(12,6))
    plt.stackplot(df_graph["time_utc"].iloc[1:], bps25_down, bps25_up, bps50_down, no_change, labels=df["Decision"].unique())
    plt.xlabel("Date")
    plt.ylabel("Probability")
    plt.title(' '.join(slug.split('-')).title())
    plt.legend()
    os.makedirs(f"results/{slug}", exist_ok=True)
    plt.savefig(f"results/{slug}/ProbabilityStackPlot.png")


if __name__=="__main__":
    webpage_url = "https://polymarket.com/event/fed-decision-in-march-885"
    slug = webpage_url.split('/')[-1]
    
    if os.path.exists(f"data/clean/{slug}/combined.csv"): 
        df = pd.read_csv(f"data/clean/{slug}/combined.csv")
    else:
        df = combine_historical_data(slug)

    df = prep_graphing_data(df)
    graph_history(df, slug)
    graph_history_area(df, slug) # Not implemented
    # graph_jan2026(df, slug)
    # graph_jan302026(df, slug)
