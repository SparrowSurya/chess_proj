import re

# PID
PID = re.compile("[01][kqbnrp]|\.\.")
PID_SEQ = re.compile("([01][kqbnrp]|\.\.){64}")

def get_pid(player: str, piece: str) -> str:
    """Returns the pid of given two info. Raises error in case of Invalid."""
    _pid = f"{player}{piece}"
    if len(_pid)==2 and PID.fullmatch(_pid):
        return _pid
    else:
        raise Exception(f"Invalid player: {player} or piece:{piece}")

def check_pid(_pid: str) -> bool:
    """Check the given pid. Raises error in case of Invalid."""
    if not isinstance(_pid, str):
        raise Exception(f"Invalid parameter type; pid:{_pid} type:{type(_pid)}")
    elif bool(PID.fullmatch(_pid)):
        return True
    else:
        raise Exception(f"Invalid piece_id: '{_pid}'")

def validate_pid_seq(seq: str) -> bool:
    """Check the given pid sequence as per chessgrid. Raises error in case of Invalid."""
    return bool(PID_SEQ.match(seq))

def pid_seq_2_list(seq: str) -> list[str]:
    """Returns the list of pids seq. Raises error if the  seq isnt valid as per chess seq."""
    validate_pid_seq(seq)
    k = PID.findall(seq)
    return k



"""
src: https://youtu.be/Q9_dS8H2rU8
moves repr:

pieces: K, Q, B, N, R, nothing for pawn

'+' for check; for multiple check use as many number of '+' (placed at end)
x for capture (placed before the Final_Pos)
'=?' for promotion after Final_Pos where ? is Q, B, N, R
'0-0' if castle from king side
'0-0-0' if castle from queen side

default: Piece_FinalPos
capture: Piece_x_FinalPos
check:
    Piece_FinalPos+ (if single)
    Piece_FinalPos++ (if double)
    so on...

if two piece of same kind can: move to a destination:
    Piece_InitialUncommonPos_Final_Pos (if single dimension info is enough)
    Piece_InitialPos_x_Final_Pos (if single dimension info is not enough + capture)

for pawn:
    Final_Pos (above rules are also implemented)

win:
    white: 1-0
    black: 0-1
    stalemate/draw: 0.5-0.5

"""
