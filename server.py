from flask import Flask, request, render_template, send_file, Response
import re
import json
import requests
import os

def findCard(s):
    name = s
    url = "https://api.scryfall.com/cards/search?q="
    
    #check if "  Flip" in s
    if name.endswith("  Flip\r"):
        name = name[:-7]
        print(name)
    
#Get The Site with Requests
    r = requests.get(url+'!"' + name + '"')
    cardBack = "https://static.wikia.nocookie.net/mtgsalvation_gamepedia/images/f/f8/Magic_card_back.jpg/revision/latest/scale-to-width-down/429?cb=20140813141013"
    doubleFaces = False
    
    
    #check if card was found
    if r.json()['object']=='error':
        return False
    
    #check if card has a backside
    if r.json()['data'][0]['layout']=="transform" or r.json()['data'][0]['layout']=="modal_dfc":
        cardName=r.json()['data'][0]['name']
        cardFront=r.json()['data'][0]['card_faces'][0]['image_uris']['png']
        cardBack=r.json()['data'][0]['card_faces'][1]['image_uris']['png']
        doubleFaces = True
        return cardName, cardFront, cardBack, doubleFaces

    
    cardName=r.json()['data'][0]['name']
    cardFront=r.json()['data'][0]['image_uris']['png']

    return cardName, cardFront, cardBack, doubleFaces




def createCard_CustomDeck(frontURL,backURL):
    card={"FaceURL":frontURL,"BackURL":backURL,"NumHeight": 1,"NumWidth": 1,"BackIsHidden": "true"}
    return card

def createCard_ContainedObjects(name,index):
    card={"CardID":index,"Name":"Card","Nickname":name,"Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":1,"scaleY":1,"scaleZ":1}}
    return card

def parse(string):
    retval = ''
    for char in string:
        retval += char if not char == '\n' else ''
        if char == '\n':
            yield retval
            retval = ''
    if retval:
        yield retval


app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('Bardown.html')


def createDeck(f):
    
    defaultBackside = "https://static.wikia.nocookie.net/mtgsalvation_gamepedia/images/f/f8/Magic_card_back.jpg/revision/latest/scale-to-width-down/429?cb=20140813141013"
    
    ContainedObjects=[]
    ContainedObjectsBack=[createCard_ContainedObjects("empty",100)]
    
    DeckIDs = []
    DeckIDsBack = [100]
    
    CustomDeck = {}
    CustomDeckBack = {}
    CustomDeckBack['1'] = createCard_CustomDeck("xxx","xxx")
    
    DoubleFaces={}
    twoBoards=False
    
    
    
    j = 2 #id start for double faced cards
    i = 1 #id start for single faced cards
    
    
    
    for line in f:
        
        
        k=1 #amount of a card
        
        #check the amount
        x_test = re.search("^(\d+)+(x )", line)
        d_test = re.search("\d+ +", line)
        
        x_test_k = re.search("^(\d+)", line)
        d_test_k = re.search("\d+", line)
        
        
        if d_test:
            k = int(d_test_k.group(0))
            print(k)
            s=line.split(d_test.group(0))
            print(s)
            line = s[1]
            print("line ohne x: " + s[1])
        
        if x_test:
            k = int(x_test_k.group(0))
            print(k)
            s=line.split(x_test.group(0))
            print(s)
            line = s[1]
            print("line mit x: " + s[1])
        
                
            

                
        
        
        card = findCard(line)
        while k>0:
            #check if card exists
            if card == False:
                print("Bad Card: "+line)
                k=k-1
                continue
            
            #if card has backside
            if card[3]:
                if not DoubleFaces:
                    twoBoards=True
                    ContainedObjectsBack.append(createCard_ContainedObjects(card[0],j*100))
                    DeckIDsBack.append(j*100)
                    CustomDeckBack[str(j)] = createCard_CustomDeck(card[1],card[2])
                    DoubleFaces = {"Name":"DeckCustom","ContainedObjects":ContainedObjectsBack,"DeckIDs":DeckIDsBack,"CustomDeck":CustomDeckBack,"Transform":{"posX":2,"posY":1,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":1,"scaleY":1,"scaleZ":1}}
                else:
                    ContainedObjectsBack.append(createCard_ContainedObjects(card[0],j*100))
                    DeckIDsBack.append(j*100)
                    CustomDeckBack[str(j)] = createCard_CustomDeck(card[1],card[2])
                j=j+1
            
            
            ContainedObjects.append(createCard_ContainedObjects(card[0],i*100))
            DeckIDs.append(i*100)
            CustomDeck[str(i)] = createCard_CustomDeck(card[1],defaultBackside)
            i=i+1
            k=k-1
        
        
                
                
                
    firstDeck={"Name":"DeckCustom","ContainedObjects":ContainedObjects,"DeckIDs":DeckIDs,"CustomDeck":CustomDeck,"Transform":{"posX":0,"posY":1,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":1,"scaleY":1,"scaleZ":1}}
    
    data={'ObjectStates':[]}
    data['ObjectStates'].append(firstDeck)
    
    if twoBoards:
        data['ObjectStates'].append(DoubleFaces)
    
    #deck = json.loads(data)
    #deck['ObjectStates'][0].append(data)
    
    return data











@app.route('/', methods=['POST'])
def my_form_post():
    deckName = request.form['text']
    deckContent = request.form['deckcontent']
    
    print(deckName)
    
    s = parse(deckContent)
    decklist = json.dumps(createDeck(s))
    
    #f = open("decks/"+deckName+".json", "w")
    #f.write(decklist)
    #f.close()
    
    
    
    
    
    
    return Response(decklist, mimetype="application/json", headers={"Content-disposition":"attachment","filename":deckName+".json"})
