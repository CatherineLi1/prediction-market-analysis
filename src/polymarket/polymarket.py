import re
import time
import requests

GAMMA_BASE = "https://gamma-api.polymarket.com"
DATA_BASE  = "https://data-api.polymarket.com"

def event_slug_from_url(url: str) -> str:
    """
    Accepts:
      https://polymarket.com/event/<event-slug>
      https://polymarket.com/event/<event-slug>/...
    """
    m = re.search(r"polymarket\.com/event/([^/?#]+)", url)
    if not m:
        raise ValueError("Could not parse event slug from URL.")
    return m.group(1)

def get_event_by_slug(slug: str) -> dict:
    # Docs: GET /events/slug/{slug}
    r = requests.get(f"{GAMMA_BASE}/events/slug/{slug}", timeout=30)
    r.raise_for_status()
    return r.json()

def fetch_all_trades_for_event(event_id: int, limit: int = 1000, sleep_s: float = 0.1) -> list[dict]:
    """
    Data API trades endpoint supports:
      /trades?eventId=<id>&limit=<n>&offset=<k>
    `limit` max is 10000 per docs; I default to 1000 for stability. :contentReference[oaicite:2]{index=2}
    """
    all_rows = []
    offset = 0

    while True:
        params = {
            "eventId": event_id,
            "limit": limit,
            "offset": offset,
            # Optional knobs:
            # "takerOnly": True,
            # "side": "BUY",
        }
        r = requests.get(f"{DATA_BASE}/trades", params=params, timeout=60)
        r.raise_for_status()
        batch = r.json()

        if not batch:
            break

        all_rows.extend(batch)
        offset += len(batch)

        # polite pacing (avoid rate limits)
        time.sleep(sleep_s)

    return all_rows

if __name__ == "__main__":
    url = "https://polymarket.com/event/2026-winter-olympics-most-gold-medals"
    slug = event_slug_from_url(url)
    event = get_event_by_slug(slug)

    # Gamma often returns id as an int or numeric string; normalize:
    event_id = int(event["id"])

    trades = fetch_all_trades_for_event(event_id=event_id, limit=1000)

    print(f"Event slug: {slug}")
    print(f"Event id:   {event_id}")
    print(f"Trades:     {len(trades)}")
    print("First trade keys:", list(trades[0].keys()) if trades else "No trades returned")

    # Save raw JSON
    import json
    with open(f"trades_event_{slug}.json", "w", encoding="utf-8") as f:
        json.dump(trades, f, ensure_ascii=False)

    print(f"Saved to trades_event_{slug}.json")
