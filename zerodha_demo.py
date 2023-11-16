from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
from get_token_and_stock_list import get_instrument_list
import redis
import json
import time

# Get the current timestamp


accessToken = "c3pH5AzjIjR8AZFTc97E30Vy4328dWbh"  # to be copied from the other file
redisConnectionString = "redis-15632.c264.ap-south-1-1.ec2.cloud.redislabs.com:15632"
# r = redis.from_url(redisConnectionString) # global redis connection object
import redis

r = redis.Redis(
  host='redis-15632.c264.ap-south-1-1.ec2.cloud.redislabs.com',
  port=15632,
  password='lczWV743S9m9q25dgJ9H5ktOYuZMDyHG')



def autoLogin():
    load_dotenv(override=True)
    apiSecret = os.getenv("ZERODHA_API_SECRET")
    apiKey = os.getenv("ZERODHA_API_KEY")


def main():
    load_dotenv(override=True)
    apiKey = os.getenv("ZERODHA_API_KEY")

    kws = KiteTicker(api_key=apiKey, access_token=accessToken)

    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close
    kws.connect()


def on_ticks(ws, ticks):
    # Callback to receive ticks.
   
    json_data = json.dumps(ticks)
   
    print(json_data)
    start_time = r.time()
    r.set('tickData', json_data)
    end_time = r.time()

    latency_in_microseconds = int(end_time[0]) * 1_000_000 + int(end_time[1]) - (int(start_time[0]) * 1_000_000 + int(start_time[1]))

    print(f"Latency: {latency_in_microseconds} microseconds")
    # print(json.loads(r.get('tickData')))



def on_connect(ws, response):
    instrumentList = get_instrument_list()
    integerInstrumentList = [int(num) for num in instrumentList]

    ws.subscribe(integerInstrumentList)

    ws.set_mode(ws.MODE_LTP, integerInstrumentList)


def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    r.close()
    ws.stop()


if __name__ == "__main__":
    main()
