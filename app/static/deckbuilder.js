var app = angular.module('app', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}]);

app.factory('Deck', function() {
    return {
      id: loadedDeck.id,
      name: loadedDeck.name,
      cards: loadedDeck.cardList.cards,
      count: loadedCount,
      colors: {
        black: loadedDeck.black,
        blue: loadedDeck.blue,
        green: loadedDeck.green,
        red: loadedDeck.red,
        white: loadedDeck.white
      },
      swamp: loadedDeck.cardList.swamp,
      island: loadedDeck.cardList.island,
      forest: loadedDeck.cardList.forest,
      mountain: loadedDeck.cardList.mountain,
      plains: loadedDeck.cardList.plains
    }
});

app.filter('cardType', function() {
    return function(input, targetType){
        output = [];
        for(var i in input) {
            if (input[i]['types'] != null) {
                if(input[i].types.toLowerCase().indexOf(targetType.toLowerCase())>-1 &&
                (targetType=='creature' || input[i].types.toLowerCase().indexOf('creature')<=-1)) {
                    output.push(input[i]);
                }
            }
            else {
                if(input[i].type.toLowerCase().indexOf(targetType.toLowerCase())>-1 &&
                (targetType=='creature' || input[i].type.toLowerCase().indexOf('creature')<=-1)) {
                    output.push(input[i]);
                }
            }
        }
        return output;
    };
});

app.controller('CardController', function($http, $scope, Deck) {
    this.list = [];
    this.set = 'M15';
    var menu = this;
    $http.get("http://mtgjson.com/json/AllSets.json").success(function(data) {
      menu.list = data;
    });
    this.query = "";
    this.add = function(card) {
        var index = Deck.cards.indexOf(card);
        if(index > -1) {
            Deck.cards[index]['count'] += 1;
        } else {
            card['count'] = 1;
            card['types'] = card['type']
            Deck.cards.push(card);
        }
        Deck.count+=1;
        for(color in card.colors) {
            if(Deck.colors[card.colors[color].toLowerCase()]!=null) {
                Deck.colors[card.colors[color].toLowerCase()] += 1;
            }
        }
    }
});

app.controller('DeckController', function($scope, $http, $timeout, Deck) {
    this.deck = Deck;
    $scope.lands = ['swamp', 'island', 'forest', 'mountain', 'plains'];
    this.remove = function(card) {
        var index = Deck.cards.indexOf(card);
        if(index > -1) {
            Deck.cards[index].count-=1
            Deck.count-=1;
            for(color in card.colors) {
                if(Deck.colors[card.colors[color].toLowerCase()]!=null) {
                    Deck.colors[card.colors[color].toLowerCase()] -= 1;
                }
            }
            if(Deck.cards[index].count<=0) {
                Deck.cards.splice(index, 1);
            }
        }
    };
    this.modLand = function(sign, type) {
        if(sign=='+') {
            Deck[type] += 1
        } else if(Deck[type]>0) {
            Deck[type] -= 1
        }
    };
    $scope.edit = false;
    $scope.showEditor = function() {
        $scope.edit = true;
        var textbox = document.getElementById("deck-name-input");
        var tmp = Deck.name;
        $timeout(function() {
          textbox.focus();
          textbox.select();
          Deck.name = tmp;
        });
    };
    $scope.blurUpdate = function() {
        $scope.edit = false;
    };
    $scope.save = function() {
        var cards = [];
        var lands = $scope.lands;
        for(land in $scope.lands) {
            var landCount = Deck[lands[land]];
            if(landCount>0) {
                cards.push({id: lands[land], cardId: lands[land], count: landCount, name: lands[land]});
            }
        }
        cards = cards.concat(Deck.cards);
        if(Deck.id==null) {
            $http.post('./create', {
                name: Deck.name,
                description: 'Totes a Description',
                size: Deck.count + Deck.swamp + Deck.island + Deck.forest + Deck.mountain + Deck.plains,
                cards: cards,
                colors: Deck.colors,
                publicity: 1
            }).success(function(data, status){
                if(status==200 && data.status==200) {
                    Deck.id = data.id;
                }
                console.log(data);
            });
        } else {
            $http.put('./update', {
                id: Deck.id,
                name: Deck.name,
                description: 'Totes a Description',
                size: Deck.count + Deck.swamp + Deck.island + Deck.forest + Deck.mountain + Deck.plains,
                cards: cards,
                colors: Deck.colors,
                publicity: 1
            }).success(function(data, status){
                console.log(data);
            });
        }
    }
});
