# Chess Project

---

### Status:
+ `src\__init__.py` is full of errors due to some major changes.
+ configuration rework.
+ match will have its own class to seperate the custom startup match.
    <p>
    since same board will be used to play match and to have <i>custom startup match.</i>
    </p>
+ `utils\graphics.py` will be currently used for the shdow effect in pawn promotion.
    <p>
    For now focus on goog looking gui has been paused. Flat colors will be used for now.
    </p>

---

### Info:
+ External package used: pillow library 
<br>
```sh
pip install pillow
```

+ Code tested in windows 10 Home edition
+ Python Version: 3.9.5
+ tkinter package

---

### Stages:
1. 1VS1 (currently)
2. 1VSpc
3. Online mode (maily Lan but not sure yet)

---

### Stage-I Aim:
+ complete chess game with all features.
+ giving user the ability to make and save their defined chess piece positions.
+ fully customisable gui (colors, pieces, background etc.)
    <p>
    will be using cutom color picker for realtime view rather tkinter color chooser.
    </p>
+ PIL addition for some attractiveness in Interface as using the tkinter canvas

---

### Stage-II Aim:
+ to have match against pc.
    <p>
    might add some levels that how pc should play.
    </p>

---

### Stage-III Aim:
+ online mode for match.
+ not sure but would like to add a voice communication.

---

### Additional:
+ add some statistics display after each game.
+ add a hint option or kind of like what can be the better move.
+ add an option to save match to replay.
+ sound effects.
+ ...

---

### Progress:
+ Board design
+ Pieces addition
+ Drag-Drop or Click-Click to move piece
+ Moves Filter (to prevent our king to be attacked)
+ Check
+ End game (just got printed in console noting more yet)
    <p><ul>
    <li> Stalemate </li>
    <li> Insufficient pieces to End Game </li>
    </ul></p>
+ Pawn Promotion <b>WIP</b>