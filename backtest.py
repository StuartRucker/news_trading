import json
import re
import random
import difflib
import requests
import datetime
from pytz import timezone

tz = timezone('EST')

API_SECRET = '0qbJ1w4qI2nq3HKpDk7uVpjqLq6qgOLTdANH84kE'
API_KEY = 'AKONDXTFSFXNTOZ15B7D'

filename = 'data/singleshot-2022-02-11.json'
with open(filename) as f:
    data = json.load(f)


# Find where an already identified ticker is in the Stocks Affected ticker
def get_ticker_index(ticker, words):
    for i in range(len(words)):
        if ticker in words[i]:
            return i
    return -1


# get company names preceeding tickers in Stocks Affected
def get_company_names(tickers, s):
    company_names = []
    all_words = s.split()

    for ticker in tickers:
        # Find the capitalized words that come before ticker in the string s
        ticker_index = get_ticker_index(ticker, all_words)

        words = all_words[:ticker_index]

        company_name = []
        for i in range(len(words) - 1, max(-1, len(words) - 3), -1):
            if any([t in words[i] for t in tickers]):
                break
            if words[i][0].isupper():
                company_name.append(words[i])
            else:
                break

        company_names.append(' '.join(reversed(company_name)))
    return company_names


# get tickers of Stocks Affected:
def get_tickers(s):
    # using regex, find stock tickers with patterns such as (XXX)
    tickers = re.findall(r'\(([A-Z]{1,5})\)', s)

    # use regex to find stock tickers with patterns such as (NYSE: VEPCO)
    tickers += re.findall(r'\(NYSE:\s*([A-Z]{1,5})\)', s)

    return tickers


# helper function for apply_stock_move
def apply_move(info, mode, move):
    if mode == 'all':
        for ticker in info.keys():
            info[ticker]['move'] = move
    else:
        info[mode]['move'] = move


# adds the stock move to the info dictionary based on the prediction
def apply_stock_move(info, s):
    up_words = set(['up', 'increase', 'increases', 'raise', 'raises', 'rise', 'rises', 'grow', 'grows'])
    down_words = set(['down', 'decrease', 'decreases', 'fall', 'falls', 'decline', 'declines', 'shrink', 'shrinks'])
    words = s.split()

    mode = 'all'
    for word in words:
        # first set mode to a company ticker if that company is mentioned in the word
        for c_info in info.values():
            if difflib.SequenceMatcher(None, c_info['ticker'], word).ratio() > 0.5 or difflib.SequenceMatcher(None,
                                                                                                              c_info[
                                                                                                                  'company'].lower(),
                                                                                                              word.lower()).ratio() > 0.46:
                mode = c_info['ticker']

        if word.lower() in up_words:
            apply_move(info, mode, 'up')
        elif word.lower() in down_words:
            apply_move(info, mode, 'down')


# converts date to format of alpaca api

def convert_date(date_obj):
    date_obj = tz.localize(date_obj)
    # make the date_obj timezone aware in ET time zone

    # use isoformat to make this date RFC-3339 compliant
    date_str = date_obj.isoformat()
    # url encode the date_str

    return date_str


def apply_prices_alpaca(info, date):
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M') + datetime.timedelta(minutes=1)
    tomorrow = date_obj + datetime.timedelta(minutes=30)
    for ticker in info.keys():
        # make a request to the alpaca api for the price of the ticker on the date at GET/v2/stocks/{symbol}/trades
        # authenticate with API_KEY and API_SECRET
        print(ticker)
        url = f'https://data.alpaca.markets/v2/stocks/{ticker}/trades'
        params = {'start': convert_date(date_obj), 'end': convert_date(tomorrow), 'limit': 2}
        print(params)
        headers = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}

        response = requests.get(url, params=params, headers=headers)
        response_json = response.json()
        if response_json and response_json['trades'] and len(response_json['trades']) > 0:
            info[ticker]['prices'] = (response_json['trades'][0]['p'], response.json()['trades'][-1]['p'])


def process_article(article):
    tickers = get_tickers(article['Prediction'])

    companies = get_company_names(tickers, article['Prediction'])

    info = {ticker: {'company': company, 'ticker': ticker, 'move': None} for ticker, company in zip(tickers, companies)}

    apply_stock_move(info, article['Prediction'])

    apply_prices_alpaca(info, article['date'])

    # print the article title, summary, and then the ticker and move for each company
    # print("\n\n*********************")
    # for k in ['title', 'summary', 'Stocks Affected', 'Prediction']:
    #     print(k, article[k])
    # print(info)

    return info


random.shuffle(data)
output_info = []
for article in data:
    output_info.append(process_article(article))

# save output_info to a json file
with open('tmp.json', 'w') as f:
    json.dump(output_info, f)
