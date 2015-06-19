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
                configs: function($http) {
                    return $http({ 'method': 'OPTIONS', 'url': '/rest/config/config/' });
                }
            }
        });
})

.controller('ConfigListCtrl', function($scope, Config, configs) {
    Config.bindAll({}, $scope, 'configs');
    $scope.config_groups = configs.data.config_groups;

    $scope.get_html_input_type = function (type) {
        var html_input_types = {
            string: 'text',
            integer: 'number',
            boolean: 'checkbox'
        };
        return html_input_types[type];
    }


    // save changed config value
    $scope.save = function (config) {
        Config.save(config);
    }
    // reset selected config value
    $scope.reset = function (config) {
        if (config.default_value) {
            config.value = config.default_value;
        }
        Config.save(config);
    }
})

