if __name__ == '__main':
    from configure import File, Config
else:
    from config.configure import File, Config

default = Config['DEFAULT']

SQSIZE = int(default['size'])
CELL_COL1 = default['col1']
CELL_COL2 = default['col2']
CELL_EDGE1 = default['edge1']
CELL_EDGE2 = default['edge2']
SEL1 = default['sel1']
SEL2 = default['sel2']
CHECK = default['check']
KILL = default['kill']

