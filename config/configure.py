from configparser import ConfigParser

config = ConfigParser()
config.read("configs/config.ini")

config.add_section('User')


with open('configs/config.ini', 'w') as file:
    config.write(file)



