pyChess
=======

This is the pyChess project by Timothy Myers.
The goal of the project is to create a chess engine that imports and exports
partial games in the Portable Game Notation file format so that chess games may be
played over email.

This is implemented in Python 2.7 right nonw due to the Flask dependency.
There are plans to move this to Python 3.3 once it becomes more avaiable in Debian
as that is my primary development platform.
This is stalled slightly right now. The game engine is fully functional and so is
the save game io. It is still not in in fully compatible PGN format however.

To Install:
    python setup.py install

This installation will install the required dependencies

To Run:
    chess.py
or
    chessGUI.py


This uses Piece images created by `Peter Wong<www.virtualPieces.net?`_.
