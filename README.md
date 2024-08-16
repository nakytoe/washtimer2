# washtimer2

Where to set timer on your appliance program for the cheapest wash?


Assumptions:
 - you are in the Nordics
 - you have pool-priced electricity contract
 - you run a 3 hour appliance program (laundry or dishes)
 - wash must complete within 12 hours
 - machine has uniform consumption curve
 - in a long run start times average to half past given hour

Application logic:
 - CloudWatch hourly trigger
 - Lambda, python script
 - Results updated to another github repo
 - Github pages
 - switched from S3 website back to GitHub pages since aws does not offer consumer-friendly ddos protection for hobby projects like this

Web page updated hourly on [www.washtimer.fi](https://www.washtimer.fi/)

Electricity prices from [porssisahko.net](https://porssisahko.net/api) open api.