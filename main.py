import requests
from datetime import datetime, timedelta
import time

url = "https://api.opensea.io/api/v1/events"


last_ts = (datetime.now() - timedelta(minutes=10)).timestamp()

while True:
  print("sales since: ", str(datetime.fromtimestamp(last_ts)))
  try:
    querystring = {"collection_slug":"the-doge-pound","event_type":"successful","only_opensea":"false","offset":"0","limit":"300", "occurred_after": str(last_ts)}

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    for event in response.json()['asset_events']:
      price = round(int(event['total_price']) /  1000000000000000000, 4)
      print(event['asset']['name'], ' sold for ', price, event['payment_token']['symbol'])
    last_ts = datetime.now().timestamp()
  except Exception as e:
    print(e)
  time.sleep(60)

