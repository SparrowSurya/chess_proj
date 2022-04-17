import json

File = "config/config.json"
uFile = "config/uconfig.json"

with open(File, 'r') as f:
    Config = json.loads(f.read())

with open(uFile, 'r') as f:
    uConfig = json.loads(f.read())
