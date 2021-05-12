import json

class Parser:
	def __init__(self, data: dict, game: int):
		self.data = data	# The original json file exported from Civ6.
		self.game = game	# Ordinal number. Used to differentiate between json files (by appearing in their names).

	def count_moments(self):
			"""Creates a json file in "output" directory with types of moments in the game. Returns an amount of unique moments.
		
			"""

			types = {}
			incr = 0
		
			for i in self.data['Moments']:
					if not i['Type'] in types:
							types[i['Type']] = 1
							incr = incr + 1
					else:
							types[i['Type']] += 1
		
			with open(f"output/event_type{self.game}.json", "w", encoding='utf-8') as write_file:
					write_file.write(json.dumps(types, indent=4, sort_keys=True))
		
			return incr

	def count_civ_moments(self, civId):
			"""Returns moments related to a civilization.
		
			Parameters
			----------
			civId : int
					An id of a civilization from the original json file.
			"""

			types = {}
		
			for i in self.data['Moments']:
					if (not i['Type'] in types) and (i['ActingPlayer'] == civId):
							types[i['Type']] = 1
					elif (i['Type'] in types) and (i['ActingPlayer'] == civId):
							types[i['Type']] += 1
		
			json_object = json.dumps(types, indent=4, sort_keys=True)
			types = json.loads(json_object)

			return types

	def count_players(self, displayAll):
			"""Creates a json file in "output" directory with civilizations in the game. Returns an amount of unique civilizations.
		
			Parameters
			----------
			displayAll : bool
					"True" to list all civilizations, including city states, free states and barbarians.
					"False" to list only proper civilizations.
			"""

			civs = {}
			incr = 0

			for i in self.data['Players']:
					if (not i['Id'] in civs) and (displayAll or (i['CivilizationShortDescription'] != i['LeaderName'])):
							civ = {}
							name = {}
							leader = {}

							name[i['CivilizationShortDescription']] = i['CivilizationShortDescription']
							leader[i['LeaderName']] = i['LeaderName']

							civ['name'] = name[i['CivilizationShortDescription']]
							civ['leader'] = leader[i['LeaderName']]
							civ['moments'] = self.count_civ_moments(i['Id'])
							
							civs[i['Id']] = civ
							incr = incr + 1
		
			with open(f"output/civ_list{self.game}.json", "w", encoding='utf-8') as write_file:
					write_file.write(json.dumps(civs, ensure_ascii=False, indent=4, sort_keys=False))
		
			return incr