# -----------------------------------------------------------------¨

# Denna kernel har hand om mina imports och dictionaries, detta för att hålla dem organiserade. 

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
    # , anledningen till att jag gjorde ett nytt för detta var för läsbarhet och min egen skull (lättare att förstå)
LettersDict = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}

    # Detta dictionary används för att koppla pjäserna på i arrayen till pjäsernas korresponderande bilder som ska användas på spelbrädet (bilden).
    # Pjäsernas bilder har varsitt specifikt namn som måste kallas i en viss for loop när bilderna ska klistras in på brädets bild, detta dictionary gör just det möjligt.
PiecesImgDict = {"♙" : "WhP.png", "♟" : "BlP.png", "♖" : "WhR.png", "♜" : "BlR.png", "♘" : "WhKn.png", "♞" : "BlKn.png", 
                 "♗" : "WhB.png", "♝" : "BlB.png", "♔" : "WhK.png", "♚" : "BlK.png", "♕" : "WhQ.png", "♛" : "BlQ.png"}

# ---------------------------------------------------------------

    # Denna funtkion tar fram vilken spelares tur det är, vit eller svart. Denna returnar även vilken tid den spelaren har kvar, genom variabler skapade i de 2 nästkommande funktioner.

def playerturn():
    
    global T
    
    if T % 2 == 0:
        return ("Svart spelares tur: {}:{} tid kvar".format(bTMin, bTSec))
    if T % 2 != 0:
        return("Vit spelares tur: {}:{} tid kvar".format(wTMin, wTSec))
    
    # Denna funktion räknar ut i sekunder vilken tid varje spelare har kvar.

def playertime():
    
    global T
    global wT
    global bT
    
    if T % 2 == 0:
        bT -= TotTime
    if T % 2 != 0:
        wT -= TotTime
        
    # Denna funktion konverterar tiden framtagen i ovanstående funktion, från sekunder till minuter och sekunder (format: "xx:xx"). Den gör minutrarna till en variabel och sekundrarna till en annan.

def converttime():
    
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

# Här kollar funktionen så att draget inte landar pjäsen på en ruta med en pjäs AV SAMMA FÄRG och...
# ... så att den flyttade pjäsen inte passerar genom en pjäs och...
# ... så att den flyttade pjäsen faktiskt flyttas någonstans och inte står kvar där den startade

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

# Denna funktion kollar och bestämmer ifall ett drags förflyttning är lagligt

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
    
# Denna funtkion ska kolla ifall en pjäs har nått sista raden på brädet (relativt till vart den startade d.v.s vit pjäs eller svart pjäs)...
# ... för att sedan kunna promotas (alltså att pjäsen byts ut mot en pjäs (inte bonde eller kung))

def promotecheck():
    
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

# Denna funktion skapar brädet och rutornas numreringar, den placerar även ut pjäserna. Ifall en match har spelats använts bl.a funktionen till att "reseta" brädet.

def boardmaker():
    
    global Board
    
    Board = np.full((8, 8), " ")

    # Här placeras pjäserna

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

# Denna funktion gör brädet till en bild som man kan spela på (istället för en array). 

def ChessBoardImg():
    
    global Board
    global P
    
    # Här skapas brädet och dess rutor
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
        
        # Här skapas ramen kring brädet och axel-numreringarna (d.v.s a,b,c... och 1,2,3...) 
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

# ---------------------------------

# Denna funktion placerar ut pjäserna och är den som uppdaterar pjäsernas position efter ett drag. Detta görs genom att iterera över hela brädet och...
# ... kolla vart det står pjäser och vad för pjäser det är. 
    
    # ((Jag tror att jag kan optimisera denna något genom att göra så att den endast kollar de rutor som har påverkats under draget...
    #, d.v.s rutan där pjäsen som flyttades stod på och rutan den flyttades till.))

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
                    PieceImgLink = str(PiecesImgDict[Piece])
                    PieceImg = Image.open(PieceImgLink)
                    img.paste(PieceImg, (50 + (100*j), 50 + (100*i)), PieceImg)
        img.save("ChessBoard.png")

