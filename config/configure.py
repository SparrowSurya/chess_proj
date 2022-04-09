from configparser import ConfigParser

config = ConfigParser()
config.read("configs/config.ini")

config.add_section('Main')


with open('config.ini', 'w') as file:
    config.write(file)



