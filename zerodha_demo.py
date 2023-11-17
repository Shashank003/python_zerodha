from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
from update_zerodha_instruments_list import update_instrument_list, return_instrument_list_from_db
import redis
import json
import time

from celery_app import hello


# Get the current timestamp


accessToken = os.getenv("ZERODHA_ACCESS_TOKEN") # to be copied from the other file
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

    print(len(ticks))
    pipeline = r.pipeline()

    for item in ticks:
        pipeline.set(str(item["instrument_token"]), item["last_price"])


    start_time = time.perf_counter()
    result = pipeline.execute()
    end_time = time.perf_counter()

    latency = end_time - start_time
    print(f"Latency: {latency:.6f} seconds") 

    print(ticks)




def on_connect(ws, response):
    instrumentList = return_instrument_list_from_db()
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
