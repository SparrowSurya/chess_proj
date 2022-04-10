from configparser import ConfigParser

if __name__ == '__main__':
    File = "config/config.ini"
else:
    File = "config.ini"

Config = ConfigParser()
Config.read(File)


# with open(File, 'w') as f:
#     config.write(f)


