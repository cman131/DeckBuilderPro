import uuid, json

class TableTopSerializable:
    def __init__(self):
        pass

    def getJsonSerializable(self):
        newDic = self.__dict__
        for key,val in self.__dict__.items():
            if isinstance(val, TableTopSerializable):
                newDic[key] = val.getJsonSerializable()
            elif isinstance(val, list) and len(val) > 0 and isinstance(val[0], TableTopSerializable):
                newDic[key] = [x.getJsonSerializable() for x in val]
            elif isinstance(val, dict):
                for k,v in val.items():
                    newDic[key][k] = v.getJsonSerializable()
        return newDic
    def getJson(self):
        return json.dumps(self.getJsonSerializable())

class TableTopSave(TableTopSerializable):

    def __init__(self, objects = []):
        self.SaveName = ""
        self.GameMode = ""
        self.Date = ""
        self.Table = ""
        self.Sky = ""
        self.Note = ""
        self.Rules = ""
        self.PlayerTurn = ""
        self.ObjectStates = objects

    def addObject(self, objectState):
        self.ObjectStates.append(objectState)

class TableTopObjectState(TableTopSerializable):
    def __init__(self, name, description):
        self.Name = "DeckCustom"
        self.Nickname = name
        self.Description = description
        self.Grid = True
        self.Locked = False
        self.SidewaysCard = False
        self.GUID = uuid.uuid4().__str__()
        self.ColorDiffuse = TableTopColor(0.713235259, 0.713235259, 0.713235259)
        self.DeckIDs = []
        self.Transform = TableTopTransform(2.5, 2.5, 0.0, 0, 180, 180, 1.0, 1.0, 1.0)
        self.CustomDeck = {}
        self.ContainedObjects = []

    def addDeck(self, deckUrl, cards = []):
        if (len(cards) > 69):
            raise Exception("No! only 69 cards in a deck.")

        deckId = len(self.CustomDeck) + 1
        self.CustomDeck[deckId] = TableTopDeck(deckUrl)
        ind = 0
        for card in cards:
            cardId = str(deckId) + (str(ind + 1) if ind + 1 >= 10 else "0"+str(ind + 1))
            self.DeckIDs.append(cardId)
            self.ContainedObjects.append(TableTopCard(card, cardId))
            ind += 1

class TableTopColor(TableTopSerializable):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class TableTopTransform(TableTopSerializable):
    def __init__(self, posX, posY, posZ, rotX, rotY, rotZ, scaleX, scaleY, scaleZ):
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.scaleZ = scaleZ

class TableTopDeck(TableTopSerializable):
    def __init__(self, faceUrl):
        self.FaceURL = faceUrl
        self.BackURL = "http://i.imgur.com/P7qYTcI.png"

class TableTopCard(TableTopSerializable):
    def __init__(self, name, cardId):
        self.Name = "Card"
        self.Nickname = name
        self.CardID = cardId
        self.Transform = TableTopTransform(2.5, 2.5, 3.5, 0, 180, 180, 1.0, 1.0, 1.0)