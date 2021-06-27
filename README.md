# ParseCiv6Export
This is a parser for json files exported at the end of the game in Sid Meier's Civilization VI. It creates two files: a list of events and their number (partly those that give era points), and a list of civilizations.<br />
A list of civilizations contains:
1. Name of the civilization
2. Leader of the civilization
3. Events of the civilization
3.1. Amount of an event
3.2. Turns on which this event happened

For the parser to work, you should add the following directories:
* exports
* output
** civilizations
** events

Put the jsons exported at the end of the game to "exports" directory, rename them to have different numbers before the file extension, and then run the "main.py" file.