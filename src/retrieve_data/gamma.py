# NOTE: This version for NFL Seas vs NE data retrieval from GAMMA API
import requests
import json
import pandas as pd


def save_raw_data(mkt_event, slug):
    response = requests.get(
        f"https://gamma-api.polymarket.com/{mkt_event}",
        params={"slug": slug},
        timeout=30
    )
    data = response.json()
    with open(f"data/raw/{slug}.json", "w") as f:
        json.dump(data, f, indent=2)
    return data

def save_processing_data(data_events, data, slug):
    if data_events=="markets":
        df = pd.DataFrame(data[0][data_events])
        columns = ["id","conditionId","liquidity","outcomes","outcomePrices","volume",
               "groupItemTitle","questionID","volumeNum","liquidityNum","clobTokenIds"]
    else:
        df = pd.DataFrame(data[0])
        columns = ["id","conditionId","liquidity","outcomes","outcomePrices","volume",
                "questionID","volumeNum","liquidityNum","clobTokenIds"]
    df[columns].to_csv(f"data/processing/{slug}.csv", index=False)


if __name__=="__main__":
    # webpage_url = "https://polymarket.com/event/who-will-trump-nominate-as-fed-chair"
    # mkt_event = "events"
    # data_events = "markets"

    webpage_url = "https://polymarket.com/sports/nfl/games/week/15/nfl-sea-ne-2026-02-08"
    mkt_event = "markets"
    data_events = "events"
    
    slug = webpage_url.split('/')[-1]
    data = save_raw_data(mkt_event, slug)
    save_processing_data(data_events, data, slug)

    