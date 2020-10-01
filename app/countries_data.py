import json

countries = {}
with open('countries_data.json', 'r') as f:
  countries = json.loads(f.read())
