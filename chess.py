import numpy as np
import time as time
import os
from IPython.display import clear_output
from PIL import Image, ImageDraw, ImageFont
import math


# Dessa dictionaries har hand om de två sidornas pjäser och används bl.a vid utplacering av pjäser och för att checka vilket lag en viss pjäs tillhör.
# ((Egentligen hade jag lika gärna kunnat ha en vanlig lista över dessa och hade ingen anledning till att göra ett dictionary av det, ...
# ... men då det nu redan är gjort och inte spelar så stor roll + att det skulle kunna användas till något ifall jag vill bygga ut fler funktioner i mitt spel. SÅ låter jag den vara.))
P1 = {"Pawn" : "♙", "Rook" : "♖", "Knight" : "♘", "Bishop" : "♗", "King" : "♔", "Queen" : "♕" }
P2 = {"Pawn" : "♟", "Rook" : "♜", "Knight" : "♞", "Bishop" : "♝", "King" : "♚", "Queen" : "♛" }

# Dessa dictionaries har hand om de pjäser en bonde kan promotas till.
PromoteDict1 = {"Torn" : "♖", "Häst" : "♘", "Löpare" : "♗", "Drottning" : "♕"}
PromoteDict2 = {"Torn" : "♜", "Häst" : "♞", "Löpare" : "♝", "Drottning" : "♛"}

# Dessa dictionaries har hand om "kodningen" för rutorna och dess korresponderande plats i arrayen, d.v.s "a2" = "0, 6" // "e5" = "4, 3"
SqCodeX = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
SqCodeY = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}

# Detta dictionary har hand om bokstäverna som placeras ut på brädets (bilden) ram. Den är i princip identiskt med dictionary (SqCodeX) men dess keys och values har bytt plats...
# , ...anledningen till att jag gjorde ett nytt för detta var för läsbarhet och min egen skull (lättare att förstå)
LettersDict = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}

# Detta dictionary används för att koppla pjäserna på i arrayen till pjäsernas korresponderande bilder som ska användas på spelbrädet (bilden).
# Pjäsernas bilder har varsitt specifikt namn som måste kallas i en viss for loop när bilderna ska klistras in på brädets bild, detta dictionary gör just det möjligt.
PiecesImgDict = {"♙" : "WhP.png", "♟" : "BlP.png", "♖" : "WhR.png", "♜" : "BlR.png", "♘" : "WhKn.png", "♞" : "BlKn.png", 
                 "♗" : "WhB.png", "♝" : "BlB.png", "♔" : "WhK.png", "♚" : "BlK.png", "♕" : "WhQ.png", "♛" : "BlQ.png"}

# ---------------------------------------------------------------

def playerturn():
    
    """Denna funtkion tar fram vilken spelares tur det är, vit eller svart. 
    Den returnar även vilken tid den spelaren har kvar, genom variabler skapade i de 2 nästkommande funktioner."""
    
    global T
    
    if T % 2 == 0:
        return ("Svart spelares tur: {}:{} tid kvar".format(bTMin, bTSec))
    if T % 2 != 0:
        return("Vit spelares tur: {}:{} tid kvar".format(wTMin, wTSec))

def playertime():
    
    """Denna funktion räknar ut i sekunder vilken tid varje spelare har kvar."""
    
    global T
    global wT
    global bT
    
    if T % 2 == 0:
        bT -= TotTime
    if T % 2 != 0:
        wT -= TotTime

def converttime():
    
    """Denna funktion konverterar tiden framtagen i ovanstående funktion, från sekunder till minuter och sekunder, 
    (format: "xx:xx"). Den gör minutrarna till en variabel och sekundrarna till en annan."""
    
    global wT
    global wTMin
    global wTSec
    global bT
    global bTMin
    global bTSec
    
    bTMin = math.floor(bT/60)
    bTSec = round(((bT/60) - (bTMin)) * 60)
    if bTSec < 10:
        bTSec = str(bTSec)
        bTSec = "0"+bTSec
    else:
        None
    
    wTMin = math.floor(wT/60)
    wTSec = round(((wT/60) - (wTMin)) * 60)
    if wTSec < 10:
        wTSec = str(wTSec)
        wTSec = "0"+wTSec
    else:
        None

# ---------------------------------------------------------------

