from app import app, models, config
from flask import render_template, redirect, request, jsonify, json
import math, requests, json

@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Conor', 'id': 1}
    return render_template('index.html', title='Home', user=user)

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
        return jsonify({'status': 500})
    deck = models.Deck.get(request.args.get('id'))
    if(deck == None):
        return jsonify({'status': 500})
    cards = []#deck.getDetailedCardList()
    user = {'name': 'Conor', 'id': 1}
    return render_template('deck.html', title=deck.name, user=user, config=config, decky=deck.__dict__(), cards=cards)

@app.route('/deck/create', methods=['POST'])
def create():
    if('name' not in request.json or 'description' not in request.json or
        'size' not in request.json or 'colors' not in request.json or 'cards' not in request.json or
            'publicity' not in request.json):
        return jsonify({'status': 500, 'missing': request.json['size']})

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
    return jsonify({'status': 200 if status else 500, 'id': temp.id})

@app.route('/deck/update', methods=['PUT'])
def update():
    if('id' not in request.json or 'name' not in request.json or 'description' not in request.json or
        'size' not in request.json or 'colors' not in request.json or 'cards' not in request.json or
            'publicity' not in request.json):
        return jsonify({'status': 500, 'missing': request.json})
    deck = models.Deck.get(int(request.json['id']))
    if deck is None:
        return jsonify({'status': 500})

    # Make a temporary object with the given data and save it to the db
    temp = models.Deck(deck.id,
                    request.json['name'],
                    request.json['description'],
                    request.json['size'],
                    request.json['colors'],
                    request.json['publicity'],
                    request.json['cards'])
    status = temp.save()
    return jsonify({'status': 200 if status else 500, 'id': temp.id})

@app.route('/deck/builder')
def builder():
    deck = models.Deck(None, 'Untitled', 'This is a description.', 0,
                       {'black':0, 'blue':0, 'green':0, 'red':0, 'white':0}, [], 1)
    if(request.args.get('id') is not None):
        deck = models.Deck.get(request.args.get('id'))
    if(deck is None):
        return jsonify({'status': 500})
    user = {'name': 'Conor', 'id': 1}
    return render_template('deckbuilder.html', title='DeckBuilder', user=user, config=config, decky=deck.__dict__())

@app.route('/card/update', methods=['GET'])
def updateCard():
    failures = []
    models.Card.clear('DOIT')
    print('Cleared')
    r = requests.get("http://mtgjson.com/json/AllCards.json")
    print('Got\'em')
    cards = r.json()
    print('Loaded')
    for key in cards.keys():
        card = cards[key]
        if 'colors' not in card:
            card['colors'] = []
        if 'manaCost' not in card:
            card['manaCost'] = ''
            card['cmc'] = 0
        if 'power' not in card:
            card['power'] = ''
            card['toughness'] = ''
        if 'multiverseid' not in card:
            if 'Swamp' == key or 'Island' == key or 'Forest' == key or 'Mountain' == key or 'Plains' == key:
                continue
            card['multiverseid'] = ''
        if 'rarity' not in card:
            card['rarity'] = 'None'
        if 'artist' not in card:
            card['artist'] = ''
        if 'subtypes' not in card:
            card['subtypes'] = []
        if 'number' not in card:
            card['number'] = ''
        if 'text' not in card:
            card['text'] = ''
        if 'types' not in card:
            card['types'] = []
        newCard = models.Card(key, card['name'], card['multiverseid'], card['manaCost'], card['cmc'], card['colors'],
                       card['types'], [], card['subtypes'], card['rarity'], card['text'], '',
                       card['artist'], card['number'], card['power'], card['toughness'], card['layout'], '')
        result = newCard.save()
        if result!='':
            failures.append(newCard.name)
        else:
            print(newCard.name + ' Inserted.')
    print(len(cards), 'Updates Completed')
    return jsonify({'status':200, 'failures': failures})
