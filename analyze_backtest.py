#open tmp.json
import json
with open('data/wsj_predictions/all_with_price.json', 'r') as f:
    data = json.load(f)

def sign(x):
    if x > 0:
        return 'up'
    elif x == 0:
        return 'flat'
    else:
        return 'down'
counts = {}

# assume we put in $100 worth for each stock and zero transaction fee
total_earnings = 0

trades = []
for prediction_obj in data:
    for d in prediction_obj['price_info'].values():
        if 'move' in d and 'prices' in d and d['move'] and d['prices'] and len(d['prices']) > 1:
            price_move_str = d['move'] + '_' + sign(d['prices'][1] - d['prices'][0])

            earnings = 0
            if d['move'] == "down":
                # we chose to sell $1000 worth of stock at first time point,
                # then buy same amount of stock at second time point
                earnings += (d['prices'][0]-d['prices'][1]) * 1000/d['prices'][0]
            if d['move'] == "up":
                earnings += (d['prices'][1] - d['prices'][0]) * 1000 / d['prices'][0]
            total_earnings += earnings
            counts[price_move_str] = counts.get(price_move_str, 0) + 1
            trades.append( (earnings, d['ticker'], prediction_obj['title'] ))
print(counts)
print(earnings)
for val, ticker, title in sorted(trades, key=lambda x: x[0], reverse=True):
    print(f"{ticker} earned {val} on {title[:50]}")
# print(trades)
