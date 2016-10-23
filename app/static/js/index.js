(function(){
  'use strict';
  var app = angular.module("MainApp", ['ngRoute', 'ui.bootstrap', 'ngAnimate']);
  app.config(function($routeProvider){
    $routeProvider.when('/', {
      templateUrl: '../static/templates/main.html'
    }).when('/collectionmanager', {
      templateUrl: '../static/templates/collectionmanager.html'
    });
  });
  app.controller("HeaderController", function($scope){
    $scope.title = "DeckBuilderPro";
    $scope.isAuthenticated = false;
  });
  app.directive("datheaderdoh", function(){
    return {
      restrict: "E",
      templateUrl: "../static/templates/site_header.html",
      require: "^HeaderController"
    };
  });
  app.filter("chunk", function() {
    return function(input){
      var newArr = [];
      var size = 12;
      for (var i=0; i<input.length; i+=size) {
        newArr.push(input.slice(i, i+size));
      }
      return newArr;
    };
  });
  app.controller('CollectionController', function($scope, chunkFilter){
    $scope.cards = [
      {
        name: 'Vulshok Sorceror',
        description: 'Vulshok sorcerors train by leaping into electrified storm clouds. Dead or alive they come back down with smiles on their faces.',
        image: 'https://abugames.com/images/products/signedmagiccards/s1712.jpg'
      },
      {
        name: 'Arrghus',
        description: 'Arrghus enters the battlefield with 8 +1/+1 counters on it.',
        image: 'http://cdn.mos.cms.futurecdn.net/5e6e56d4c3e8ade5f8fb4c5714cfd708-650-80.jpg'
      },
      {
        name: 'Blue-eyes White Dragon',
        description: 'This legendary dragon is a powerful engine of destruction, and is virtually invincible. Very few have seen this dragon and lived to tell the tale.',
        image: 'https://s-media-cache-ak0.pinimg.com/564x/f4/e3/97/f4e397ef5e0a4cd7cdbf30e65aa149c0.jpg'
      },
      {
        name: 'Arrghus',
        description: 'Arrghus enters the battlefield with 8 +1/+1 counters on it.',
        image: 'http://cdn.mos.cms.futurecdn.net/5e6e56d4c3e8ade5f8fb4c5714cfd708-650-80.jpg'
      },
      {
        name: 'Blue-eyes White Dragon',
        description: 'This legendary dragon is a powerful engine of destruction, and is virtually invincible. Very few have seen this dragon and lived to tell the tale.',
        image: 'https://s-media-cache-ak0.pinimg.com/564x/f4/e3/97/f4e397ef5e0a4cd7cdbf30e65aa149c0.jpg'
      },
      {
        name: 'Arrghus',
        description: 'Arrghus enters the battlefield with 8 +1/+1 counters on it.',
        image: 'http://cdn.mos.cms.futurecdn.net/5e6e56d4c3e8ade5f8fb4c5714cfd708-650-80.jpg'
      },
      {
        name: 'Blue-eyes White Dragon',
        description: 'This legendary dragon is a powerful engine of destruction, and is virtually invincible. Very few have seen this dragon and lived to tell the tale.',
        image: 'https://s-media-cache-ak0.pinimg.com/564x/f4/e3/97/f4e397ef5e0a4cd7cdbf30e65aa149c0.jpg'
      },
      {
        name: 'Arrghus',
        description: 'Arrghus enters the battlefield with 8 +1/+1 counters on it.',
        image: 'http://cdn.mos.cms.futurecdn.net/5e6e56d4c3e8ade5f8fb4c5714cfd708-650-80.jpg'
      },
      {
        name: 'Blue-eyes White Dragon',
        description: 'This legendary dragon is a powerful engine of destruction, and is virtually invincible. Very few have seen this dragon and lived to tell the tale.',
        image: 'https://s-media-cache-ak0.pinimg.com/564x/f4/e3/97/f4e397ef5e0a4cd7cdbf30e65aa149c0.jpg'
      },
      {
        name: 'Arrghus',
        description: 'Arrghus enters the battlefield with 8 +1/+1 counters on it.',
        image: 'http://cdn.mos.cms.futurecdn.net/5e6e56d4c3e8ade5f8fb4c5714cfd708-650-80.jpg'
      },
      {
        name: 'Blue-eyes White Dragon',
        description: 'This legendary dragon is a powerful engine of destruction, and is virtually invincible. Very few have seen this dragon and lived to tell the tale.',
        image: 'https://s-media-cache-ak0.pinimg.com/564x/f4/e3/97/f4e397ef5e0a4cd7cdbf30e65aa149c0.jpg'
      }
    ];
  })
}());
