import numpy as np
import time as time

# spelarnas pjäs-listor // dessa är ganska långa och klumpiga men är det jag får använda för stunden
# P1 = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "R1", "H1", "B1", "Q", "K", "B2", "H2", "R2"]
# P2 = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "r1", "h1", "b1", "q", "k", "b2", "h2", "r2"]

P1 = {"Pawn" : "♙", "Rook" : "♖", "Knight" : "♘", "Bishop" : "♗", "King" : "♔", "Queen" : "♕" }
P2 = {"Pawn" : "b", "Rook" : "♜", "Knight" : "♞", "Bishop" : "♝", "King" : "♚", "Queen" : "♛" }

# rutornas numrering i ett dictionary
SqCodeX = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
SqCodeY = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}

# ---------------------------------------------------------------
# Här beksrivs/tas fram vilken spelares tur det är

def playerturn(arg1):
    if arg1 % 2 == 0:
        return ("Black's turn: {} seconds remaining".format(bT))
    if arg1 % 2 != 0:
        return("White's turn: {} seconds remaining".format(wT))
    
def playertime(arg1):
    global wT
    global bT
    if arg1 % 2 == 0:
        bT -= TotTime
    if arg1 % 2 != 0:
        wT -= TotTime

# ---------------------------------------------------------------

# denna del ska kolla så att draget inte landar pjäsen på en ruta med en pjäs AV SAMMA FÄRG

def legalmove1():
    
    if T % 2 == 0:
        if tP in P2.values():
            return False
        else:
            return True
    
    if T % 2 != 0:
        if tP in P1.values():
            return False
        else:
            return True

# ---------------------------------------------------------------

# denna del ska kolla så att själva draget är lagligt - än så länge kollar den endast bönder

def legalmove2():
    global P
    
    if P == "♙":
        if T == 1:
            if (My == Py - 1 and Mx == Px) or (My == Py - 2 and Mx == Px):
                return True
            else:
                return False
        if T != 1:
            if (My == Py and Mx == Px):
                return True
            else:
                return False
            
    if P == "b":
        if T == 2:
            if (My == Py + 1 and Mx == Px) or (My == Py + 2 and Mx == Px):
                return True
            else:
                return False
        if T != 2:
            if (My == Py and Mx == Px):
                return True
            else:
                return False

# ---------------------------------------------------------------

# skapar brädet och rutornas numreringar
# --------------------------------------

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

# -----------------

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

# Här spelas spelet / flyttas pjäserna

T = 0

wT = 600
bT = 600

while True:
    start = time.time()
    T += 1
    print(playerturn(T))
        
    print("Vilken pjäs ska du flytta?")
    Px = int(SqCodeX[input()])
    Py = int(SqCodeY[input()])
    
    print("Vart ska pjäsen flyttas?")
    Mx = int(SqCodeX[input()])
    My = int(SqCodeY[input()])
    
    end = time.time()
    TotTime = int(end - start)
    playertime(T)
    
    P = Board[Py, Px]
    legalmove2()
    if legalmove2() == True:
        None
    if legalmove2() == False:
        print("Olagligt drag, försök igen")
        T -= 1
        continue
    
    tP = Board[My, Mx]
    legalmove1()
    if legalmove() == True:
        None
    if legalmove() == False:
        print("Olagligt drag, försök igen")
        T -= 1
        continue
    
    Board[My, Mx] = P
    Board[Py, Px] = " "
    print(Board)

# ---------------------------------------------------------------