# Market
# Get reference token IDs

import requests
import json


def fetch_markets(url):
    params = {
        "active": "true",
        "closed": "false",
        "limit": 100,
    }
    response = requests.get(url, params=params)
    print(response)
    data = response.json()
    return data

def save_raw_data(data, slug):
    with open(f"data/raw/gamma/{slug}.json", "w") as f:
        json.dump(data, f, indent=2)



if __name__ == "__main__":

    # Change this as needed
    # webpage_url = "https://polymarket.com/event/fed-decision-in-january"
    # webpage_url = "https://polymarket.com/event/ecb-interest-rates-february-2026"
    webpage_url = "https://polymarket.com/sports/nfl/games/week/15/nfl-sea-ne-2026-02-08"

    slug = webpage_url.split('/')[-1]
    url = f"https://gamma-api.polymarket.com/events/slug/{slug}"

    # Fetch data
    data = fetch_markets(url)
    print(True)
    save_raw_data(data, slug)
