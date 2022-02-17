    
    
import datetime
import requests
from pytz import timezone
tz = timezone('EST')

ALPACA_API_SECRET = '0qbJ1w4qI2nq3HKpDk7uVpjqLq6qgOLTdANH84kE'
ALPACA_API_KEY = 'AKONDXTFSFXNTOZ15B7D'


# use isoformat to make this date RFC-3339 compliant
def convert_date(date_obj):
    date_obj = tz.localize(date_obj)
    date_str = date_obj.isoformat()
    return date_str


def get_price(ticker, date, minutes_after=1.6):   
    
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')  # + datetime.timedelta(minutes=1)
    date_obj = date_obj + datetime.timedelta(minutes=minutes_after)

    url = f'https://data.alpaca.markets/v2/stocks/{ticker}/trades'

    # FIRST ACTION (EITHER SHORT OR BUY)
    params = {'start': convert_date(date_obj), 'end': convert_date(date_obj + datetime.timedelta(minutes=5)), 'limit': 10}
    
    headers = {'APCA-API-KEY-ID': ALPACA_API_KEY, 'APCA-API-SECRET-KEY': ALPACA_API_SECRET}

    response = requests.get(url, params=params, headers=headers)
    response_json = response.json()

   
    try:
        return response_json['trades'][0]['p']
    except:
        return None

def percent_move(ticker, date, minutes):
    price1 = get_price(ticker, date)
    price2 = get_price(ticker, date, minutes_after=minutes)

    if price1 is None or price2 is None:
        return None
    else:
        return (price2 - price1) / price1 * 100