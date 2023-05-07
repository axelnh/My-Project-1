import numpy as np
import time as time
import os
from IPython.display import clear_output
from PIL import Image, ImageDraw, ImageEnhance

P1 = {"Pawn" : "♙", "Rook" : "♖", "Knight" : "♘", "Bishop" : "♗", "King" : "♔", "Queen" : "♕" }
P2 = {"Pawn" : "♟", "Rook" : "♜", "Knight" : "♞", "Bishop" : "♝", "King" : "♚", "Queen" : "♛" }

PromoteDict1 = {"Torn" : "♖", "Häst" : "♘", "Löpare" : "♗", "Drottning" : "♕"}
PromoteDict2 = {"Torn" : "♜", "Häst" : "♞", "Löpare" : "♝", "Drottning" : "♛"}

# rutornas numrering i ett dictionary
SqCodeX = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
SqCodeY = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}

# dictionary för boktstäverna jag har med i bilden på mitt schack-bräde
LettersDict = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}

# dictionary för att koppla pjäser till dess korresponderande bilder sparade på jupyter
PiecesImgDict = {"♙" : "WhP.png", "♟" : "BlP.png", "♖" : "WhR.png", "♜" : "BlR.png", "♘" : "WhKn.png", "♞" : "BlKn.png", 
                 "♗" : "WhB.png", "♝" : "BlB.png", "♔" : "WhK.png", "♚" : "BlK.png", "♕" : "WhQ.png", "♛" : "BlQ.png"}
# ---------------------------------------------------------------
# Här beksrivs/tas fram vilken spelares tur det är

def playerturn(arg1):
    if arg1 % 2 == 0:
        return ("Svarts spelares tur: {} sekunder kvar".format(bT))
    if arg1 % 2 != 0:
        return("Vit spelares tur: {} sekunder kvar".format(wT))
    
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
    global tP
    
    xdelta = (Mx - Px)
    ydelta = (My - Py)
    
    if (Mx == Px) and (My == Py):
        return False
    
    if T % 2 == 0:
        if tP in P2.values():
            return False
        else:
            None
            
    if T % 2 != 0:
        if tP in P1.values():
            return False
        else:
            None
    
    if P == "♖" or P == "♜" or P == "♕" or P == "♛":
        
        if ((Mx != Px) and (My == Py)) or ((Mx == Px) and (My != Py)):
        
            if xdelta >= 2:
                for i in range(xdelta):
                    if i == 0:
                        continue
                    if Board[Py, (Px + i)] in (P1.values() or P2.values()):
                        return False
                    else:
                        None
            elif xdelta <= -2:
                for i in range(abs(xdelta)):
                    if i == 0:
                        continue
                    if Board[Py, (Px - i)] in (P1.values() or P2.values()):
                        return False
                    else:
                        None
            elif ydelta >= 2:
                for i in range(ydelta):
                    if i == 0:
                        continue
                    if Board[(Py + i), Px] in (P1.values() or P2.values()):
                        return False
                    else:
                        None
            elif ydelta <= -2:
                for i in range(abs(ydelta)):
                    if i == 0:
                        continue
                    if Board[(Py - i), Px] in (P1.values() or P2.values()):
                        return False
                    else:
                        None
            
            else:
                return True
        
        else:
            None
    
    if P == "♗" or P == "♝" or P == "♕" or P == "♛":
        
        if (abs(Mx - Px) == abs(My - Py)):
            
            if xdelta >= 2 and ydelta >= 2:
                for i in range(xdelta):
                    if i == 0:
                        continue
                    if Board[(Py + i), (Px + i)] in (P1.values() or Board[(Py + i), (Px + i)] in P2.values()):
                        return False
                    else:
                        None
            elif xdelta >= 2 and ydelta <= -2:
                for i in range(xdelta):
                    if i == 0:
                        continue
                    if Board[(Py - i), (Px + i)] in (P1.values() or Board[(Py - i), (Px + i)] in P2.values()):
                        return False
                    else:
                        None
            elif xdelta <= -2 and ydelta >= 2:
                for i in range(ydelta):
                    if i == 0:
                        continue
                    if Board[(Py + i), (Px - i)] in (P1.values() or Board[(Py + i), (Px - i)] in P2.values()):
                        return False
                    else:
                        None
            elif xdelta <= -2 and ydelta <= -2:
                for i in range(abs(xdelta)):
                    if i == 0:
                        continue
                    if Board[(Py - i), (Px - i)] in P1.values() or Board[(Py - i), (Px - i)] in P2.values():
                        return False
                    else:
                        None
                        
            else:
                return True
        
        else:
            return False

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
        elif (My == Py) and (Mx != Px):
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

def promotecheck():
    
    global Py
    global T
    
    if T % 2 == 0:
        if My == 7:
            return True
        else:
            return False
    
    if T % 2 != 0:
        if My == 0:
            return True
        else:
            return False

# -----------------------------------

# skapar brädet och rutornas numreringar
# --------------------------------------

def boardmaker():
    
    global Board
    
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

        Board[7, 0] = P1["Rook"]
        Board[7, 7] = P1["Rook"]

        Board[7, 1] = P1["Knight"]
        Board[7, 6] = P1["Knight"]

        Board[7, 2] = P1["Bishop"]
        Board[7, 5] = P1["Bishop"]

        Board[7, 3] = P1["Queen"]
        Board[7, 4] = P1["King"]

# ---------------------------------------------------------------

