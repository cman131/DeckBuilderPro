var app = angular.module('app', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}]);

app.factory('Deck', function() {
    var cardList = loadedDeck.cardList == null ? [] : loadedDeck.cardList;
    var universe = allSets[0];
    if (loadedDeck.universe != null && loadedDeck.universe != "") {
        for (i in allSets) {
            if (allSets[i].name == loadedDeck.universe) {
                universe = allSets[i];
                break;
            }
        }
    }
    return {
      id: loadedDeck.id == '' ? null : loadedDeck.id,
      name: loadedDeck.name,
      cards: cardList,
      count: loadedCount,
      colors: loadedDeck.colors,
      universe: universe
    };
});

app.filter('distinct', function() {
    return function(input, propName){
        var dic = {};
        for(var i in input) {
            dic[input[i][propName]] = input[i];
        }
        var output = [];
        for(var i in dic) {
            output.push(dic[i]);
        }
        return output;
    }
});

app.filter('cardType', function() {
    return function(input, targetType){
        var output = [];
        for(var i in input) {
            if (input[i]['type'] == targetType) {
                output.push(input[i]);
            }
        }
        return output;
    };
});

app.filter('cardSet', function() {
    return function(input, targetSet){
        var output = [];
        for(var i in input) {
            var setId = input[i]['number'].substring(0, 3).replace('/', '');
            var matches = allSets.filter(function(obj) {
                return obj.id == setId && obj.name == targetSet.name;
            });
            if (matches.length > 0) {
                output.push(input[i]);
            }
        }
        return output;
    };
});

app.controller('CardController', function($http, $scope, Deck) {
    this.list = [];
    menu = this;
    $http.get("../wcard/all").success(function(data) {
      menu.list = data.data;
    });
    this.sets = allSets;
    this.query = "";
    this.deck = Deck;
    this.add = function(card) {
        var index = Deck.cards.indexOf(card);
        if(index > -1) {
            Deck.cards[index]['count'] += 1;
        } else {
            card['count'] = 1;
            Deck.cards.push(card);
        }
        Deck.count+=1;
        Deck.colors[card.color.toLowerCase()] += 1;
    }
});

app.controller('DeckController', function($scope, $http, $timeout, Deck) {
    this.deck = Deck;
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
    $scope.edit = loadedDeck['id'] != '' && loadedDeck['id'] != null;
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
        console.log(Deck.id);
        if(Deck.id==null) {
            $http.post('./create', {
                name: Deck.name,
                description: 'Totes a Description',
                universe: Deck.universe.name,
                size: Deck.count,
                cards: Deck.cards,
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
                universe: Deck.universe.name,
                size: Deck.count,
                cards: Deck.cards,
                colors: Deck.colors,
                publicity: 1
            }).success(function(data, status){
                console.log(data);
            });
        }
    }
});
