import os
import openai
import json

openai.organization = input("orgo")
openai.api_key = input("api")
openai.Engine.list()

# Opening JSON file
f = open('data/wsj/2022-02-11.json')

# returns JSON object as
# a dictionary
data = json.load(f)

keywords = ['Business', 'Economy', 'Heard on the Street', 'Markets', 'Tech', 'Stocks', 'Opinion', 'Life & Work']
articles = 0

output = []
for elem in data:

    elemSeen = False
    for key in keywords:
        if key in elem['categories'][0] and not elemSeen:
            # blurb = "List out all the names and stock tickers of the companies most associated with the news, and how the price will move as a result of the news:\n\n"
            # blurb += "TITLE: FDA Authorizes Use of New Eli Lilly Covid-19 Antibody Treatment\n"
            # blurb += "SUMMARY: The drug retains effectiveness against the Omicron variant. U.S. drug regulators authorized the use of a new Covid-19 antibody drug from Eli Lilly & Co. that retains effectiveness against the Omicron variant of the virus, filling a void after authorities stopped distributing some older antibody drugs that lost effectiveness against the strain."
            # blurb += "\n\nLLY: The price of Lilly is likely to increase as a result of this news.\n\n"

            blurb = "List out all the names and stock tickers of the companies most associated with the news, and how the price will move as a result of the news:\n\n"
            blurb += "TITLE: Adidas Frees the Nipple With New Sports-Bra Campaign for Women\n"
            blurb += "SUMMARY: The German sportswear brand released an internet-breaking image of bare breasts to accompany a sports-bra collection of 43 diverse styles. Adidas launched its new sports-bra campaign today with an unusual image: a grid of 25 sets of bare breasts. Aside from the surprise factor of the nudity, the breasts shown are only remarkable because they are completely normal. These are real breasts in all their perky, saggy, asymmetrical, varied forms."
            blurb += "\n\n- Adidas (ADS):  Adidas' stock price is likely to go up because of the positive publicity the company is receiving for its new campaign.\n- Nike (NKE): Nike's stock price is likely to go down because of the competition from Adidas.\n\n"


            blurb += "List out all the names and stock tickers of the companies most associated with the news, and how the price will move as a result of the news:\n\n"
            blurb += "TITLE: " + elem["title"]
            blurb += "\nSUMMARY: " + elem["summary"]
            # print(blurb)

            openai.Engine.retrieve("text-davinci-001")
            response = openai.Completion.create(
                    engine="text-davinci-001",
                    prompt=blurb,
                    max_tokens=64,
                    temperature=0)
            print("Headline:", elem["title"])
            print("Prediction:\n", response["choices"][0]["text"])
            print("-"*100)

            elem["Prediction"] = response["choices"][0]["text"]
            output.append(elem)

            elemSeen = True
            articles += 1

with open('data/singleshot-2022-02-11.json', "w") as f:
    json.dump(output, f)


