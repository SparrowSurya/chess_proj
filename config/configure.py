import json

# if __name__ == '__main__':
#     File = "config/config.json"
# else:
#     File = "config.json"
File = "config/config.json"
# print("File:", File)
with open(File, 'r') as f:
    Data = f.read()

Config = json.loads(Data)

