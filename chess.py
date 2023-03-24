import numpy as np

# spelarnas pjäs-listor // dessa är ganska långa och klumpiga men är det jag får använda för stunden
# P1 = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "R1", "H1", "B1", "Q", "K", "B2", "H2", "R2"]
# P2 = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "r1", "h1", "b1", "q", "k", "b2", "h2", "r2"]

P1 = {"Pawn" : "♙", "Rook" : "♖", "Knight" : "♘", "Bishop" : "♗", "King" : "♔", "Queen" : "♕" }
P2 = {"Pawn" : "♟", "Rook" : "♜", "Knight" : "♞", "Bishop" : "♝", "King" : "♚", "Queen" : "♛" }

# rutornas numrering i ett dictionary
SqCode = {}