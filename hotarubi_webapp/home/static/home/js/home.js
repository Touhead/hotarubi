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

homeApp.factory('News', ['$resource',
    function($resource){
     return $resource('/api/news/:news_id', {id: '@news_id'});
    }]
);

homeApp.factory('NewsDetail', ['$resource',
    function($resource){
     return $resource('/api/news/:news_id');
    }]
);

homeApp.factory('NewsImages', ['$resource',
    function($resource){
     return $resource('/api/threads/:news_id/images/:image_id', {id: '@image_id'});
    }]
);

homeApp.factory('Threads', ['$resource',
    function($resource){
     return $resource('/api/threads/:thread_id', {id: '@thread_id'});
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

homeApp.factory('PostImages', ['$resource',
    function($resource){
     return $resource('/api/posts/:post_id/images/:image_id', {id: '@post_id'});
    }]
);

homeApp.factory('UserEventSubscription', ['$resource',
    function($resource){
     return $resource('/api/users/:username/event_subscription/:event_subscription_id', {id: '@event_subscription_id'});
    }]
);

homeApp.factory('EventEventSubscription', ['$resource',
    function($resource){
     return $resource('/api/events/:guild_event_id/event_subscription/:event_subscription_id', {id: '@event_subscription_id'});
    }]
);

homeApp.factory('EventSubscription', ['$resource',
    function($resource){
     return $resource('/api/event_subscription');
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
        })
        .when('/news/:news_id', {
            templateUrl: '/static/home/html/news/news_view.html',
            controller: 'newsNewsView',
        })
        .otherwise({
            redirectTo: '/'
        });
});

homeApp.directive('fileModel', ['$parse', function ($parse) {
        return {
            restrict: 'A',
            link: function(scope, element, attrs) {
                var model = $parse(attrs.fileModel);
                var modelSetter = model.assign;

                element.bind('change', function(){
                    scope.$apply(function(){
                        modelSetter(scope, element[0].files[0]);
                    });
                });
            }
        };
}]);

homeApp.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl){
        var fd = new FormData();
        fd.append('file', file);

        $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })

        .success(function(){
        })

        .error(function(){
        });
    }
}]);


homeApp.controller('indexThreadList', function EventListController($scope, Threads) {

    $scope.eventNotNull = function (thread) {
        return thread.banner != null;
    };
    
    $scope.threads = Threads.query();
});

homeApp.controller('indexEventList', function EventListController($scope, $filter, GuildEvent, GuildEventImages, UserEventSubscription, AuthUser) {

    $scope.events = GuildEvent.query();
    $scope.user_event_subscriptions = UserEventSubscription.query({username: AuthUser.username});
    $scope.newEventSubscription = new UserEventSubscription();
    $scope.newEventSubscription.user = AuthUser.id;

    $scope.hasSubscribed = function (guild_event) {
        return $filter('filter')($scope.user_event_subscriptions, {guild_event: guild_event.id}, false).length;
    };

    $scope.getEventSubscription = function (guild_event){
        $scope.user_event_subscriptions.some(function (user_event_subscription) {
                if (user_event_subscription.guild_event == guild_event.id){
                    $scope.user_event_subscription = user_event_subscription;
                    return true;
                }
        })
    };

    $scope.subscribe = function (guild_event) {
        if (AuthUser.id == "")
            return false;

        $scope.newEventSubscription.guild_event = guild_event.id;
        $scope.newEventSubscription.$save({username: AuthUser.username}).then(function (result) {
            $scope.user_event_subscriptions.push(result);
            guild_event.nb_subscriber += 1;
        }).then(function () {
            $scope.newEventSubscription = new UserEventSubscription();
            $scope.newEventSubscription.user = AuthUser.id;
        });
    };

    $scope.unsubscribe = function (guild_event) {
        if (AuthUser.id == "")
            return;

    $scope.getEventSubscription(guild_event);
        if ($scope.user_event_subscription == null)
            return;
        $scope.user_event_subscription.$delete({username: AuthUser.username, event_subscription_id: $scope.user_event_subscription.id}).then(function (user_event_subscription) {
            $scope.idx = $scope.user_event_subscriptions.indexOf(user_event_subscription);
            $scope.user_event_subscriptions.splice($scope.idx, 1);
            guild_event.nb_subscriber -= 1;
            $scope.user_event_subscription = null;
        })
    };
    /*$scope.events_images = [];
    $scope.events.$promise.then(function(){
        angular.forEach($scope.events, function(event){
            $scope.events_images.push(GuildEventImages.query({thread_id: event.id}));
            $scope.test = (GuildEventImages.query({thread_id: event.id}));
        });
    });*/
});

homeApp.controller('indexNewsList', function NewListController($scope, News) {

    $scope.news = News.query();
});

