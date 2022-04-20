if __name__ == '__main':
    from configure import Config, uConfig
else:
    from config.configure import Config, uConfig

Default = Config['DEFAULT']

SQSIZE = int(Default['size'])
CELL_COL1 = Default['col1']
CELL_COL2 = Default['col2']
CELL_SEL0 = Default['sel0']
CELL_SEL1 = Default['sel1']
CELL_SEL2 = Default['sel2']
CHECK = Default['check']
KILL = Default['kill']
BOARD_BORDER = Default['board_border']
MARKING_FONT = Default['marking_font']

MARKING = (
    ('1', '2', '3', '4', '5', '6', '7', '8'),
    ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
)

ipath = "assets/images/" + uConfig["ipath"]