# ---------------------------------

# I denna kernel och While loop spelas själva spelet, här kallas de olika funktionerna och spelet påverkas beroende på vad funktionerna returnar.

    # Här kallas 2 funktioner för att reseta brädets array (som har hand om reglerna) och brädets bild.
boardmaker()
ChessBoardImg()

    # Här bestäms / resetas variabeln som har hand om vems tur det är (rond-nummer)
T = 0

    # Här bestäms / resetas varaiblerna som har hand om hur mycket tid varje spelare har på sig.
wT = 600
bT = 600

    # här startas loopen som ÄR spelet.
while True:
    
        # Här öppnas det skapade schack-brädet och uppdateras efter hur schack-brädet ser just nu.
    BoardPieces()
    BoardImage = Image.open("ChessBoard.png")
    BoardImage.show()

        # Här konverteras den återstående tiden till min:sek
    converttime()
    
        # Här startas timern som används vid tids-bestämning och vems tur det är printas
    start = time.time()
    T += 1
    print(playerturn())
        
        # Här frågas spelaren vilken pjäs (positionen för pjäsen) som ska flyttas, och variablerna för start-postionen bestäms.
    print("Vilken pjäs ska du flytta?")
    Pp1 = [*input()]
    Px = int(SqCodeX[Pp1[0]])
    Py = int(SqCodeY[Pp1[1]])

        # Här frågas spelaren vart pjäsen ska flyttas, och variablerna för flytt-positionen bestäms.
    print("Vart ska pjäsen flyttas?")
    Pp2 = [*input()]
    Mx = int(SqCodeX[Pp2[0]])
    My = int(SqCodeY[Pp2[1]])
    
        # Här stannas tiden / timern och kvarstående tid beräknas. Här kollas även ifall tiden har gått under 0, d.v.s gått ut och spelaren vars tid gick ut förlorar.
    end = time.time()
    TotTime = int(end - start)
    playertime()
    if bT <= 0:
        print("Tiden är ute för svart spelare. Vit spelare vinner!")
    elif wT <= 0:
        print("Tiden är ute för vit spelare. Svart spelare vinner!")
    else:
        None
    
        # Här bestäms vad för pjäs som flyttas och vad för pjäs (eller "tomhet") som pjäsen flyttas till.
    P = Board[Py, Px]
    tP = Board[My, Mx]
    
        # De 3 nästkommande funktionerna kollar ifall draget är lagligt.
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
        print("Olagligt drag. Försök igen. ")
        T -= 1
        continue

    legalmove1()
    if legalmove1() == True:
        None
    elif legalmove1() == False:
        clear_output(wait=True)
        print("Olagligt drag. Försök igen. ")
        T -= 1
        continue

        # Här kollas ifall den flyttade pjäsen är en bonde och om den ska promotas, och isåfall vad för pjäs den ska promotas till.
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

        # Här kollas ifall någon spelare har tagit en kung, d.v.s vunnit, och isåfall vinner den spelaren.
        # ((Egentligen tar man aldrig kungen i schack men då det var svårt att koda det "riktiga sättet", speciellt p.g.a hur jag har skrivit min kod, fick det här duga.))        
    if T % 2 == 0:
        if tP == "♔":
            Board[My, Mx] = P
            Board[Py, Px] = " "
            clear_output(wait=True)
            
            BoardPieces()
            BoardImage = Image.open("ChessBoard.png")
            BoardImage.show()
            
            print("Svart spelare vinner!")
            break
            
    if T % 2 != 0:
        if tP == "♚":
            Board[My, Mx] = P
            Board[Py, Px] = " "
            clear_output(wait=True)
            
            BoardPieces()
            BoardImage = Image.open("ChessBoard.png")
            BoardImage.show()
            
            print("Vit spelare vinner!")
            break
    
    else:
        None

        # Efter att draget är bekräftat görs själva draget här.          
    Board[My, Mx] = P
    Board[Py, Px] = " "
    
    clear_output(wait=True)

# ---------------------------------------------------------------