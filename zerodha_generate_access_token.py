#Step 1: Click login url and generate request token
#step 2: Manually copy paste request token and run this file to generate access token


from dotenv import load_dotenv
import os
from kiteconnect import KiteConnect

requestToken = "4kvEMYmYpLYB9oEPBiqMU2ShpG2Qi0BO" #this is manually generated each time

def main():
    load_dotenv(override=True)
    apiKey = os.getenv("ZERODHA_API_KEY")
    loginUrl = "https://kite.zerodha.com/connect/login?v=3&api_key=dyzpin0xs5zplbpf" #will change if api key changes
    apiSecret = os.getenv("ZERODHA_API_SECRET")
    kite = KiteConnect(api_key=apiKey)
     #manually generated each time
    data = kite.generate_session(request_token=requestToken, api_secret=apiSecret)
    print(data["access_token"])

if __name__ == '__main__':
    main()