pyChess
=======

This is the pyChess project by Timothy Myers.
The goal of the project is to create a chess engine that imports and exports
partial games in the Portable Game Notation file format so that chess games may be
played over email.

This is currently implemented in Python 3.4.
This is back under active development right now. The game engine is fully functional 
including a PGN parser/exporter that support FEN notation.

Also included is configuration that allows for randomized starting positions, an idea
shameless inspired by `Really Bad Chess<http://www.reallybadchess.com/>`

To Install:
    pip install .

This installation will install the required dependencies

To Run:
    chess.py

Also included is the pychess.wsgi file required for hooking the Web UI up to an apache 
server. The apache site file is left up to the consumer.

This uses Piece images created by `Peter Wong
<http://www.virtualPieces.net>`_.
