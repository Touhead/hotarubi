/**
 * Created by touhe on 6/5/2016.
 */

var homeApp = angular.module('homeApp', ['ngResource']);

homeApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

homeApp.factory('GuildEvent', ['$resource',
    function($resource){
     return $resource('/api/events/:id', {id: '@id'});
    }]
);

homeApp.factory('New', ['$resource',
    function($resource){
     return $resource('/api/news/:id', {id: '@id'});
    }]
);

var homeApp = angular.module('homeApp.resource', ['homeApp']);

homeApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

homeApp.controller('homeAppEventList', function EventListController($scope, GuildEvent) {

    $scope.events = GuildEvent.query();

    //$scope.images = GuildEventImage.query();
});

homeApp.controller('homeAppNewList', function NewListController($scope, New) {

    $scope.news = New.query();

});