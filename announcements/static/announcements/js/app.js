var myApp = angular.module('myApp', [])
.directive('tagManager', function($filter) {
    return {
        restrict: 'E',
        scope: {
          tags: '=',
          allTags: '=',
          autocomplete: '=autocomplete'
        },
        template:
            '<div class="tags">' +
      			'<div ng-repeat="(idx, tag) in tags" class="tag badge" ng-class="{\'badge-primary\' : allTags.indexOf(tag) !== -1, \'badge-secondary\' : allTags.indexOf(tag) === -1}">{{tag}}' +
            // '<div ng-repeat="(idx, tag) in tags" class="tag badge" ng-class="setColor(tag)">{{tag}}' +
            '<button type="button" class="close" ng-click="remove(idx)" aria-label="Close"> <span aria-hidden="true">&times;</span></button></div>' +
            '</div>' +
            '<div class="input-group mb-3"><input type="text" class="form-control" placeholder="add a tag..." ng-model="newValue" /> ' +
            '<span class="input-group-append"><button class="btn btn-outline-secondary" ng-click="add()" type="button">Add</button></span></div>',

        link: function ( $scope, $element ) {

      		var input = angular.element($element).find('input');

      		// setup autocomplete
      		if ($scope.autocomplete) {
              $scope.autocompleteFocus = function(event, ui) {
                input.val(ui.item.value);
                return false;
              };
              $scope.autocompleteSelect = function(event, ui) {
                $scope.newValue = ui.item.value;
                $scope.$apply( $scope.add );

                return false;
              };
              $($element).find('input').autocomplete({
                    minLength: 0,
                    source: function(request, response) {
                      var item;
                      return response((function() {
                        var _i, _len, _ref, _results;
                        _ref = $scope.autocomplete;
                        _results = [];
                        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                          item = _ref[_i];
                          if (item.toLowerCase().indexOf(request.term.toLowerCase()) !== -1) {
                            _results.push(item);
                          }
                        }
                        return _results;
                      })());
                    },
                    focus: (function(_this) {
                      return function(event, ui) {
                        return $scope.autocompleteFocus(event, ui);
                      };
                    })(this),
                    select: (function(_this) {
                      return function(event, ui) {
                        return $scope.autocompleteSelect(event, ui);
                      };
                    })(this)
                  });
            }

            $scope.lowerCased = function () {
              return $filter('lowercase')($scope.newValue);
            }

            $scope.getStrLength = function() {
                return $scope.newValue.length;
            }

             // adds the new tag to the array
            $scope.add = function() {
      				// if not dupe, add it
              // $scope.newValue.toLowerCase();
              $scope.newValue = $scope.lowerCased();
              $scope.valLength = $scope.getStrLength();

              if($scope.valLength > 0){
                if ($scope.tags.indexOf($scope.newValue)==-1){
                      	$scope.tags.push($scope.newValue);

                }
              }
              $scope.newValue = "";
            };

            // remove an item
            $scope.remove = function ( idx ) {
                $scope.tags.splice( idx, 1 );
            };

            // $scope.setColor = function (idx, tag) {
            //   if ($scope.allTags.indexOf(tag) ==-1){
            //     return "badge-danger";
            //   }
            //   else{
            //     return "badge-primary";
            //   }
            // }

            // capture keypresses
            input.bind( 'keypress', function ( event ) {
                // enter was pressed
                if ( event.keyCode == 13 ) {
                    $scope.$apply( $scope.add );
                }
            });
        }
    };
})

.controller('tagsCtrl', ['$scope', function ( $scope ) {
    $scope.tags = [ 'bootstrap', 'list', 'angular' ];
    $scope.allTags = [ 'bootstrap', 'list', 'angular', 'directive', 'edit', 'label', 'modal', 'close', 'button', 'grid', 'javascript', 'html', 'badge', 'dropdown'];
       // $scope.allTags = {{ all_tags }};
}]);




// $(document).ready(function() {});
