import json
import os

from c6ep import Parser

directory = 'exports'   # Directory where json exports are stored
incr = 0                # Increment that will be included in the resulting files' names
for file in os.listdir(directory):
    with open(f'{directory}/{file}', "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
  
    parse = Parser(data, incr)
    print(parse.count_moments())
    print(parse.count_players(False))
    incr += 1
