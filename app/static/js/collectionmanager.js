(function(){
  'use strict';
  angular.Module('MainApp').Directive("card-popover", function(){
    return {
      restrict: "A",
      scope: {
        popoverCard: "=cardPopover"
      },
      link: function() {
        element.popover({
          trigger: 'hover',
          templateUrl: './static/card_popover.html'
        });
      }
    };
  });
});