/*homeApp.controller('eventEventDetail', function EventController($scope, $routeParams, GuildEvent, ThreadPosts, Posts) {

    $scope.posts = GuildEvent.query({thread_id: $routeParams.guild_event_id});
});*/
homeApp.controller('eventEventView', function EventController($scope, $routeParams, GuildEventDetail, GuildEventImages, ThreadPosts, Posts, AuthUser, UserEventSubscription, PostImages, fileUpload) {

    $scope.posts = []

    $scope.$on('$routeChangeSuccess', function() {
        $scope.event = GuildEventDetail.get({guild_event_id: $routeParams.guild_event_id});
        $scope.event_images = GuildEventImages.query({thread_id: $routeParams.guild_event_id});
        $scope.posts = ThreadPosts.query({thread_id: $routeParams.guild_event_id});
        $scope.newPost = new Posts();
        $scope.newPost.thread = $routeParams.guild_event_id;
        $scope.newPost.post_image = [];
        $scope.post_image = [];
    });

    $scope.save = function () {
        $scope.newPost.pub_date = new Date();
        /*$scope.newPost.post_image = new PostImages();
        $scope.newPost.post_image.image = $scope.post_image;
        console.log('file is ' );
        console.dir($scope.post_image);
        var uploadUrl = "/fileUpload";
        fileUpload.uploadFileToUrl($scope.post_image, uploadUrl);**/

        $scope.newPost.$save().then(function (result) {
            $scope.posts.push(result);
        }).then(function () {
            $scope.newPost = new Posts();
            $scope.newPost.thread = $routeParams.guild_event_id;
            $scope.newPost.post_image = [];
        }).then(function () {
            $scope.errors_post = null;
        }, function (rejection) {
            $scope.errors_post = rejection.data;
            console.log(rejection.data);
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

    $scope.user_event_subscriptions = UserEventSubscription.query({username: AuthUser.username});
    $scope.newEventSubscription = new UserEventSubscription();
    $scope.newEventSubscription.user = AuthUser.id;

    $scope.hasSubscribed = function (guild_event) {
        return $filter('filter')($scope.user_event_subscriptions, {guild_event: guild_event.id}, false).length;
    };

    $scope.getEventSubscription = function (guild_event){
        $scope.user_event_subscriptions.some(function (user_event_subscription) {
                if (user_event_subscription.guild_event == guild_event.id){
                    $scope.user_event_subscription = user_event_subscription;
                    return true;
                }
        })
    };

    $scope.subscribe = function (guild_event) {
        if (AuthUser.id == "")
            return false;

        $scope.newEventSubscription.guild_event = guild_event.id;
        $scope.newEventSubscription.$save({username: AuthUser.username}).then(function (result) {
            $scope.user_event_subscriptions.push(result);
            guild_event.nb_subscriber += 1;
        }).then(function () {
            $scope.newEventSubscription = new UserEventSubscription();
            $scope.newEventSubscription.user = AuthUser.id;
        });
    };

    $scope.unsubscribe = function (guild_event) {
        if (AuthUser.id == "")
            return;

    $scope.getEventSubscription(guild_event);
        if ($scope.user_event_subscription == null)
            return;
        $scope.user_event_subscription.$delete({username: AuthUser.username, event_subscription_id: $scope.user_event_subscription.id}).then(function (user_event_subscription) {
            $scope.idx = $scope.user_event_subscriptions.indexOf(user_event_subscription);
            $scope.user_event_subscriptions.splice($scope.idx, 1);
            guild_event.nb_subscriber -= 1;
            $scope.user_event_subscription = null;
        })
    };
});

homeApp.controller('newsNewsView', function EventController($scope, $routeParams, NewsDetail, NewsImages, ThreadPosts, Posts, AuthUser, PostImages, fileUpload) {

    $scope.posts = [];

    $scope.$on('$routeChangeSuccess', function() {
        $scope.news = NewsDetail.get({news_id: $routeParams.news_id});
        $scope.news_images = NewsImages.query({news_id: $routeParams.news_id});
        $scope.posts = ThreadPosts.query({thread_id: $routeParams.news_id});
        $scope.newNews = new Posts();
        $scope.newNews.thread = $routeParams.news_id;
        $scope.newNews.post_image = [];
        $scope.post_image = [];
    });

    $scope.save = function () {
        $scope.newNews.pub_date = new Date();
        /*$scope.newPost.post_image = new PostImages();
        $scope.newPost.post_image.image = $scope.post_image;
        console.log('file is ' );
        console.dir($scope.post_image);
        var uploadUrl = "/fileUpload";
        fileUpload.uploadFileToUrl($scope.post_image, uploadUrl);**/

        $scope.newNews.$save().then(function (result) {
            $scope.posts.push(result);
        }).then(function () {
            $scope.newNews = new Posts();
            $scope.newNews.thread = $routeParams.news_id;
            $scope.newNews.post_image = [];
        }).then(function () {
            $scope.errors_post = null;
        }, function (rejection) {
            $scope.errors_post = rejection.data;
            console.log(rejection.data);
        });
    };

    $scope.canDelete = function (post) {
        return post.user.username == AuthUser.username
    };

    $scope.delete = function (post) {
        post.$delete({thread_id: $routeParams.news_id, post_id: post.id}).then(function (post) {
            $scope.idx = $scope.posts.indexOf(post)
            $scope.posts.splice($scope.idx, 1)
        })
    };
});