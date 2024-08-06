# for local dev / test 
import numpy as np
import pandas as pd
from washtimer import porssisahko as pool
from washtimer.consumption import min_max_hours
from washtimer.page_html import get_page_html


def main():

    # calculate cheapest hours

    price_df = pool.request_latest_prices()

    # currently only accounting for 3 hour programs based on user experience
    power_hours = 3
    df = min_max_hours(price_df, power_hours=[power_hours])
    begin_hours = int(df[np.logical_and(df.power_hours==3, df.minmax == "min")].hours_to_start[0])
    end_hours = begin_hours + power_hours
    
    # format html page

    html_content = get_page_html(begin_hours, end_hours)

    print(html_content)

if __name__=="__main__":

    main()