def legalmove1():
    
    """Denna funktionen ska se så att man inte försöker flytta en motståndarpjäs"""
    
    if T % 2 == 0:
        if P in P2.values():
            return True
        elif P in P1.values():
            return False
        
    if T % 2 != 0:
        if P in P1.values():
            return True
        elif P in P2.values():
            return False

# ---------------------------------------------------------------

def legalmove2():
    
    """Denna funktion bestämmer ifall ett förflyttningen av en bestämd pjäs är lagligt.
    T.ex får torn endast flyttas antingen i x-led eller i y-led. Löpare får endast flyttas diagonalt. O.S.V"""
    
    global P
    global Mx
    global My
    global Px
    global Py
    global LastMoveY
    global LastMoveX
    global enpassent
    global tower
    
    enpassent = False
    tower = False
    
    towermove()
    if towermove() == True:
        tower = True
        return True
    elif towermove() == False:
        None
        
    enpassentcheck()
    if enpassentcheck() == True:
        enpassent = True
        return True
    elif enpassentcheck() == False:
        None
    
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
        elif Py != 6:
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
        elif Py != 1:
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

def legalmove3():
    
    """Denna funktion kollar så att draget inte landar pjäsen på en ruta med en pjäs AV SAMMA FÄRG och...
    ... så att den flyttade pjäsen inte passerar genom en pjäs och...
    ... så att den flyttade pjäsen faktiskt flyttas någonstans och inte står kvar där den startade"""
    
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
            
    elif T % 2 != 0:
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
    
    elif P == "♗" or P == "♝" or P == "♕" or P == "♛":
        
        if (abs(Mx - Px) == abs(My - Py)):
            
            if xdelta >= 2 and ydelta >= 2:
                for i in range(xdelta):
                    if i == 0:
                        continue
                    if Board[(Py + i), (Px + i)] in P1.values() or Board[(Py + i), (Px + i)] in P2.values():
                        return False
                    else:
                        None
            elif xdelta >= 2 and ydelta <= -2:
                for i in range(xdelta):
                    if i == 0:
                        continue
                    if Board[(Py - i), (Px + i)] in P1.values() or Board[(Py - i), (Px + i)] in P2.values():
                        return False
                    else:
                        None
            elif xdelta <= -2 and ydelta >= 2:
                for i in range(ydelta):
                    if i == 0:
                        continue
                    if Board[(Py + i), (Px - i)] in P1.values() or Board[(Py + i), (Px - i)] in P2.values():
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
    
def promotecheck():
    
    """Den här funktionen används för att kolla om en bonde har "tillståndet" att promotas, 
    d.v.s att den står på sista ranken / raden relativt till sin ursprungliga rad."""
    
    global My
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

def enpassentcheck():
    
    """Vissa lagliga drag är inte godkända i huvud-funktionen för lagliga drag. Denna funktion kollar om ett kallat drag är
    i form av enpassent (ett av 2 sådana drag) och ifall det ÄR lagligt, isåfall godkänns det. Om detta drag görs behöver
    även flyttandet av pjäserna ske annorlunda och då skapas en variabel som heter "enpassent", ifall denna variabel är True
    så vet programmet att detta speciella drag har genomförts och flyttar pjäser i enlighet därmed."""
    
    global T
    global P
    global Px
    global Py
    global Mx
    global My
    
    global LastPiece
    global LastMoveX
    global LastMoveY
    
    if P == "♟" and Py == 4:
        if (LastPiece == "♙") and ((LastMoveX == Px + 1) or (LastMoveX == Px - 1)) and LastMoveY == 4:
            if ((Mx == Px + 1) or (Mx == Px - 1)) and (My == Py + 1):
                return True
                enpassent = True
            else:
                return False
                enpassent = False
        else:
            None
    if P == "♙" and Py == 3:
        if (LastPiece == "♟") and ((LastMoveX == Px + 1) or (LastMoveX == Px - 1)) and LastMoveY == 3:
            if ((Mx == Px + 1) or (Mx == Px - 1)) and (My == Py - 1):
                return True
                enpassent = True
            else:
                return False
                enpassent =  False
    else:
        return None

# -----------------------------------------