def ChessBoardImg():
    
    global Board
    global P
    
    with Image.new("RGB", (900, 900), "lightgrey") as img:
        for Y in range(8):
            for X in range(8):
                for y in range(100):
                    for x in range(100):
                        if ((Y + 1) % 2 != 0) and ((X + 1) % 2 == 0):
                            img.putpixel(((x + 50 + (100*X)), y + 50 + (100*Y)), (106, 161, 33))
                        elif ((Y + 1) % 2 == 0) and ((X + 1) % 2 != 0):
                            img.putpixel(((x + 50 + (100*X)), y + 50 + (100*Y)), (106, 161, 33))
                        else:
                            continue
        
        for Z in range(2):
            for Z1 in range(900):
                for Z2 in range(50):
                    img.putpixel((Z1, Z2 + (850*Z)), (0, 0, 0))
                    img.putpixel((Z2 + (850*Z), Z1), (0, 0, 0))
        
        drawimg = ImageDraw.Draw(img)
        
        for i in range(8):
            drawimg.text(((100 + 100*i), 25), LettersDict[i], fill=(255, 255, 255))
            drawimg.text(((100 + 100*i), 875), LettersDict[i], fill=(255, 255, 255))
            drawimg.text((25, (100 + 100*i)), str(8-i), fill=(255, 255, 255))
            drawimg.text((875, (100 + 100*i)), str(i+1), fill=(255, 255, 255))
        
        img.save("ChessBoard.png")

# ---------------------------------

def BoardPieces():
    
    global Board
    
    with Image.open("ChessBoard.png") as img:
        
        for i in range(8):
            for j in range(8):
                Piece = Board[i, j]
                if Piece not in P1.values() and Piece not in P2.values():
                    for y in range(100):
                        for x in range(100):
                            if ((i + 1) % 2 != 0) and ((j + 1) % 2 == 0):
                                img.putpixel(((x + 50 + (100*j)), y + 50 + (100*i)), (106, 161, 33))
                            elif ((i + 1) % 2 == 0) and ((j + 1) % 2 != 0):
                                img.putpixel(((x + 50 + (100*j)), y + 50 + (100*i)), (106, 161, 33))
                            elif ((i + 1) % 2 == 0) and ((j + 1) % 2 == 0):
                                img.putpixel(((x + 50 + (100*j)), y + 50 + (100*i)), (211, 211, 211))
                            elif ((i + 1) % 2 != 0) and ((j + 1) % 2 != 0):
                                img.putpixel(((x + 50 + (100*j)), y + 50 + (100*i)), (211, 211, 211))
                else:
                    PieceImgLink = str(PiecesImgDict[Piece])
                    PieceImg = Image.open(PieceImgLink)
                    img.paste(PieceImg, (50 + j + (100*j), 50 + i + (100*i)), PieceImg)
        img.save("ChessBoard.png")

# ---------------------------------

# Här spelas spelet / flyttas pjäserna

boardmaker()
ChessBoardImg()

T = 0

wT = 600
bT = 600

while True:
    
    BoardPieces()
    BoardImage = Image.open("ChessBoard.png")
    BoardImage.show()
    
    start = time.time()
    T += 1
    print(playerturn(T))
        
    print("Vilken pjäs ska du flytta?")
    Pp1 = [*input()]
    Px = int(SqCodeX[Pp1[0]])
    Py = int(SqCodeY[Pp1[1]])
    
    print("Vart ska pjäsen flyttas?")
    Pp2 = [*input()]
    Mx = int(SqCodeX[Pp2[0]])
    My = int(SqCodeY[Pp2[1]])
    
    end = time.time()
    TotTime = int(end - start)
    playertime(T)
    
    P = Board[Py, Px]
    tP = Board[My, Mx]
    
    legalmove3()
    if legalmove3() == True:
        None
    elif legalmove3() == False:
        clear_output(wait=True)
        print("Du kan inte flytta en motståndarpjäs. Försök igen")
        T -= 1
        continue
    
    legalmove2()
    if legalmove2() == True:
        None
    elif legalmove2() == False:
        clear_output(wait=True)
        print("Olagligt drag. Försök igen")
        T -= 1
        continue

    legalmove1()
    if legalmove1() == True:
        None
    elif legalmove1() == False:
        clear_output(wait=True)
        print("Olagligt drag. Försök igen")
        T -= 1
        continue
        
    if P == "♙" or P == "♟":
        promotecheck()
        if promotecheck() == True:
            print("Vilken pjäs ska bonden befordras till? : Häst, Löpare, Torn, Drottning")
            PrmtI = input()
            if T % 2 == 0:
                Prmt = PromoteDict2[PrmtI]
            if T % 2 != 0:
                Prmt = PromoteDict1[PrmtI]
            Board[My, Mx] = Prmt
            Board[Py, Px] = " "
            clear_output(wait=True)
            continue
            
        elif promotecheck() == False:
            None
            
    if T % 2 == 0:
        if tP == "♔":
            Board[My, Mx] = P
            Board[Py, Px] = " "
            clear_output(wait=True)
            BoardImage.show()
            print("Svart Vinner!")
            break
            
    if T % 2 != 0:
        if tP == "♚":
            Board[My, Mx] = P
            Board[Py, Px] = " "
            clear_output(wait=True)
            BoardImage.show()
            print("Vit Vinner!")
            break
    
    else:
        None
              
    Board[My, Mx] = P
    Board[Py, Px] = " "
    
    clear_output(wait=True)

# ---------------------------------------------------------------