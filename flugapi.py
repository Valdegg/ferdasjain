# LiveSearch fluggjalda api 


from datetime import date, timedelta
from requests import get, post, put
from pprint import pprint
import json
import sys

USER_COUNTRY = "IS/"
API = 'http://api.dohop.com/api/v1/livestore/en/' + USER_COUNTRY
CURRENCY = "EUR"

def get_for_day(from_airport, day, stay=None):
    include_split = bool(stay)

    request = {'currency': CURRENCY,
               'fare-format': 'full',
               'from_airport': from_airport,
               #'arrival_airports': arrival_airports,
               #'wd': '12345', # monday = 1
               'date_from': day,
               'date_to': day,
               'stay': stay,
               'include_split': include_split,
               'n_max': 100}
    uri='per-country/{from_airport}/{date_from}/{date_to}'
    uri=API+uri.format(**request)
    json = get(uri, params=request).json()

    if "error" in json:
        raise FareError(json["error"])
    return json
	
	
	

fluggjold = get_for_day("KEF", "2017-07-12")
print(fluggjold)
gjold = fluggjold['fares']
vellir = fluggjold['airports']
for flug in gjold: 
	
	print( vellir[flug['b']] )
	print( str(flug['f'])+ flug['c']) 