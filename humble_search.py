## This script scrapes the steam game pages from that one website and returns it as a usable table

# Import Modules
import pandas as pd
import numpy as np
import re

# Import data

imported_table = pd.read_csv(r'humble_games_list.csv')
print(imported_table.shape)

# Create the naughty list from the games that failed the tag search process
def make_naughty():
    no_tags = imported_table.loc[imported_table['Tags'] == 'Game not found'].copy()
    pending_changes = no_tags.reset_index(drop=True)
    pending_changes.to_csv('pending_changes.csv')
    print(no_tags.shape)
    print(pending_changes.head(10))

make_naughty()




