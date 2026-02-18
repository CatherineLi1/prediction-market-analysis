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
        df_c["Duration"] = c.split('.')[0]
        if df.empty:
            df = df_c
            continue
        df = pd.concat([df, df_c], axis=0)
    df = df.reset_index(drop=True)
    df.sort_values("time_utc").to_csv(f"{path}/combined.csv", index=False)
    return df

def prep_graphing_data(df):
    n = 10
    top_n_nominees = df.groupby("Duration")['p'].sum().nlargest(n).index.to_list()
    df = df[df["Duration"].isin(top_n_nominees)]
    df.sort_values("time_utc", inplace=True)
    return df

def graph_history(df, slug):
    plt.figure(figsize=(12,6))
    for team in df["Duration"].unique():
        df_n = df[df["Duration"]==team]
        plt.plot(pd.to_datetime(df_n["time_utc"]), df_n["p"], label=team)
    plt.xlabel("Date")
    plt.ylabel("Probability")
    plt.title(' '.join(slug.split('-')).title())
    plt.legend()
    os.makedirs(f"results/{slug}", exist_ok=True)
    plt.savefig(f"results/{slug}/History.png")

def graph_history_area(df, slug):
    df_graph = df.pivot(index="time_utc", columns="Duration", values="p").reset_index()
    
    df_graph = df_graph.sort_values(by="time_utc").set_index("time_utc")
    # .fillna(method="ffill").set_index("time_utc")
    

    a,b,c,d,e,f,g = df_graph['No Handshake'],df_graph["Photographed only"],df_graph['under2s'],df_graph['2–6s'],df_graph['6–10s'],df_graph['10–15s'],df_graph['15s+']
    plt.figure(figsize=(12,6))
    plt.stackplot(a,b,c,d,e,f,g, labels=df["Duration"].unique())
    plt.xlabel("Date")
    plt.ylabel("Probability")
    plt.title(' '.join(slug.split('-')).title())
    plt.legend()
    os.makedirs(f"results/{slug}", exist_ok=True)
    plt.savefig(f"results/{slug}/ProbabilityStackPlot.png")


if __name__=="__main__":
    webpage_url = "https://polymarket.com/event/how-long-will-trump-and-netanyahu-shake-hands-for-when-they-meet"
    slug = webpage_url.split('/')[-1]
    
    if os.path.exists(f"data/clean/{slug}/combined.csv"): 
        df = pd.read_csv(f"data/clean/{slug}/combined.csv", parse_dates=["time_utc"])
    else:
        df = combine_historical_data(slug)

    df = prep_graphing_data(df)
    # graph_history(df, slug)
    graph_history_area(df, slug)
