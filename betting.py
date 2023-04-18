import json
import pandas as pd
import requests
from pandas import json_normalize
from six import iteritems

pd.options.mode.chained_assignment = None

def get_data_from_api():
    url = "https://odds.p.rapidapi.com/v4/sports/basketball_nba/odds"
    querystring = {"regions":"us","oddsFormat":"american","markets":"h2h","dateFormat":"iso"}
    headers = {"X-RapidAPI-Key": "850d3d8184mshaf4ab07458a8dadp17502ejsnf4794b7c9f95",
               "X-RapidAPI-Host": "odds.p.rapidapi.com"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

def process_data(data):
    l = []
    for i in range(len(data)):
        for j in range(len(data[i]['bookmakers'])):
            l.append(data[i]['bookmakers'][j]['title'])
            for x in range(len(data[i]['bookmakers'][j]['markets'][0]['outcomes'])):
                l.append(data[i]['bookmakers'][j]['markets'][0]['outcomes'][x]['name'])
                l.append(data[i]['bookmakers'][j]['markets'][0]['outcomes'][x]['price'])
    return l

def create_dict_from_list(l):
    d = {}
    for i in range(0, len(l), 5):
        if l[i] in d:
            d[l[i]].update({l[i+1]:l[i+2], l[i+3]:l[i+4]})
        else:
            d[l[i]] = {l[i+1]:l[i+2], l[i+3]:l[i+4]}
    return d

def create_dataframe(d):
    df = pd.DataFrame.from_dict(d, orient='index')
    return df

def calculate_max_row(df):
    max_row = lambda x: max(x.max(), x.max())
    return df.apply(max_row, axis = 0)

def calculate_odds(price_list):
    for i, v in enumerate(price_list):
        if v < 0:
            price_list[i] = (abs(v)/(abs(v) + 100)) * 100
        else:
            price_list[i] = (100/(v + 100)) * 100
    return price_list

def calculate_implied(price_list):
    implied = []
    for i in range(0, len(price_list), 2):
        implied.append(price_list[i] + price_list[i+1])
        implied.append(price_list[i] + price_list[i+1])
    return implied

def prepare_dataframe(df1, odds, implied):
    df1['Odds'] = odds
    df1['Implied'] = implied
    df1.rename({0:'American Odds', 1:'Bookmaker'}, axis = 1, inplace=True)
    df1.index.name = "Teams"
    df1.drop(['American Odds'], axis=1, inplace=True)
    return df1

def create_team_dataframes(df1):
    team1 = df1.iloc[0::2, :]
    team1.drop(['Implied'], axis=1, inplace=True, errors='')
    team2 = df1.iloc[1::2, :]
    team1.reset_index(inplace=True)
    team2.reset_index(inplace=True)
    team2 = team2[['Implied', 'Odds', 'Bookmaker', 'Teams']]
    return team1, team2

def betting():
    data = get_data_from_api()
   
