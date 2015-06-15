angular.module('OpenSlidesApp.config', [])

.config(function($stateProvider) {
    $stateProvider
        .state('config', {
            url: '/config',
            abstract: true,
            template: "<ui-view/>",
        })
        .state('config.list', {
            controller: 'ConfigListCtrl',
            resolve: {
                configs: function(Config) {
                    return Config.findAll();
                }
            }
        });
})

.controller('ConfigListCtrl', function($scope, Config) {
    Config.bindAll({}, $scope, 'configs');

    $scope.save = function (key) {
        Config.save(key);
    }
    $scope.saveall = function () {
        // TODO: save all config values
    };
    $scope.reseteall = function () {
        // TODO: reset all config values
    };
})

