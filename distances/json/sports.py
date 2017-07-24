"""sports.py"""

import json
from collections import OrderedDict

sport_choises = 'distances/json/sports.json'
owndefault = "Running"

def get_sport_choices():
	""" Returns first choices from json."""
	with open(sport_choises) as f:
		data = json.load(f, object_pairs_hook=OrderedDict)
		choices = []
		for d in data:
			choices.append((d, d))
	return tuple(choices)

def get_sports_json():
	with open(sport_choises) as f:
		data = json.load(f)
		js_data = json.dumps(data)
		return js_data
	
def getFieldChoices(key_field=owndefault):
	with open(sport_choises) as f:
		json_data = json.load(f)
		choices = []
		if key_field  in json_data:
			subfields = json_data[key_field]
			for field in subfields:
				choices.append((field, field))
	return tuple(choices) 
