import os
import psycopg2
import requests
import csv
from io import StringIO

from dotenv import load_dotenv

load_dotenv(override=True)

# PostgreSQL configuration
pg_config = {
    "user": os.getenv("PGUSER"),
    "host": os.getenv("PGHOST"),
    "database": os.getenv("PGDATABASE"),
    "password": os.getenv("PGPASSWORD"),
    "port": os.getenv("PGPORT"),
}

# Create a PostgreSQL connection pool
connection = psycopg2.connect(**pg_config)

def update_instrument_list():
    instrument_list = []

    # Fetch data from PostgreSQL
    select_query = 'SELECT * FROM public."Stocks"'
    cursor = connection.cursor()
    cursor.execute(select_query)
    result = cursor.fetchall()
    print(result)

    # Fetch data from Zerodha API
    headers = {
        'Authorization': 'token ' + os.getenv("ZERODHA_API_KEY") + ":" + os.getenv("ZERODHA_ACCESS_TOKEN"),
    }
    response = requests.get("https://api.kite.trade/instruments", headers=headers)


    lines = response.text.split('\n')
    data_array = [line.split(',') for line in lines]


    for i in range(len(result)):
        #below line finds the index where the data array has the stock token value and is the nse exchange
        data_index = next((index for index, item in enumerate(data_array) if item[1] == result[i][2] and item[11] == 'NSE'), -1)
        instrument_list.append(data_array[data_index][0])
    
    for i in range(len(result)):
        update_query = f'UPDATE public."Stocks" SET "zerodhaInstrumentToken" = {instrument_list[i]} WHERE "id" = {result[i][0]}'
        print(instrument_list[i])
        print(result[i][0])
        cursor.execute(update_query)

    connection.commit()
    

    return instrument_list


def return_instrument_list_from_db():
    instrument_list = []

    # Fetch data from PostgreSQL
    select_query = 'SELECT "zerodhaInstrumentToken" FROM public."Stocks"'
    cursor = connection.cursor()
    cursor.execute(select_query)
    result = cursor.fetchall()
    result_list = [item[0] for item in result]
    return result_list


if __name__ == "__main__":
    update_instrument_list()
