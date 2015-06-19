angular.module('OpenSlidesApp.config.site', [])

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
                configOption: function($http) {
                    return $http({ 'method': 'OPTIONS', 'url': '/rest/config/config/' });
                }
            }
        });
})

.controller('ConfigListCtrl', function($scope, Config, configOption) {
    Config.bindAll({}, $scope, 'configs');
    $scope.configGroups = configOption.data.config_groups;

    // save changed config value
    $scope.save = function(key, value) {
        Config.get(key).value = value;
        Config.save(key);
    }
    // reset selected config value
    $scope.reset = function(config) {
        if (config.default_value) {
            config.value = config.default_value;
        }
        Config.save(config);
    }
})

