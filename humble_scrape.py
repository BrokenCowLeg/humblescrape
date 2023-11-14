## This script scrapes the Humble Choice bundles from that one website and returns it as a usable table

# Import Modules
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import steam_scrape

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Scrape the site
url = "https://appsolutelywonderful.com/humblechoice/"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# Strip the tags to just the list of games
game_list = soup.find_all('li')
game_list = [x.text for x in game_list]

# Import the list into a pandas dataframe
game_list = pd.DataFrame(data=game_list)
game_list = game_list.drop([0,1,2,3,4]).copy()
game_list = game_list.reset_index(drop=True)
game_list.columns=['Games']

# Fix the games on the naughty list
naughty_list = pd.read_excel(r'pending_changes.xlsx')
naughty_list = naughty_list.drop(['Notes'], axis=1)
for j in game_list['Games']:
    for x in naughty_list['Game']:
        if j == x:
            print(str(j)+' is naughty.')
            replacement_str = str(naughty_list.loc[naughty_list['Game'] == j, 'Tags'])
            replacement_str = re.sub('\d+(....)', '', replacement_str)
            replacement_str = re.sub('\s+(Name: Tags, dtype: object)', '', replacement_str)
            game_list.loc[game_list['Games'] == j, 'Games'] = replacement_str
            print('It was changed to '+str(replacement_str))
game_list = game_list.drop(game_list[game_list['Games'] == 'Not on steam'].index)
#print(naughty_list.head(5))

# Strip the tags from the bundle month list
#month_list = soup.find_all('h2')
#month_list = [x.text for x in month_list]
#print(len((month_list)))
#month_list_ext =[]
#for i in month_list:
   # multi_month = (str(i)+',') * 8
   # multi_month = multi_month.split(',')
   # month_list_ext = month_list_ext + multi_month
#while('' in month_list_ext):
    #month_list_ext.remove('')
#month_list = pd.DataFrame(data=month_list_ext)

# Test mode shit
king_list = game_list.loc[game_list['Games'] == 'Curse of the Dead Gods'].copy()
small_list = game_list[:4].copy()
small_list = small_list.append(king_list)

test_mode = False
if test_mode == True:
    game_list = small_list
else:
    game_list = game_list

# Calling and running steam_scrape
game_plus_tags = pd.DataFrame(columns=['Game','Tags'])
for i in game_list['Games']:
    print('Searching for: ' + str(i))
    gametags = steam_scrape.game_search(i)
    gametags = ','.join(gametags)
    game_plus_tags = game_plus_tags.append({
        'Game':i,
        'Tags':gametags
    },ignore_index=True)

print(game_plus_tags.shape)

if test_mode == False:
    game_plus_tags.to_csv('humble_games_list.csv',index=False)
else:
    game_plus_tags = game_plus_tags[game_plus_tags['Tags'].str.contains('Co-op')]
    print(game_plus_tags.head(10))