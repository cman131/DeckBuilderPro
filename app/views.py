from app import app, models, config, tabletop_generator
from flask import render_template, redirect, request, jsonify, json, Response
import math, requests, json

@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Conor', 'id': 1}
    return render_template('index.html', title='Home', user=user)

@app.route('/testroute')
def testIndex():
    user = {'name': 'Conor', 'id': 1}
    return render_template('testindex.html', title='Home', user=user)

@app.route('/results')
def results():
    term = request.args.get('term')
    colors = json.loads(request.args.get('colors'))
    user = {'name': 'Conor', 'id': 1}

    results = models.Deck.search(term, colors)
    return render_template('results.html', title='Results', user=user, results=results, searchTerm=term, searchColors=colors)

@app.route('/deck')
def deck():
    if(request.args.get('id') == None):
        return jsonify({'status': 400, 'message': 'Bad id. Go home, you\'re clearly drunk.'})
    try:
        int(request.args.get('id'))
    except Exception:
        print(request.args.get('id'))
        return jsonify({'status': 400, 'message': 'Bad id. Go home, you\'re clearly drunk.'})
    deck = models.Deck.get(request.args.get('id'))
    if(deck == None):
        return jsonify({'status': 404})
    cards = deck.getDetailedCardList()
    user = {'name': 'Conor', 'id': 1}
    return render_template('deck.html', title=deck.name, user=user, config=config, decky=deck.__dict__(), cards=cards)

@app.route('/deck/tabletop')
def deckTabletop():
    if(request.args.get('id') == None):
        return jsonify({'status': 400, 'message': 'Bad id. Go home, you\'re clearly drunk.'})
    try:
        int(request.args.get('id'))
    except Exception:
        return jsonify({'status': 400, 'message': 'Bad id. Go home, you\'re clearly drunk.'})
    deck = models.Deck.get(request.args.get('id'))
    if(deck == None):
        return jsonify({'status': 404})
    cardDetails = deck.getDetailedCardList()
    cards = cardDetails["cards"]
    cards.append(getLandCard('swamp', cardDetails['swamp']))
    cards.append(getLandCard('island', cardDetails['island']))
    cards.append(getLandCard('mountain', cardDetails['mountain']))
    cards.append(getLandCard('plains', cardDetails['plains']))
    cards.append(getLandCard('forest', cardDetails['forest']))
    outputJson = tabletop_generator.TableTopGenerator.generateTableTopJson(deck.name, deck.description, cards)
    return Response(outputJson,
             mimetype='application/json',
             headers={'Content-Disposition': 'attachment;filename='+deck.name.replace(' ', '_')+'.json'})

@app.route('/deck/create', methods=['POST'])
def create():
    if('name' not in request.json or 'description' not in request.json or
        'size' not in request.json or 'colors' not in request.json or 'cards' not in request.json or
            'publicity' not in request.json):
        return jsonify({'status': 400, 'missing': request.json['size']})

    # Make a temporary object with the given data and save it to the db
    colors = request.json['colors']
    cards = request.json['cards']
    temp = models.Deck(None, request.json['name'],
                    request.json['description'],
                    request.json['size'],
                    colors,
                    request.json['publicity'],
                    cards)
    status = temp.save()
    return jsonify({'status': 200 if status else 400, 'id': temp.id})

@app.route('/deck/update', methods=['PUT'])
def update():
    if('id' not in request.json or 'name' not in request.json or 'description' not in request.json or
        'size' not in request.json or 'colors' not in request.json or 'cards' not in request.json or
            'publicity' not in request.json):
        return jsonify({'status': 400, 'missing': request.json})
    try:
        int(request.json['id'])
    except Exception:
        return jsonify({'status': 400, 'message': 'Bad id. Go home, you\'re clearly drunk.'})
    deck = models.Deck.get(int(request.json['id']))
    if deck is None:
        return jsonify({'status': 404})

    # Make a temporary object with the given data and save it to the db
    cards = request.json['cards']
    temp = models.Deck(deck.id,
                    request.json['name'],
                    request.json['description'],
                    request.json['size'],
                    request.json['colors'],
                    request.json['publicity'],
                    cards)
    status = temp.save()
    return jsonify({'status': 200 if status else 500, 'id': temp.id})

@app.route('/deck/builder')
def builder():
    count = 0
    deck = models.Deck('', 'Untitled', 'This is a description.', 0,
                       {'black':0, 'blue':0, 'green':0, 'red':0, 'white':0}, True, [])
    deck.cardList = {'cards': [], 'swamp': 0, 'island': 0, 'mountain': 0, 'forest': 0, 'plains': 0}
    if(request.args.get('id') is not None):
        try:
            int(request.args.get('id'))
        except Exception:
            return jsonify({'status': 400, 'message': 'Bad id. Go home, you\'re clearly drunk.'})
        deck = models.Deck.get(request.args.get('id'))
        if deck == None:
            return jsonify({'status': 404})
        deck.cardList = deck.getDetailedCardList()
        count = sum([x["count"] for x in deck.cardList['cards']]) +\
                deck.cardList['swamp'] + deck.cardList['island'] + deck.cardList['mountain'] +\
                deck.cardList['plains'] + deck.cardList['forest']
    user = {'name': 'Conor', 'id': 1}
    return render_template('deckbuilder.html', title='DeckBuilder', user=user, config=config, decky=deck.__dict__(), count=count)

