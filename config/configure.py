import json

File = "config/config.json"

with open(File, 'r') as f:
    Data = f.read()

Config = json.loads(Data)

