# Bracket Program 5000
A tournament bracket software supporting arbitrary high elimination.
meaning it supports triple elimination, quad elim etc as well as single & double.

### What it does
 - bracket generation and viewing
 - supports arbitrarily high elimination
 - match reporting
  - projected bracket by seed
  - bracket saving/loading
  - player placing when bracket is complete
  - avoiding rematches in losers bracket when possible

### 2.0
 - import players from existing Challonge/StartGG brackets (with seeding intact)
 - support for match scores (ex 3-1)
 - scrollwheel support
  
### What it doesn't do (yet)
 - easily reorder participants
 - dark mode
 - zoom in/out in bracket view

### What it will never do
 - manage setups / timeslots etc.
 - support other formats like round robin

---

### Dependencies
Python==3.6.1

pyinstaller (for building executable files)
pysmashgg
pychallonge
python-dotenv
wxPython==4.0.0a2
Pillow>=8.4.0

---

### Screenshots
The User Interface
![Gui](docs/examples/gui.png?raw=true "GUI")


full screenshots of a triple elimination bracket

Winners Bracket
![Winners bracket](docs/examples/winners.png?raw=true "Winners Bracket")
Losers Bracket
![Losers bracket](docs/examples/losers.png?raw=true "Losers Bracket")
Losers 2x Bracket (when a player loses in losers bracket)
![Losers 2x bracket](docs/examples/losers2x.png?raw=true "Losers 2x Bracket")
Finals Bracket (when there is 3 players left, similar to Grand Finals)
![Finals bracket](docs/examples/finals.png?raw=true "Finals Bracket")
