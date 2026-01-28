# NOTE: This version for NFL Seas vs NE data retrieval from GAMMA API
import requests
import json


def get_condition_id(slug):
    with open(f"data/raw/gamma/{slug}.json", 'r') as f:
        data = json.load(f)
    condition_id = data[0]["conditionId"]
    return condition_id

def save_raw_clob_data(slug, condition_id):
    response = requests.get(
        "https://data-api.polymarket.com/trades",
        params={
            "market": condition_id,
            "limit": 1000
        },
        timeout=30
    )
    result = response.json()
    with open(f"data/raw/clob/{slug}.json", "w") as f:
        json.dump(result, f, indent=2)


if __name__=="__main__":
    webpage_url = "https://polymarket.com/sports/nfl/games/week/15/nfl-sea-ne-2026-02-08"
    slug = webpage_url.split('/')[-1]

    condition_id = get_condition_id(slug)
    raw = save_raw_clob_data(slug, condition_id)    