# Weiss Schwarz

@app.route('/wdeck/create', methods=['POST'])
def wcreate():
    if('name' not in request.json or 'description' not in request.json or
        'size' not in request.json or 'colors' not in request.json or 'cards' not in request.json or
            'publicity' not in request.json or 'universe' not in request.json):
        return jsonify({'status': 400, 'missing': request.json['size']})

    # Make a temporary object with the given data and save it to the db
    temp = models.WeissDeck(None, request.json['name'],
                    request.json['description'],
                    request.json['universe'],
                    request.json['colors'],
                    request.json['publicity'],
                    request.json['cards'])
    status = temp.save()
    return jsonify({'status': 200 if status else 400, 'id': temp.id})

@app.route('/wdeck/builder')
def wbuilder():
    count = 0
    deck = models.WeissDeck('', 'Untitled', 'This is a description.', '',
                       {'blue':0, 'green':0, 'red':0, 'yellow':0}, True, [])
    if(request.args.get('id') is not None):
        try:
            int(request.args.get('id'))
        except Exception:
            return jsonify({'status': 400, 'message': 'Bad id. Go home, you\'re clearly drunk.'})
        deck = models.wDeck.get(request.args.get('id'))
        if deck == None:
            return jsonify({'status': 404})
        deck.cardList = deck.getDetailedCardList()
        count = sum([x["count"] for x in deck.cardList['cards']])
    allSets = [set.__dict__ for set in models.WeissSet.loadAll()]
    user = {'name': 'Conor', 'id': 1}
    return render_template('wdeckbuilder.html', title='DeckBuilder', user=user, config=config, decky=deck.__dict__(), count=count, allSets=allSets)

@app.route('/wcard/all')
def allWCards():
    print('Retrieving Cards.')
    cards = models.WeissCard.loadAll(True)
    print('Got all the cards!')
    return jsonify({'status': 200, 'data': cards})

#DB Updaters - leave disabled
@app.route('/weiss/image/pull', methods=['GET'])
def getWeissImages():
    if True:
        return jsonify({'status': 404})
    cards = models.WeissCard.getAllImageless()
    tabletop_generator.TableTopGenerator.getWeissImages(cards)
    return jsonify({'status': 200})

@app.route('/card/update', methods=['GET'])
def updateCard():
    if True:
        return jsonify({'status': 404})
    failures = []
    models.Card.clear('DOIT')
    print('Cleared')
    response = requests.get("http://mtgjson.com/json/AllSets.json")
    print('Got\'em')
    sets = response.json()
    print('Loaded')
    cardCount = 0
    sets['LandParty'] = {'name': 'LandParty',
                         'cards': [
                             getLandCard('swamp', 0,),
                             getLandCard('island', 0),
                             getLandCard('forest', 0),
                             getLandCard('mountain', 0),
                             getLandCard('plains', 0)]}
    for set in sets:
        print(' - Loading Set: ' + sets[set]['name'])
        for card in sets[set]['cards']:
            if 'colors' not in card:
                card['colors'] = []
            if 'manaCost' not in card:
                card['manaCost'] = ''
                card['cmc'] = 0
            if 'power' not in card:
                card['power'] = ''
                card['toughness'] = ''
            if 'multiverseid' not in card:
                if 'Swamp' == card['name'] or 'Island' == card['name'] or 'Forest' == card['name'] or 'Mountain' == card['name'] or 'Plains' == card['name']:
                    continue
                card['multiverseid'] = ''
            if 'rarity' not in card:
                card['rarity'] = 'None'
            if 'artist' not in card:
                card['artist'] = ''
            if 'subtypes' not in card:
                card['subtypes'] = []
            if 'text' not in card:
                card['text'] = ''
            if 'flavor' not in card:
                card['flavor'] = ''
            if 'types' not in card:
                card['types'] = []
            if 'layout' not in card:
                card['layout'] = ''
            if 'imagename' not in card:
                card['imagename'] = ''
            newCard = models.Card(card['id'], card['name'], card['multiverseid'], card['manaCost'], card['cmc'], card['colors'],
                           card['types'], card['subtypes'], card['rarity'], card['text'], card['flavor'],
                           card['artist'], card['power'], card['toughness'], card['layout'], card['imagename'])
            result = newCard.save()
            if result!='':
                failures.append(newCard.name)
            else:
                print(newCard.name + ' Inserted.')
                cardCount += 1
    print(cardCount, 'Updates Completed')
    return jsonify({'status':200, 'failures': failures})

# Private
def getLandCard(name, count):
    lands = {'swamp': {'name': 'swamp', 'id': 'swamp', 'multiverseid': '402061'},
             'island': {'name': 'island', 'id': 'island', 'multiverseid': '401927'},
             'mountain': {'name': 'mountain', 'id': 'mountain', 'multiverseid': '401962'},
             'plains': {'name': 'plains', 'id': 'plains', 'multiverseid': '401994'},
             'forest': {'name': 'forest', 'id': 'forest', 'multiverseid': '401889'}}
    land = lands[name]
    land['count'] = count
    land['imageurl'] = "http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid="+str(land['multiverseid'])
    return land
