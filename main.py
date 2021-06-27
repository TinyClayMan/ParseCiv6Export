import json
import os
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from c6ep import Parser

# Ideally, the export file should have a number at the end
# This function matches that number and returns it
def gameNumber(file):
    return re.search(r'([0-9]+)(?=\.)', file).group()

# Parse the files
def parse():
    directory = 'exports'   # Directory where json exports are stored

    for file in os.listdir(directory):
        with open(f'{directory}/{file}', "r", encoding='utf-8') as read_file:
            data = json.load(read_file)

        parse = Parser(data, gameNumber(file))
        print(parse.count_moments())
        print(parse.count_players(False))

# Loads the parsed data into the Firebase DB
def pushToFirebase():
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('key/serviceAccountKey.json')

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': open('key/databaseURL.txt', 'r').read()
    })

    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('/statsForEvents')

    # Directories where the parsed data json files are stored
    civDirectory = 'output/civilizations'
    eventDirectory = 'output/events'
    
    # Dictionary that will contain combined data
    game = {}

    for file in os.listdir(civDirectory):
        with open(f'{civDirectory}/{file}', 'r', encoding='utf-8') as read_file:
            data = json.load(read_file)
        game[f"game{gameNumber(file)}"] = data

    # Refreshing the increment
    incr = 0
    for file in os.listdir(eventDirectory):
        with open(f'{eventDirectory}/{file}', 'r', encoding='utf-8') as read_file:
            data = json.load(read_file)
        events = {}
        events["events"] = data
        game[f"game{gameNumber(file)}"] = {**game[f"game{gameNumber(file)}"], **events}
        
        ref.set(game)
        incr = incr + 1

print('Expecting input:\n"parse" to parse the file,\n"push" to push the parsed data to Firebase DB.')
while True:
    input_action = input()
    if input_action == "parse":
        parse()
        break
    elif input_action == "push":
        pushToFirebase()
        break
    else:
        print('Wrong input')
        continue