def enpassentupdate():
    
    """Denna funktion (likt towerupdate()) genom det speciella draget en passent. I en passent kallar man bara på att 
    flytta en bonde till en viss ruta MEN en bonde på en onämnd ruta blir även captured/tagen. Denna funktion
    gör så att den onämnda bonden blir captured/tagen."""
    
    global tower
    global LastMoveY
    global LastMoveX
    
    if enpassent == True:
        Board[LastMoveY, LastMoveX] = " "
    else:
        None

# -----------------------------------------

def towercheck():
    
    """Denna funktion håller koll på de faktorer som bestämmer ifall draget rokad (tower på engelska) är tillgängligt. 
    Genom att räkna ifall kungen eller tornen har flyttas kan en annan funktion senare godkänna draget.
    Därefter kan ännu en annan funktion genomföra draget, då det är (likt en passent) ett specialfall."""
    
    global WKMoves
    global BKMoves
    global WR1Moves
    global WR2Moves
    global BR1Moves
    global BR2Moves
    
    if P == "♔":
        WKMoves += 1
    if P == "♚":
        BKMoves += 1
    if Py == 7 and Px == 0:
        WR1Moves += 1
    if Py == 7 and Px == 7:
        WR2Moves += 1
    if Py == 0 and Px == 0:
        BR1Moves += 1
    if Py == 0 and Px == 7:
        BR2Moves += 1

# -------------------------------------

def towermove():
    
    """Denna funktionen kollar ifall ett kallat drag är i form av rokad, om det är lagligt och isåfall godkänner det."""
    
    if P == "♔":
        if (My == 7) and (Mx == 2):
            if (WKMoves == 0) and (WR1Moves == 0) and (Board[7, 3] not in P1.values()) and (Board[7, 3] not in P2.values()) and (Board[7, 1] not in P1.values()) and (Board[7, 1] not in P2.values()):
                return True
            else:
                return False
        elif (My == 7) and (Mx == 6) and (Board[7, 5] not in P1.values()) and (Board[7, 5] not in P2.values()):
            if (WKMoves == 0) and (WR2Moves == 0):
                return True
            else:
                return False
        else:
            return None
    if P == "♚":
        if (My == 0) and (Mx == 2):
            if (BKMoves == 0) and (BR1Moves == 0) and (Board[0, 3] not in P1.values()) and (Board[0, 3] not in P2.values()) and (Board[0, 1] not in P1.values()) and (Board[0, 1] not in P2.values()):
                return True
            else:
                return False
        elif (My == 0) and (Mx == 6) and (Board[0, 5] not in P1.values()) and (Board[0, 5] not in P2.values()):
            if (BKMoves == 0) and (BR2Moves == 0):
                return True
            else:
                return False
        return None

# ----------------------------------------

def towerupdate():
    
    """Denna funktion genomför det speciella draget rokad. I rokad kallar man på att flytta kungen MEN ett av tornen 
    kommer också flyttas. Denna funktionen flyttar även tornet."""
    
    global tower
    global Board
    global P
    global Mx
    
    if tower == True:
        if (P == "♔") and (Mx == 2):
            Board[7, 0] = " "
            Board[7, 3] = "♖"
        if (P == "♔") and (Mx == 6):
            Board[7, 7] = " "
            Board[7, 5] = "♖"
        if (P == "♚") and (Mx == 2):
            Board[0, 0] = " "
            Board[0, 3] = "♜"
        if (P == "♚") and (Mx == 6):
            Board[0, 7] = " "
            Board[0, 5] = "♜"
    elif tower == False:    
        Board[My, Mx] = P
        Board[Py, Px] = " "

# -------------------------------------

def boardmaker():
    
    """Denna funktion skapar brädet som i sin tur används för att hålla koll på alla pjäser och om drag är lagliga. 
    Det bräde som denna funktion skapar är hela spelets grund och allting baseras på detta."""
    
    global Board
    
    Board = np.full((8, 8), " ")

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

# -------------------------------------------

def ChessBoardImg():
    
    """Denna funktion skapar brädet i form av en bild (filformat: .png)"""
    
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
        
        borderimg = ImageDraw.Draw(img)
        borderfont = ImageFont.truetype("Castoro-Regular.ttf", 30)
        
        for i in range(8):
            borderimg.text(((90 + 100*i), 10), LettersDict[i], fill=(255, 255, 255), font=borderfont)
            borderimg.text(((90 + 100*i), 860), LettersDict[i], fill=(255, 255, 255), font=borderfont)
            borderimg.text((20, (85 + 100*i)), str(8-i), fill=(255, 255, 255), font=borderfont)
            borderimg.text((870, (85 + 100*i)), str(i+1), fill=(255, 255, 255), font=borderfont)
        
        img.save("ChessBoard.png")

