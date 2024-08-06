import requests
import time
import datetime as dt
import pandas as pd
import pytz

# porssisahko.net provides api for NordPool electricity exchange hourly
# prices for Finland. Prices include tax, but not operator costs.
# Prices are available until the end of the next day, and are updated
# around 14:00 every day. 
# API is declared free to use for any purpose, but no licence is provided.
# API documentation available at https://porssisahko.net/api

API = "https://api.porssisahko.net/v1/"
REQUEST_LATEST_PRICES = "latest-prices.json"
REQUEST_PRICE_FOR_HOUR = "price.json?date=[date]&hour=[hour]"
PARAM_DATE = "[date]"
PARAM_HOUR = "[hour]"

# Porssisahko api assumes single hour requests in local time
TIMEZONE = "Europe/Helsinki"

def convert_to_timezone(time_str: str, tz = str)->str:
        fmt1 = "%Y-%m-%dT%H:%M:%S.000Z"
        t = dt.datetime.strptime(time_str, fmt1)
        t_utc = pytz.utc.localize(t)
        t_tz = t_utc.astimezone(tz)
        fmt2 = "%Y-%m-%d %H:%M:%S %Z%z"
        return dt.datetime.strftime(t_tz, fmt2)

WAIT_S = 0.2
TRY_MAX = 3

def parse_request(date:str = "", hour:str = "")->str:
    """
    Parse and return an API request
    """
    if hour == "latest":
        return API + REQUEST_LATEST_PRICES
    else:
        return API + REQUEST_PRICE_FOR_HOUR.replace(PARAM_DATE, date).replace(PARAM_HOUR, hour)

def request_price_for_hour(date:str, hour:str)->pd.DataFrame:
    """
    Request electricity price for an hour
    """
    request_str = parse_request(date, hour)

    data = None
    counter = 0
    while counter < TRY_MAX:
        data = requests.get(request_str)
        if data.status_code == 200:
            ret = data.json()
            ret["price"] = [ret["price"]]
            # add datetime and timezone info to ret
            tz = pytz.timezone(TIMEZONE)
            timestamp = dt.datetime.strptime(f"{date}T{hour}", "%Y-%m-%dT%H")
            timestamp_utc = tz.localize(timestamp).astimezone(pytz.utc)
            timestamp_str = timestamp_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            ret["startDate"] = [timestamp_str]
            # convert to dataframe
            df = pd.DataFrame(ret)
            return df
        counter += 1
        time.sleep(WAIT_S) # to avoid overloading the API
    msg = f"Max tries of {TRY_MAX} reached without successful response. Latest status code: {data.status_code}, for GET request: {request_str}"
    raise RuntimeError(msg)

def request_latest_prices()->pd.DataFrame:
    """
    Get all available prices from the API.
    """
    request_str = parse_request(hour = "latest")

    data = None
    counter = 0
    while counter < TRY_MAX:
        data = requests.get(request_str)
        if data.status_code == 200:
            df = pd.DataFrame(data.json())
            df = pd.concat([df, df["prices"].apply(pd.Series)], axis=1)
            df.drop(columns=["prices", "endDate"], inplace = True)
            return df
        counter += 1
        time.sleep(WAIT_S) # to avoid overloading API
    msg = f"Max tries of {TRY_MAX} reached without successful response. Latest status code: {data.status_code}, for GET request: {request_str}"
    raise RuntimeError(msg)