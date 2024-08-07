import boto3
import numpy as np
import pandas as pd
from washtimer import porssisahko as pool
from washtimer.consumption import min_max_hours
from washtimer.page_html import get_page_html
import os


def lambda_handler(event, context):

    # calculate cheapest hours

    price_df = pool.request_latest_prices()

    # currently only accounting for 3 hour programs based on user experience
    power_hours = 3
    df = min_max_hours(price_df, power_hours=[power_hours])
    begin_hours = int(df[np.logical_and(df.power_hours==3, df.minmax == "min")].hours_to_start[0])
    end_hours = begin_hours + power_hours
    
    # format html page

    html_content = get_page_html(begin_hours, end_hours)
    
    # Specify the S3 bucket name and object key
    bucket_name = os.getenv("BUCKET_NAME")
    object_key = 'index.html'

    # Initialize S3 client
    s3 = boto3.client('s3')

    # Upload the HTML content as a file to S3
    s3.put_object(Bucket=bucket_name,
                  Key=object_key,
                  Body=html_content,
                  ContentType='text/html',
                  Metadata={'Cache-Control': 'max-age=60'}
                )

    return {
        'statusCode': 200,
        'body': 'Page update completed'
    }