# ------------------------------------------

def BoardPieces():
    
    """Denna funktion använder Board[]-arrayen för att redigera ChessBoard.png-bilden skapad i en annan funktion. 
    Genom att iterera över arrayen kan den studera vilka pjäser som är vart och sedan paste-a in bilder på pjäserna
    på ChessBoard.png"""
    
    global Board
    
    with Image.open("ChessBoard.png") as img:
        
        for i in range(8):
            for j in range(8):
                Piece = Board[i, j]
                if Piece == " ":
                    continue
                PieceImgLink = str(PiecesImgDict[Piece])
                PieceImg = Image.open(PieceImgLink)
                img.paste(PieceImg, (50 + (100*j), 50 + (100*i)), PieceImg)
        img.save("ChessBoard.png")

# ----------------------------------------

def BoardUpdater():
    
    """Denna funktion uppdaterar brädet efter varje drag. Eftersom man inte vill behöva iterera över hela brädet
    varje gång ett drag görs kollar denna funktion vilka rutor som är annorlunda från innan och 
    uppdaterar sedan ENDAST dem."""
    
    global Board
    global PrevBoard
    global changelist
    
    changelist = []
    for i in range(8):
        for j in range(8):
            if PrevBoard[i, j] != Board[i, j]:
                changelist.append((i, j))
            else:
                None
       
    with Image.open("ChessBoard.png") as img:
        for i in range(len(changelist)):
            
            SQ = changelist[i]
            Y = SQ[0]
            X = SQ[1]
            Piece = Board[SQ]
            
            if ((Y + 1) % 2 != 0) and ((X + 1) % 2 == 0) or ((Y + 1) % 2 == 0) and ((X + 1) % 2 != 0):
                colour = (106, 161, 33)
            elif ((Y + 1) % 2 == 0) and ((X + 1) % 2 == 0) or ((Y + 1) % 2 != 0) and ((X + 1) % 2 != 0):
                colour = (211, 211, 211)
                
            for y in range(100):
                for x in range(100):
                    img.putpixel(((x + 50 + (100*X)), y + 50 + (100*Y)), (colour))
                        
            if (Piece in P1.values()) or (Piece in P2.values()):
                PieceImgLink = str(PiecesImgDict[Piece])
                PieceImg = Image.open(PieceImgLink)
                img.paste(PieceImg, (50 + (100*X), 50 + (100*Y)), PieceImg)
            else:
                None
    img.save("ChessBoard.png")

# ---------------------------------------

"""I denna kernel/del av koden, spelas själva spelet. Spelet i sig är en While-loop där varannan iteration är
vit spelares tur och varannan är svart spelares tur. Det är här funktionerna appliceras genom att kallas på, 
på olika sätt vid olika tillfällen."""

# Här byggs/resetas brädet.
boardmaker()
# Här skapas png-bilden som representerar brädet.
ChessBoardImg()
# Här placeras pjäserna ut på png-bilden i fråga.
BoardPieces()

#Här under skapas/resetas olika variabler som används under spelets gång.
T = 0

wT = 600
bT = 600

WKMoves = 0
BKMoves = 0
WR1Moves = 0
WR2Moves = 0
BR1Moves = 0
BR2Moves = 0

