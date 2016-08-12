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
        self.black = colors['black']
        self.blue = colors['blue']
        self.green = colors['green']
        self.red = colors['red']
        self.white = colors['white']
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

    def save(self):
        data = [self.name, self.description, self.size, int(self.black), int(self.blue),
                int(self.green), int(self.red), int(self.white),
                int(self.publicity)]
        command = ('INSERT INTO Deck (name, description, size, '
                    'black, blue, green, red, white, publicity) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);')
        if(self.id != None):
            data.append(int(self.id))
            command = ('UPDATE Deck SET name=%s'
                        ', description=%s'
                        ', size=%s'
                        ', black=%s'
                        ', blue=%s'
                        ', green=%s'
                        ', red=%s'
                        ', white=%s'
                        ', publicity=%s'
                        ' WHERE id=%s;')
        cursor.execute(command, data)
        connection.commit()
        self.id = connection.insert_id()
        if self.cardList!=[]:
            command1 = ('DELETE FROM Deck_Card WHERE DeckId=%s;')
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
        cursor.execute('SELECT * FROM Deck WHERE id=' + id + ';')
        result = cursor.fetchall()[0]
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
            result['publicity'])

    @staticmethod
    def search(term, colors):
        command = ('SELECT * FROM Deck WHERE (name like "%%s%" OR description like "%%s%") AND (black=%s AND blue=%s AND green=%s AND red=%s AND white=%s AND publicity=1);')
        data = [term, term, int(colors['black']), int(colors['blue']), int(colors['green']), int(colors['red']), int(colors['white'])]
        cursor.execute(command, data)
        return cursor.fetchall()