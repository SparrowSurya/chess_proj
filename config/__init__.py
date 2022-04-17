if __name__ == '__main':
    from configure import Config, uConfig
else:
    from config.configure import Config, uConfig

Default = Config['DEFAULT']

SQSIZE = int(Default['size'])
CELL_COL1 = Default['col1']
CELL_COL2 = Default['col2']
CELL_EDGE1 = Default['edge1']
CELL_EDGE2 = Default['edge2']
SEL1 = Default['sel1']
SEL2 = Default['sel2']
CHECK = Default['check']
KILL = Default['kill']

# images path as per user settings
ipath = "assets/images/" + uConfig["ipath"]