# Här är loopen som ÄR själva spelet. 
while True:
    
    # Här öppnas png-bilden i fråga, så att den kan nås och kallas på under spelets gång.
    BoardImage = Image.open("ChessBoard.png")
    # Här visas bilden i fråga
    BoardImage.show()
    
    # Här kallas funktionen som gör om den kvarstående tiden till min:sek
    converttime()
    
    # Här startas timern som används i vissa funktioner.
    start = time.time()
    T += 1
    # Här printas vems tur det är
    print(playerturn())
    
    # Här frågas spelaren om vilken pjäs de ska flytta (rutan pjäsen står på)
    print("Vilken pjäs ska du flytta?")
    Pp1 = [*input()]
    Px = int(SqCodeX[Pp1[0]])
    Py = int(SqCodeY[Pp1[1]])
    
    # Här frågas spelaren om vart de ska flytta pjäsen.
    print("Vart ska pjäsen flyttas?")
    Pp2 = [*input()]
    Mx = int(SqCodeX[Pp2[0]])
    My = int(SqCodeY[Pp2[1]])
    
    # Här stoppas timern. Tiden det tog att genomföra draget bestäms.
    end = time.time()
    TotTime = int(end - start)
    
    # Funktionen som räknar ut tiden kvar kallas.
    playertime()
    
    # Om tiden för en spelare har nått 0 innan spelaren hann göra sitt drag, vinner den andra spelaren.
    if bT <= 0:
        print("Tiden är ute för svart spelare. Vit spelare vinner!")
        break
    elif wT <= 0:
        print("Tiden är ute för vit spelare. Svart spelare vinner!")
        break
    else:
        None
    
    # Här bestäms några andra variabler som inte kunde bestämmas tidigare.
    P = Board[Py, Px]
    tP = Board[My, Mx]
    
    # Här kallas första funktionen som ska kolla om ett drag är lagligt. Om det inte är det tvingas spelaren försöka igen.
    legalmove1()
    if legalmove1() == True:
        None
    elif legalmove1() == False:
        clear_output(wait=True)
        print("Du kan inte flytta en motståndarpjäs. Försök igen")
        T -= 1
        continue
    
    # Här kallas andra funktionen som ska kolla om ett drag är lagligt. Om det inte är det tvingas spelaren försöka igen.
    legalmove2()
    if legalmove2() == True:
        None
    elif legalmove2() == False:
        clear_output(wait=True)
        print("Olagligt drag. Försök igen.")
        T -= 1
        continue
    
    # Här kallas tredje funktionen som ska kolla om ett drag är lagligt. Om det inte är det tvingas spelaren försöka igen.
    legalmove3()
    if legalmove3() == True:
        None
    elif legalmove3() == False:
        clear_output(wait=True)
        print("Olagligt drag. Försök igen.")
        T -= 1
        continue
    
    # Här checkar spelet ut om en bonde är vid sjunde ranken/raden och ska därmed promotas och vad den ska promotas till.
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
    
    # Här kollar spelet om motståndarens kung blev tagen. Isåfall vinner spelaren som tog motståndar-kungen. 
    # (Egentligen tar man aldrig kungen i schack, utan man vinner genom att ställa sig i en position där kungen... 
    # ...KOMMER ATT BLI tagen nästa drag oavsett vad hen gör. Men p.g.a av hur jag skrev min kod blev det väldigt svårt att göra.)
    if T % 2 == 0:
        if tP == "♔":
            Board[My, Mx] = P
            Board[Py, Px] = " "
            clear_output(wait=True)
            
            BoardUpdater()
            BoardImage = Image.open("ChessBoard.png")
            BoardImage.show()
            
            print("Svart spelare vinner!")
            break          
    if T % 2 != 0:
        if tP == "♚":
            Board[My, Mx] = P
            Board[Py, Px] = " "
            clear_output(wait=True)
            
            BoardUpdater()
            BoardImage = Image.open("ChessBoard.png")
            BoardImage.show()
            
            print("Vit spelare vinner!")
            break
    
    else:
        None
    
    # Här skapas en till variabel som inte kunde skapas tidigare. Variabeln respresenterar i nästa iteration av loopen, 
    # ... den föregående verisonen av brädet.
    PrevBoard = Board.copy()
    
    # Här kallas funktionerna som updaterar brädet på ett speciellt sätt OM det speciella draget gjorts.
    towerupdate()
    enpassentupdate()
    
    # Här görs draget man kallade på. 
    Board[My, Mx] = P
    Board[Py, Px] = " "
       
    # Här skapas ännu fler variabler som kanske ska användas vid nästa iteration.
    LastPiece = P
    LastMoveX = Mx
    LastMoveY = My
    
    #Här kallas funktionen som håller koll på ifall rokad är tillgängligt, 
    # ... genom att räkna hur många gånger ett visst torn eller en viss kung flyttas.
    towercheck()
    
    # Här kallas funktione som uppdaterar png-bilden av brädet.
    BoardUpdater()
    
    # Här rensas alla output från denna iteration så att nästa output inte är fylld av två iterationer.
    clear_output(wait=True)