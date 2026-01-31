# NOTE: This version for NFL Seas vs NE data retrieval from GAMMA API
import requests
import json
import pandas as pd


def save_raw_gamma_data(mkt_event, slug):
    response = requests.get(
        f"https://gamma-api.polymarket.com/{mkt_event}",
        params={"slug": slug},
        timeout=30
    )
    data = response.json()
    with open(f"data/raw/gamma/{slug}.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__=="__main__":
    webpage_url = "https://polymarket.com/event/who-will-trump-nominate-as-fed-chair"
    mkt_event = "events"

    # webpage_url = "https://polymarket.com/sports/nfl/games/week/15/nfl-sea-ne-2026-02-08"
    # mkt_event = "markets"
    
    slug = webpage_url.split('/')[-1]
    save_raw_gamma_data(mkt_event, slug)
    