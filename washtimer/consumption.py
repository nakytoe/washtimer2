import datetime as dt
import numpy as np
import pandas as pd

def uniform_consumption_kernel(hours:float,
                            minutes:float = 0,
                            account_for_current_time = False)->np.array:
    """
    Assuming an appliance consumes energy with constant power,
    calculate power consumption curve per hour for a program starting now.
    """
    hours += minutes/60
    now_minutes = dt.datetime.now().minute
    # if current time is not accounted for,
    # assume that appliance program would be started at half an hour,
    # (statistically valid assumption over long periods of time)
    now_hours = now_minutes/60 if account_for_current_time else 0.5
    ceil_hours = int(np.ceil(now_hours+hours))
    # assuming constant power for appliance
    kernel = np.ones(ceil_hours)
    # first hour percentage
    kernel[0] -= now_hours
    # last hour percentage
    kernel[-1] -= ceil_hours-now_hours-hours
    # normalize
    kernel /= hours

    return kernel


def calculate_consumption(energy_prices:pd.DataFrame,
                          hours:float,
                          minutes:float = 0, 
                          account_for_current_time = False,
                          kernel_function = uniform_consumption_kernel)->pd.DataFrame:

    """
    Calculate energy consumption / price via simple kernel convolution.

    Note that the unit for consumption is one,
    as we do not know the power of the appliance.

    Therefore, the result is actually a kernel/rolling mean of the hourly prices,
    defaulting with assumption that program is started half past current hour, with
    optionally accounting for the starting time offset (e.g. starting at 13 past etc.)
    """
    
    kernel = kernel_function(hours, minutes, account_for_current_time)
    energy_prices = energy_prices.sort_values(by = "startDate", ascending=True)
    mean_price = np.convolve(energy_prices.price, kernel, "valid")
    
    valid_hours = mean_price.shape[0]
    start_time = energy_prices.startDate.iloc[:valid_hours]

    def get_hourdelta(time_then: str, time_now: str)->str:
        fmt = "%Y-%m-%dT%H:%M:%S.000Z"
        time_d =  dt.datetime.strptime(time_then, fmt) - dt.datetime.strptime(time_now, fmt)
        return time_d.seconds//3600
        
    hours_to_start = start_time.apply(get_hourdelta, args = [dt.datetime.now()])

    hours_to_end = hours_to_start + hours

    df = pd.DataFrame({"mean_price":mean_price,
                       "power_hours":hours,
                       "hours_to_start":hours_to_start,
                       "hours_to_end":hours_to_end})
    
    return df

def min_max_hours(energy_prices: pd.DataFrame,
                power_hours = [1, 2, 3, 4],
                account_for_current_time:bool = False,
                kernel_function = uniform_consumption_kernel,
                drop_past: bool = True)->pd.DataFrame:
    
    """
    Evaluate the cheapest and most expensive hours to time appliance programs
    of different power hours to. 
    """

    min_max_df = pd.DataFrame(columns={"mean_price":float,
                       "power_hours":float,
                       "start_time":int,
                       "end_time":int,
                       "minmax":str})
    
    min_max_df["minmax"] = np.nan

    def is_future(time_str: str)->str:
        fmt = "%Y-%m-%dT%H:%M:%S.000Z"
        t = dt.datetime.strptime(time_str, fmt)
        now = dt.datetime.now()
        return t > now
    
    if drop_past:
        energy_prices = energy_prices[energy_prices.startDate.apply(is_future)]

    # only keep up to next 12 hours
    energy_prices = energy_prices.iloc[:min(12, energy_prices.shape[0])]
    
    # calculate consumptions for appliance programs of given lengths
    for hours in power_hours:
        mean_price = calculate_consumption(energy_prices,
                            hours, 
                            account_for_current_time=account_for_current_time,
                            kernel_function = kernel_function)
        
        cheapest = mean_price.iloc[mean_price.mean_price.argmin()].copy()
        cheapest["minmax"] = "min"

        expensive = mean_price.iloc[mean_price.mean_price.argmax()].copy()
        expensive["minmax"] = "max"

        min_max_df.loc[min_max_df.shape[0]] = cheapest
        min_max_df.loc[min_max_df.shape[0]] = expensive
        
    return min_max_df