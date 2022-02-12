#open tmp.json
import json
with open('tmp.json', 'r') as f:
    data = json.load(f)

def sign(x):
    if x > 0:
        return 'up'
    elif x == 0:
        return 'flat'
    else:
        return 'down'
counts = {}
for prediction_obj in data:
    for d in prediction_obj.values(): 
        if 'move' in d and 'prices' in d and d['move'] and d['prices'] and len(d['prices']) > 1:
            price_move_str = d['move'] + '_' + sign(d['prices'][1] - d['prices'][0])
            counts[price_move_str] = counts.get(price_move_str, 0) + 1

print(counts)