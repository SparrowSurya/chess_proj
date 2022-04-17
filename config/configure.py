import json

File = "config/config.json"
uFile = "config/uconfig.json"

with open(File, 'r') as f:
    Data = f.read()

with open(uFile, 'r') as f:
    uData = f.read()

Config = json.loads(Data)
uConfig = json.loads(uData)