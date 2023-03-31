import numpy as np

# spelarnas pjäs-listor // dessa är ganska långa och klumpiga men är det jag får använda för stunden
# P1 = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "R1", "H1", "B1", "Q", "K", "B2", "H2", "R2"]
# P2 = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "r1", "h1", "b1", "q", "k", "b2", "h2", "r2"]

P1 = {"Pawn" : "♙", "Rook" : "♖", "Knight" : "♘", "Bishop" : "♗", "King" : "♔", "Queen" : "♕" }
P2 = {"Pawn" : "♟", "Rook" : "♜", "Knight" : "♞", "Bishop" : "♝", "King" : "♚", "Queen" : "♛" }

# rutornas numrering i ett dictionary
SqCode = {}

# ---------------------------------------------------------------

# Här beksrivs/tas fram vilken spelares tur det är
T = 1

def playerturn(arg1):
    if arg1 % 2 == 0:
        return ("Blacks turn")
    if arg1 % 2 != 0:
        return("Whites turn")

def turnswitch(arg1):
    arg1 += 1
    return(T)


for i in range(3):
    turnswitch(T)
    print(playerturn(turnswitch(T)))

# ---------------------------------------------------------------

# skapar brädet och rutornas numreringar
Board = np.full((8, 8), " ")

# skapar axlarna // vet fortfarande inte riktigt hur jag ska implementera dessa men har kvar dem här ändå
X = np.full((1, 8), 0)
Y = np.full((8, 1), 0)
for i in range(8):
    X[0, i] = i + 1
    Y[i, 0] = i + 1

# placerar pjäserna
for i in range(8):
    Board[1, i] = P2["Pawn"]
    Board[6, i] = P1["Pawn"]

Board[0, 0] = P2["Rook"]
Board[0, 7] = P2["Rook"]

Board[0, 1] = P2["Knight"]
Board[0, 6] = P2["Knight"]

Board[0, 2] = P2["Bishop"]
Board[0, 5] = P2["Bishop"]

Board[0, 3] = P2["Queen"]
Board[0, 4] = P2["King"]

# -----

Board[7, 0] = P1["Rook"]
Board[7, 7] = P1["Rook"]

Board[7, 1] = P1["Knight"]
Board[7, 6] = P1["Knight"]

Board[7, 2] = P1["Bishop"]
Board[7, 5] = P1["Bishop"]

Board[7, 3] = P1["Queen"]
Board[7, 4] = P1["King"]
    
print(Board)

# ---------------------------------------------------------------

# här flyttas pjäserna

print("Vilken pjäs ska du flytta?")
piece = input()
print("Vart ska pjäsen flyttas?")
move = input()

# ---------------------------------------------------------------