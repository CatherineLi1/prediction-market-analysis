import requests
import pandas as pd

BASE = "https://api.elections.kalshi.com/trade-api/v2"

########
# TIME #
########
import time
end_ts = int(time.time())
start_ts = end_ts - 14 * 24 * 3600  # 7 days
params = {
    "start_ts": start_ts, # 1770973968,
    "end_ts": end_ts, # 1770976968,
    "period_interval": 60
}

###########################
### Check ticker exists ###
###########################
# series = "KXWOHOCKEY" # Gold medal in Women's Ice Hockey at the 2026 Winter Olympics
# r = requests.get(f"{BASE}/markets", params={"series_ticker": series, "status": "open"})
# markets = r.json()["markets"]
# for m in markets[:20]:
#     print(m["ticker"], "***", m["title"])


#############################################
### Get historical market data for ticker ###
#############################################
ticker = "KXWOHOCKEY-WOMEN26MEDAL-USA"
r = requests.get(f"{BASE}/markets/{ticker}", params=params)
# ticker = "kxsb-26"
# r = requests.get(f"{BASE}/historical/markets/{ticker}/candlesticks")
data = r.json()
pd.DataFrame(data).to_csv("test.csv")