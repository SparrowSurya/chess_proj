from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

print(config.sections())

config.add_section('Main')

with open('config.ini', 'w') as file:
    config.write(file)



