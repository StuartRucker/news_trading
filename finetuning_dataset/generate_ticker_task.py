import os
import json
import time
import tqdm

#import get_price from ../util.py 
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from util import percent_move



#Phase 1: Generate the ticker task
#Ticker task = identifying relevant tickers
def get_filenames():
    PATH_PREFIX = '../data/wsj_predictions/'
    #make path relative to this file
    PATH_PREFIX = os.path.join(os.path.dirname(__file__), PATH_PREFIX)
    existing_datasets = ['large_vaccine_prompt_with_price.json',
                        'vaccine_prompt_with_price.json',
                        'vaccine_prompt_with_price1.json',
                        'visa_prompt_with_price.json',
                        'all_with_price.json']
    return [os.path.join(PATH_PREFIX, dataset_suffix) for dataset_suffix in existing_datasets]

def get_all_articles(filenames):

    all_articles = []
    seen_headlines = set()
    #read each file
    for filename in filenames:
        
        with open(filename, 'r') as f:
            data = json.load(f)

        #read each sentence
        for i in range(len(data)):
            #read each word
            
            #add the article to all_articles if 'title' is not in seen_headlines
            if data[i]['title'] not in seen_headlines:
                all_articles.append(data[i])
                seen_headlines.add(data[i]['title'])
    return all_articles


def keep_article(article):
    if 'stock market' in article['title'].lower():
        return False
    return True





filenames = get_filenames()
all_articles = get_all_articles(filenames)
all_articles = filter(keep_article, all_articles)

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'annotation_data/articles_preannotation.txt')



# append to the OUTPUT_FILE 
with open(OUTPUT_FILE, 'w') as f:
    
    
    for article in tqdm.tqdm(all_articles):
        print("**********************************************************", file=f)
        print(f"News: \"{article['title']}. {article['summary']}\"", file =f)
        
        
        for ticker in article['price_info'].keys():
            print(f"- {ticker}: {percent_move(ticker, article['date'], minutes=60)}", file=f)

        print("[[PREDICTION]]", file=f)
        print(article['Prediction'].strip(), file =f)
        print("[[ENDPREDICTION]]", file=f)
        # print(f"Tickers={', '.join(tickers)}", file =f)
        # print(f"Tags=", file =f)

        time.sleep(.005)

        