import json

def count_moments(data):
		"""Creates a json file in "output" directory with types of moments in the game. Returns an amount of unique moments.
		
		Parameters
		----------
		data : dict
				The original json file exported from Civ6.
		"""

		types = {}
		incr = 0
		
		for i in data['Moments']:
				if not i['Type'] in types:
						types[i['Type']] = 1
						incr = incr + 1
				else:
						types[i['Type']] += 1
		
		with open("output/event_type.json", "w") as write_file:
				write_file.write(json.dumps(types, indent=4, sort_keys=True))
		
		return incr

def count_civ_moments(data, civId):
		"""Returns moments related to a civilization.
		
		Parameters
		----------
		data : dict
				The original json file exported from Civ6.
		civId : int
				An id of a civilization from the original json file.
		"""

		types = {}
		
		for i in data['Moments']:
				if (not i['Type'] in types) and (i['ActingPlayer'] == civId):
						types[i['Type']] = 1
				elif (i['Type'] in types) and (i['ActingPlayer'] == civId):
						types[i['Type']] += 1
		
		json_object = json.dumps(types, indent=4, sort_keys=True)
		types = json.loads(json_object)

		return types

def count_players(data, displayAll):
		"""Creates a json file in "output" directory with civilizations in the game. Returns an amount of unique civilizations.
		
		Parameters
		----------
		data : dict
				The original json file exported from Civ6.
		displayAll : bool
				"True" to list all civilizations, including city states, free states and barbarians.
				"False" to list only proper civilizations.
		"""

		civs = {}
		incr = 0

		for i in data['Players']:
				if (not i['Id'] in civs) and (displayAll or (i['CivilizationShortDescription'] != i['LeaderName'])):
						civ = {}
						name = {}
						leader = {}

						name[i['CivilizationShortDescription']] = i['CivilizationShortDescription']
						leader[i['LeaderName']] = i['LeaderName']

						civ['name'] = name[i['CivilizationShortDescription']]
						civ['leader'] = leader[i['LeaderName']]
						civ['moments'] = count_civ_moments(data, i['Id'])
							
						civs[i['Id']] = civ
						incr = incr + 1
		
		with open("output/civ_list.json", "w") as write_file:
				write_file.write(json.dumps(civs, indent=4, sort_keys=False))
		
		return incr

with open("eleanoreDump.json", "r") as read_file:
    data = json.load(read_file)

print(count_moments(data))
print(count_players(data, False))