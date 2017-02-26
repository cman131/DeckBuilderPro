from app import dbconnect
from app import config
from flask import json

cursor, connection = dbconnect.connection(config)

class WeissCard:
    def __init__(self, id, name, number, rarity, type, color, level, cost, power, soul, c_trigger, traits, text, flavor, imageurl):
        self.id = id
        self.name = name
        self.number = number
        self.rarity = rarity
        self.type = type
        self.color = color
        self.level = level
        self.cost = cost
        self.power = power
        self.soul = soul
        self.c_trigger = c_trigger
        self.traits = traits
        self.text = text
        self.flavor = flavor
        self.imageurl = imageurl

    def save(self, id=None):
        try:
            data = [self.name, self.number, self.rarity, self.type, self.color, self.level, self.cost,
                    self.power, self.soul, self.c_trigger, self.traits, self.text, self.flavor, self.imageurl, id]
            command = ('INSERT INTO wsdb_eng (name, number, rarity, type, color, level, ' +
                        'cost, power, soul, c_trigger, traits, text, flavor, imageurl, pid) ' +
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);')
            if id != None:
                command = ('UPDATE wsdb_eng SET name=%s' +
                            ', number=%s' +
                            ', rarity=%s' +
                            ', type=%s' +
                            ', color=%s' +
                            ', level=%s' +
                            ', cost=%s' +
                            ', power=%s' +
                            ', soul=%s' +
                            ', c_trigger=%s' +
                            ', traits=%s' +
                            ', text=%s' +
                            ', flavor=%s' +
                            ', imageurl=%s' +
                            ' WHERE pid=%s;')
            cursor.execute(command, data)
            connection.commit()
        except Exception:
            return self.name
        return ''

    # Static Methods

    @staticmethod
    def load(id):
        data = [id]
        command = ('SELECT * FROM wsdb_eng WHERE pid=%s;')
        cursor.execute(command, data)
        results = cursor.fetchall()
        if len(results) == 0:
            return None
        result = results[0]
        return WeissCard(id, result['name'], result['number'], result['rarity'], result['type'],
                    result['color'], result['level'], result['cost'],
                    result['power'], result['soul'], result['c_trigger'], result['traits'], result['text'],
                    result['flavor'], result['imageurl'])

    @staticmethod
    def loadAll(isDict=False):
        data = []
        command = ('SELECT * FROM wsdb_eng;')
        cursor.execute(command, data)
        results = cursor.fetchall()
        if isDict:
            return results
        return [WeissCard(result['pid'], result['name'], result['number'], result['rarity'], result['type'],
                    result['color'], result['level'], result['cost'],
                    result['power'], result['soul'], result['c_trigger'], result['traits'], result['text'],
                    result['flavor'], result['imageurl']) for result in results]

    @staticmethod
    def clear(yaSure):
        if yaSure=='DOIT':
            command = ('DELETE FROM Card WHERE pid!=%s')
            cursor.execute(command, ['0'])
            connection.commit()

    @staticmethod
    def getAllImageless():
        command = ("SELECT * FROM wsdb_eng WHERE imageurl IS NULL;")
        cursor.execute(command, [])
        results = cursor.fetchall()
        return [WeissCard(result['pid'], result['name'], result['number'], result['rarity'], result['type'],
                     result['color'], result['level'], result['cost'], result['power'], result['soul'],
                     result['c_trigger'], result['traits'], result['text'], result['flavor'], '') for result in results]

class WeissSet:
    """
    id = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(100))
    """

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def load(id):
        data = [id]
        command = ('SELECT * FROM WeissSet WHERE id=%s;')
        cursor.execute(command, data)
        results = cursor.fetchall()
        if len(results) <= 0:
            return None
        result = results[0]
        return WeissSet(result['id'], result['name'])

    # Static Methods
    @staticmethod
    def loadAll():
        data = []
        command = ('SELECT * FROM WeissSet;')
        cursor.execute(command, data)
        results = cursor.fetchall()
        return [WeissSet(result['id'], result['name']) for result in results]

