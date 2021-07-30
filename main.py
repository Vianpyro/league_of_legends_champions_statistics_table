# -*- coding: utf-8 -*-
import os
import requests
import json

# Get the data from the Data Dragon API
version = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]

# Check if version is in json file name
if os.path.isfile(f'champions_{version}.json'):
    print('loading from file')
    data = json.load(open(f'champions_{version}.json'))
else:
    print(f'loading data online for patch {version}')
    data = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json').json()['data']

    # Remove unnecessary data to free up drive space
    for champion in data:
        champion_stats = data[champion]['name'], data[champion]['stats']
        data[champion].clear()
        data[champion]['name'], data[champion]['stats'] = champion_stats
        
    # Remove every stat in which every champion has a value of 0
    keys_to_remove = []
    for stat in data[list(data.keys())[0]]['stats']:
        is_value_null = True
        for champion in data:
            if data[champion]['stats'][stat] != 0:
                is_value_null = False
        if is_value_null:
            keys_to_remove.append(stat)
    for key in keys_to_remove:
        for champion in data:
            data[champion]['stats'].pop(key)

    with open(f'champions_{version}.json', 'w') as f:
        f.write(json.dumps(data))

# Find the longest champion name
first_champion = list(data.keys())[0]
longest_word = 0
for champion in data:
    if len(data[champion]['name']) > longest_word:
        longest_word = len(data[champion]['name'])

for stat in data[first_champion]['stats']:
    if len(stat) > longest_word:
        longest_word = len(stat)

# Sort champions by stat
sort_by = input(f"Sort champions by {['name'] + list(data[first_champion]['stats'].keys())}: ")
if sort_by in data[first_champion]['stats']:
    sorted_champions = sorted(data, key=lambda champion: data[champion]['stats'][sort_by], reverse=True)
else:
    sorted_champions = data.keys()
    

# Write everything to a text file
line_separator = f"\n{'-' * ((longest_word + 3) * len(data[first_champion]['stats']) + 3)}\n"

with open('champions.txt', 'w') as file:
    file.write(f"{'name':^{longest_word}} |")

    for stat in data[first_champion]['stats']:
        file.write(f"{stat.replace('perlevel', '/level'):^{longest_word}} |")

    file.write(line_separator)

    for champion in sorted_champions:
        file.write(f"{data[champion]['name']:^{longest_word}} |")

        for stat in data[champion]['stats']:
            file.write(f"{data[champion]['stats'][stat]:^{longest_word}} |")

        file.write(line_separator)
