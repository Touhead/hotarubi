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
     return $resource('/api/events/:guild_event_id', {id: '@guild_event_id'});
    }]
);

homeApp.factory('GuildEventDetail', ['$resource',
    function($resource){
     return $resource('/api/events/:guild_event_id');
    }]
);

homeApp.factory('GuildEventImages', ['$resource',
    function($resource){
     return $resource('/api/threads/:thread_id/images/:image_id', {id: '@image_id'});
    }]
);

homeApp.factory('New', ['$resource',
    function($resource){
     return $resource('/api/news/:new_id', {id: '@new_id'});
    }]
);

homeApp.factory('ThreadPosts', ['$resource',
    function($resource){
     return $resource('/api/threads/:thread_id/posts/:post_id', {id: '@post_id'});
    }]
);

homeApp.factory('Posts', ['$resource',
    function($resource){
     return $resource('/api/posts/:post_id', {id: '@post_id'});
    }]
);

var homeApp = angular.module('homeApp.resource', ['ngRoute', 'homeApp']);

homeApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

homeApp.config(function($locationProvider) {
        $locationProvider.html5Mode(true);
});

homeApp.config(function($routeProvider, $locationProvider) {
        $routeProvider
        .when('/events/:guild_event_id', {
            templateUrl: '/static/home/html/events/event_view.html',
            controller: 'eventEventView',
        });
});

homeApp.controller('indexEventList', function EventListController($scope, GuildEvent, GuildEventImages) {

    $scope.events = GuildEvent.query();
    $scope.events_images = [];
    $scope.events.$promise.then(function(){
        angular.forEach($scope.events, function(event){
            $scope.events_images.push(GuildEventImages.query({thread_id: event.id}));
            $scope.test = (GuildEventImages.query({thread_id: event.id}));
        });
    });
});

homeApp.controller('indexNewList', function NewListController($scope, New) {

    $scope.news = New.query();
});

/*homeApp.controller('eventEventDetail', function EventController($scope, $routeParams, GuildEvent, ThreadPosts, Posts) {

    $scope.posts = GuildEvent.query({thread_id: $routeParams.guild_event_id});
});*/
homeApp.controller('eventEventView', function EventController($scope, $routeParams, GuildEventDetail, GuildEventImages, ThreadPosts, Posts, AuthUser) {

    $scope.posts = []

    $scope.$on('$routeChangeSuccess', function() {
        $scope.event = GuildEventDetail.get({guild_event_id: $routeParams.guild_event_id});
        $scope.event_images = GuildEventImages.query({thread_id: $routeParams.guild_event_id});
        $scope.posts = ThreadPosts.query({thread_id: $routeParams.guild_event_id});
        $scope.newPost = new Posts();
        $scope.newPost.thread = $routeParams.guild_event_id;
        $scope.newPost.post_image = [];
    });

    $scope.$on('onDataChange', function() {
        $scope.posts = ThreadPosts.query({thread_id: $routeParams.guild_event_id});
    });

    $scope.save = function () {
        $scope.newPost.$save().then(function (result) {
            $scope.posts.push(result);
        }).then(function () {
            $scope.newPost = new Posts();
            $scope.newPost.thread = $routeParams.guild_event_id;
            $scope.newPost.post_image = [];
        }).then(function () {
            $scope.errors = null
        }, function (rejection) {
            $scope.errors = rejection.data
        });
    };

    $scope.canDelete = function (post) {
        return post.user.username == AuthUser.username
    };

    $scope.delete = function (post) {
        post.$delete({thread_id: $routeParams.guild_event_id, post_id: post.id}).then(function (post) {
            $scope.idx = $scope.posts.indexOf(post)
            $scope.posts.splice($scope.idx, 1)
        })
    };
});