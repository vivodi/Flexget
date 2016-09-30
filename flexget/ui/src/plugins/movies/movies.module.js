/* global angular, registerPlugin */
(function () {
    'use strict';

    angular
        .module('plugins.movies', [
            'ngMaterial',
            'ngSanitize',

            'blocks.exception',
            'blocks.router'
        ]);

    registerPlugin('plugins.movies');
}());