class WeissDeck:
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    set = db.column(db.String(45))
    description = db.Column(db.String(45))
    blue = db.Column(db.Integer)
    green = db.Column(db.Integer)
    red = db.Column(db.Integer)
    yellow = db.Column(db.Integer)
    publicity = db.Column(db.Integer)
    """

    def __init__(self, id, name, description, universe, colors, publicity, cardList=[]):
        self.id = id
        self.name = name
        self.description = description
        self.universe = universe
        self.yellow = 1 if int(colors['yellow']) > 0 else 0
        self.blue = 1 if int(colors['blue']) > 0 else 0
        self.green = 1 if int(colors['green']) > 0 else 0
        self.red = 1 if int(colors['red']) > 0 else 0
        self.publicity = publicity
        self.cardList = cardList

    def __dict__(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'universe': self.universe,
                'colors': {'blue':self.blue, 'green':self.green, 'red':self.red, 'yellow':self.yellow},
                'cardList': self.cardList}

    def __repr__(self):
        return '<Deck %r>' % self.name

    def getDetailedCardList(self):
        command = ('SELECT wsdb_eng.*, WeissDeck_WeissCard.count FROM Card '
                   'JOIN WeissDeck_WeissCard on wsdb_eng.id=WeissDeck_WeissCard.cardid '
                   'WHERE WeissDeck_WeissCard.deckid=%s;')
        cursor.execute(command, [self.id])
        retVal = {'cards': cursor.fetchall()}
        return retVal

    def save(self):
        data = [self.name, self.description, self.universe, int(self.blue),
                int(self.green), int(self.red), int(self.yellow), int(self.publicity)]
        cursor.execute('SELECT COUNT(name) AS count FROM WeissSet WHERE name=%s', [self.universe])
        unicount = cursor.fetchall()[0]
        if unicount['count'] <= 0:
            return False

        command = ('INSERT INTO WeissDeck (name, description, universe, ' +
                    'blue, green, red, yellow, publicity) ' +
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s);')
        if(self.id != None):
            data.append(int(self.id))
            command = ('UPDATE WeissDeck SET name=%s' +
                        ', description=%s' +
                        ', universe=%s' +
                        ', blue=%s' +
                        ', green=%s' +
                        ', red=%s' +
                        ', yellow=%s' +
                        ', publicity=%s' +
                        ' WHERE id=%s;')
        cursor.execute(command, data)
        connection.commit()
        self.id = self.id if self.id is not None else connection.insert_id()
        if self.cardList!=[]:
            command1 = ('DELETE FROM WeissDeck_WeissCard WHERE deckId=%s;')
            data1 = [self.id]
            command2 = ''
            data2 = []
            for card in self.cardList:
                command2 += 'INSERT INTO WeissDeck_WeissCard (deckId, cardId, count) VALUES (%s, %s, %s);'
                data2.append(self.id)
                data2.append(card['pid'])
                data2.append(card['count'])
            command2 = (command2)
            cursor.execute(command1, data1)
            cursor.execute(command2, data2)
            connection.commit()
        return True

    #Static Methods

    @staticmethod
    def all():
        cursor.execute('SELECT * FROM WeissDeck;')
        return cursor.fetchall()

    @staticmethod
    def get(id):
        cursor.execute('SELECT * FROM WeissDeck WHERE id=%s;', [int(id)])
        results = cursor.fetchall()
        if len(results) <= 0:
            return None
        result = results[0]
        cursor.execute('SELECT cardId,count FROM WeissDeck_WeissCard WHERE deckId=%s;', [int(id)])
        cardList = cursor.fetchall()
        return Deck(
            id,
            result['name'],
            result['description'],
            result['universe'],
            result['size'],
            {
                'blue':result['blue'],
                'green':result['green'],
                'red':result['red'],
                'yellow':result['yellow']
                        },
            result['publicity'],
            cardList)

    @staticmethod
    def search(term, colors):
        term = '%'+term+'%'
        colorNames = ['blue', 'green', 'red', 'yellow']
        colorstr = ''
        for color in colorNames:
            if colors[color]==1:
                colorstr += ' AND '+color+'=1'
        command = ('SELECT * FROM WeissDeck WHERE (name like %s OR description like %s) AND (publicity=1'+colorstr+');')
        data = [term, term]
        cursor.execute(command, data)
        return cursor.fetchall()

class Card:
    def __init__(self, id, name, multiverseid, manacost, cmc, colors, types, subtypes,
                 rarity, text, flavor, artist, power, toughness, layout, imagename):
        self.id = id
        self.name = name
        self.multiverseid = multiverseid
        self.manacost = manacost
        self.cmc = cmc
        self.colors = colors
        self.types = types
        self.subtypes = subtypes
        self.rarity = rarity
        self.text = text
        self.flavor = flavor
        self.artist = artist
        self.power = power
        self.toughness = toughness
        self.layout = layout
        self.imagename = imagename
        self.imageurl = "http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid="+str(multiverseid)

    def save(self):
        try:
            data = [self.id, self.name, self.multiverseid, self.manacost, int(self.cmc), json.dumps(self.colors),
                    json.dumps(self.types), json.dumps(self.subtypes), self.rarity, self.text, self.flavor,
                    self.artist, self.power, self.toughness, self.layout, self.imagename, self.imageurl]
            command = ('INSERT INTO Card (id, name, multiverseid, manacost, cmc, colors, types, ' +
                        'subtypes, rarity, text, flavor, artist, power, toughness, layout, imagename, imageurl) ' +
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);')
            cursor.execute(command, data)
            connection.commit()
        except Exception:
            return self.name
        return ''

    @staticmethod
    def load(id):
        data = [id]
        command = ('SELECT * FROM Card WHERE id=%s;')
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
        command = ('SELECT Card.*, Deck_Card.count FROM Card '
                   'JOIN Deck_Card on Card.id=Deck_Card.cardid '
                   'WHERE Deck_Card.deckid=%s;')
        cursor.execute(command, [self.id])
        cards = cursor.fetchall()
        retVal = {'cards': [], 'swamp': 0, 'island': 0, 'mountain': 0, 'forest': 0, 'plains': 0}
        for card in cards:
            if(card['id'] == 'swamp' or card['id'] == 'island' or card['id'] == 'forest' or card['id'] == 'mountain'
                    or card['id'] == 'plains'):
                retVal[card['id']] = card['count']
            else:
                retVal['cards'].append(card)
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
        results = cursor.fetchall()
        if len(results) <= 0:
            return None
        result = results[0]
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
