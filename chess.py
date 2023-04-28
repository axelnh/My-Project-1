import numpy as np
import time as time

P1 = {"Pawn" : "♙", "Rook" : "♖", "Knight" : "♘", "Bishop" : "♗", "King" : "♔", "Queen" : "♕" }
P2 = {"Pawn" : "♟", "Rook" : "♜", "Knight" : "♞", "Bishop" : "♝", "King" : "♚", "Queen" : "♛" }

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
    global P
    global Mx
    global My
    global Px
    global Py
    
    if (Mx == Px) and (My == Py):
        return False
    
    else:
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

# denna del ska kolla så att själva draget är lagligt

def legalmove2():
    global P
    global Mx
    global My
    global Px
    global Py
    
    if P == "♙":
        if Py == 6:
            if (Board[(Py - 1), Px] in P1.values()) or (Board[(Py - 1), Px] in P2.values()):
                return False
            elif (My == Py - 1 and Mx == Px) or (My == Py - 2 and Mx == Px):
                return True
            elif ((My == Py - 1 and Mx == Px + 1) or (My == Py - 1 and Mx == Px - 1)) and tP in P2.values():
                return True
            else:
                return False
        if Py != 6:
            if (My == Py - 1 and Mx == Px):
                return True
            elif ((My == Py - 1 and Mx == Px + 1) or (My == Py - 1 and Mx == Px - 1)) and tP in P2.values():
                return True
            else:
                return False
            
    elif P == "♟":
        if Py == 1:
            if (Board[(Py + 1), Px] in P1.values()) or (Board[(Py + 1), Px] in P2.values()):
                return False
            elif (My == Py + 1 and Mx == Px) or (My == Py + 2 and Mx == Px):
                return True
            elif ((My == Py + 1 and Mx == Px + 1) or (My == Py + 1 and Mx == Px - 1)) and tP in P1.values():
                return True
            else:
                return False
        if Py != 1:
            if (My == Py + 1 and Mx == Px):
                return True
            elif ((My == Py + 1 and Mx == Px + 1) or (My == Py + 1 and Mx == Px - 1)) and tP in P1.values():
                return True
            else:
                return False
            
    elif P == "♖" or P == "♜":
        xdelta = (Mx - Px)
        ydelta = (My - Py)
        
        if (xdelta != 0):
            for i in range(abs(xdelta)):
                if xdelta <= 0:
                    i = -i
                if i == 0:
                    continue
                if (Board[Py, (Px + i)] in P1.values()) or (Board[Py, (Px + i)] in P2.values()):
                    return False
                else:
                    None
        elif (ydelta != 0):
            for i in range(abs(ydelta)):
                if ydelta <= 0:
                    i = -i
                if i == 0:
                    continue
                if (Board[(Py + i), Px] in P1.values()) or (Board[(Py + i), Px] in P2.values()):
                    return False
                else:
                    None
        if (Mx != Px and My != Py) or (Mx == Px and My == Py):
            return False
        else:
            return True
    
    elif P == "♗" or P == "♝":
        if (abs(Mx - Px) == abs(My - Py)):
            return True
        else:
            return False
        
    elif P == "♔" or P == "♚":
        if (abs(Mx - Px) == 1 and My == Py) or (abs(My - Py) == 1 and Mx == Px):
            return True
        elif (abs(Mx - Px) == 1) and (abs(My - Py) == 1):
            return True
        else:
            return False
     
    elif P == "♕" or P == "♛":
        if (Mx == Px) and (My != Py):
            return True
        elif (abs(Mx - Px) == abs(My - Py)):
            return True
        else:
            return False
    
    elif P == "♘" or P == "♞":
        if (abs(My - Py) == 2) and (abs(Mx - Px) == 1):
            return True
        elif (abs(Mx - Px) == 2) and (abs(My - Py) == 1):
            return True
        else:
            return False
        
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

# -----------------

for i in range(4):
    for j in range(8):
        Board[i+2, j] = " "

# -----------------

print(Board)

# ---------------------------------------------------------------

# Här spelas spelet / flyttas pjäserna

T = 0

wT = 600
bT = 600

while True:
    print(Board)
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
    tP = Board[My, Mx]
    legalmove2()
    if legalmove2() == True:
        None
    elif legalmove2() == False:
        print("Olagligt drag, så får man inte göra. Försök igen")
        T -= 1
        continue

    legalmove1()
    if legalmove1() == True:
        None
    elif legalmove1() == False:
        print("Olagligt drag, där står din pjäs redan. Försök igen")
        T -= 1
        continue
    
    Board[My, Mx] = P
    Board[Py, Px] = " "

# ---------------------------------------------------------------