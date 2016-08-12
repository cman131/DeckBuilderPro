from app import dbconnect
from app import config
from flask import json

cursor, connection = dbconnect.connection(config)

class Card:
    def __init__(self, id, name, multiverseid, manacost, cmc, colors, types, supertypes,
                 subtypes, rarity, text, flavor, artist, number, power, toughness, layout,
                 imagename):
        self.id = id
        self.name = name
        self.multiverseid = multiverseid
        self.manacost = manacost
        self.cmc = cmc
        self.colors = colors
        self.types = types
        self.supertypes = supertypes
        self.subtypes = subtypes
        self.rarity = rarity
        self.text = text
        self.flavor = flavor
        self.artist = artist
        self.number = number
        self.power = power
        self.toughness = toughness
        self.layout = layout
        self.imagename = imagename

    def save(self):
        try:
            data = [self.id, self.name, self.multiverseid, self.manacost, int(self.cmc), json.dumps(self.colors),
                    json.dumps(self.types), json.dumps(self.supertypes), json.dumps(self.subtypes), self.rarity,
                    self.text, self.flavor, self.artist, self.number, self.power, self.toughness, self.layout, self.imagename]
            command = ('INSERT INTO Card (id, name, multiverseid, manacost, cmc, colors, types, supertypes, ' +
                        'subtypes, rarity, text, flavor, artist, number, power, toughness, layout, imagename) ' +
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);')
            cursor.execute(command, data)
            connection.commit()
        except Exception:
            return self.name
        return ''

    @staticmethod
    def load(id):
        data = [id]
        command = ('SECLECT * FROM Card WHERE id=%s;')
        cursor.execute(command, data)
        result = cursor.fetchall()[0]
        return Card(id, result['name'], result['multiverseid'], result['manacost'], result['cmc'],
                    json.loads(result['colors']), json.loads(result['types']), json.loads(result['supertypes']),
                    json.loads(result['subtypes']), result['rarity'], result['text'], result['flavor'], result['artist'],
                    result['number'], result['power'], result['toughness'], result['layout'], result['imagename'])
    @staticmethod
    def clear(yaSure):
        if yaSure=='DOIT':
            command = ('DELETE FROM Card WHERE id!=%s')
            cursor.execute(command, ['0'])
            connection.commit()

class Deck:
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    description = db.Column(db.String(45))
    size = db.Column(db.String(45))
    black = db.Column(db.Integer)
    blue = db.Column(db.Integer)
    green = db.Column(db.Integer)
    red = db.Column(db.Integer)
    white = db.Column(db.Integer)
    publicity = db.Column(db.Integer)
    """

    def __init__(self, id, name, description, size, colors, publicity, cardList=[]):
        self.id = id
        self.name = name
        self.size = size
        self.description = description
        self.black = 1 if int(colors['black']) > 0 else 0
        self.blue = 1 if int(colors['blue']) > 0 else 0
        self.green = 1 if int(colors['green']) > 0 else 0
        self.red = 1 if int(colors['red']) > 0 else 0
        self.white = 1 if int(colors['white']) > 0 else 0
        self.publicity = publicity
        self.cardList = cardList

    def __dict__(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'size': self.size,
                'colors': {'black':self.black, 'blue':self.blue, 'green':self.green, 'red':self.red, 'white':self.white},
                'cardList': self.cardList}

    def __repr__(self):
        return '<Deck %r>' % self.name

    def getDetailedCardList(self):
        retVal = {'cards': [], 'swamp': 0, 'island': 0, 'mountain': 0, 'forest': 0, 'plains': 0}
        for card in self.cardList:
            if(card['cardId'] == 'swamp' or card['cardId'] == 'island' or card['cardId'] == 'forest' or card['cardId'] == 'mountain'
                    or card['cardId'] == 'plains'):
                retVal[card['cardId']] = card['count']
            else:
                command = ('SELECT * FROM Card WHERE id=%s;')
                cursor.execute(command, [card['cardId']])
                fullCard = cursor.fetchall()[0]
                fullCard['count'] = card['count']
                retVal['cards'].append(fullCard)
        return retVal

    def save(self):
        data = [self.name, self.description, int(self.size), int(self.black), int(self.blue),
                int(self.green), int(self.red), int(self.white),
                int(self.publicity)]
        command = ('INSERT INTO Deck (name, description, size, ' +
                    'black, blue, green, red, white, publicity) ' +
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);')
        if(self.id != None):
            data.append(int(self.id))
            command = ('UPDATE Deck SET name=%s' +
                        ', description=%s' +
                        ', size=%s' +
                        ', black=%s' +
                        ', blue=%s' +
                        ', green=%s' +
                        ', red=%s' +
                        ', white=%s' +
                        ', publicity=%s' +
                        ' WHERE id=%s;')
        cursor.execute(command, data)
        connection.commit()
        self.id = self.id if self.id is not None else connection.insert_id()
        if self.cardList!=[]:
            command1 = ('DELETE FROM Deck_Card WHERE deckId=%s;')
            data1 = [self.id]
            command2 = ''
            data2 = []
            for card in self.cardList:
                command2 += 'INSERT INTO Deck_Card (deckId, cardId, count) VALUES (%s, %s, %s);'
                data2.append(self.id)
                data2.append(card['id'])
                data2.append(card['count'])
            command2 = (command2)
            cursor.execute(command1, data1)
            cursor.execute(command2, data2)
            connection.commit()
        return True

    #Static Methods

    @staticmethod
    def all():
        cursor.execute('SELECT * FROM Deck;')
        return cursor.fetchall()

    @staticmethod
    def get(id):
        cursor.execute('SELECT * FROM Deck WHERE id=%s;', [int(id)])
        result = cursor.fetchall()[0]
        cursor.execute('SELECT cardId,count FROM Deck_Card WHERE deckId=%s;', [int(id)])
        cardList = cursor.fetchall()
        return Deck(
            id,
            result['name'],
            result['description'],
            result['size'],
            {
                'black':result['black'],
                'blue':result['blue'],
                'green':result['green'],
                'red':result['red'],
                'white':result['white']
                        },
            result['publicity'],
            cardList)

    @staticmethod
    def search(term, colors):
        term = '%'+term+'%'
        colorNames = ['black', 'blue', 'green', 'red', 'white']
        colorstr = ''
        for color in colorNames:
            if colors[color]==1:
                colorstr += ' AND '+color+'=1'
        command = ('SELECT * FROM Deck WHERE (name like %s OR description like %s) AND (publicity=1'+colorstr+');')
        data = [term, term]
        cursor.execute(command, data)
        return cursor.fetchall()