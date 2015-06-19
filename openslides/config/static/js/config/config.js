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
    var html_input_types = {
        string: 'text',
        integer: 'number'
    };

    // convert input_type in html-type
    $scope.get_html_input_type = function (type) {
        return html_input_type.type
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

