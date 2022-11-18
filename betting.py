import json
import pandas as pd
import requests
from pandas import json_normalize
from six import iteritems
pd.options.mode.chained_assignment = None

# this is the response from the API that I used
response = requests.request("GET", url, headers=headers, params=querystring)
a = response.json()
l = []

# this block iterates through the nested json the api returns to pull the relevant information for later use and store it in l
for i in range(len(a)):
    for j in range(len(a[i]['bookmakers'])):
        l.append(a[i]['bookmakers'][j]['title'])
        for x in range(len(a[i]['bookmakers'][j]['markets'][0]['outcomes'])):
            l.append(a[i]['bookmakers'][j]['markets'][0]['outcomes'][x]['name'])
            l.append(a[i]['bookmakers'][j]['markets'][0]['outcomes'][x]['price'])

# this block takes the information from the list and appends the games and prices to the betmaker    
d = {}
for i in range(0, len(l), 5):
    if l[i] in d:
        d[l[i]].update({l[i+1]:l[i+2], l[i+3]:l[i+4]})
    else:
        d[l[i]] = {l[i+1]:l[i+2], l[i+3]:l[i+4]}

# creates a df from the dictionary
df = pd.DataFrame.from_dict(d, orient='index')

# finds the highest or lowest price for each team depending on whether they have + or - odds
max_row = lambda x: max(x.min(), x.max(), key = abs)
new = df.apply(max_row, axis = 0)
maker = df.abs().idxmax()
df1 = pd.concat([new, maker], axis=1)

# this block takes the prices and calculates the teams odds in decimal form
price = df1.filter([0]).values.reshape(1,-1).ravel().tolist()
for i, v in enumerate(price):
    if v < 0:
        price[i] = (abs(v)/(abs(v) + 100)) * 100
    else:
        price[i] = (100/(v + 100)) * 100

# this block figures the implied probability of the matchup witch is the most important and what we need to pay attention to
implied = []        
for i in range(0, len(price), 2):
    implied.append(price[i] + price[i+1])
    implied.append(price[i] + price[i+1])

# this block is just some renaming and rearanging to make the df look better
df1['Odds'] = price
df1['Implied'] = implied
df1.rename({0:'American Odds', 1:'Bookmaker'}, axis = 1, inplace=True)
df1.index.name = "Teams"
df1.drop(['American Odds'], axis=1, inplace=True)
team1 = df1.iloc[0::2, :]
team1.drop(['Implied'], axis=1, inplace=True, errors='')
team2 = df1.iloc[1::2, :]
team1.reset_index(inplace=True)
team2.reset_index(inplace=True)
team2 = team2[['Implied', 'Odds', 'Bookmaker', 'Teams']]
hz = pd.concat([team1, team2], axis=1).round(decimals=2)
hz_html = hz.to_html()

