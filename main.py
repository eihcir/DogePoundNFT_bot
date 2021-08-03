import os
import requests
from datetime import datetime, timedelta
import time
import tweepy

CONSUMER_KEY = os.environ['CONSUMER_KEY']

CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

ACCESS_SECRET = os.environ['ACCESS_SECRET']



# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


OPENSEA_URL = "https://api.opensea.io/api/v1/events"

#  Keep a backlog of 15 minutes in case of api outages 
last_ts = (datetime.now() - timedelta(minutes=15)).timestamp()

last_batch_ids = []
while True:
  print("sales since: ", str(datetime.fromtimestamp(last_ts)))
  try:
    querystring = {"collection_slug":"the-doge-pound","event_type":"successful","only_opensea":"false","offset":"0","limit":"300", "occurred_after": str(last_ts)}

    headers = {"Accept": "application/json"}

    response = requests.request("GET", OPENSEA_URL, headers=headers, params=querystring)

    events = response.json()['asset_events']

    for event in events:
      if event['id'] in last_batch_ids:
        continue
      price = round(int(event['total_price']) /  1000000000000000000, 4)
      msg = "{} was purchased for {} {} #THEDOGEPOUNDNFT {}".format(
        event['asset']['name'],
        price,
        event['payment_token']['symbol'],
        event['asset']['permalink'])
      print(msg)
      api.update_status(msg)


    last_ts = (datetime.now() - timedelta(minutes=15)).timestamp()
    last_batch_ids = [e['id'] for e in events]
    print(last_batch_ids)
  except Exception as e:
    print(e)
  time.sleep(60)

