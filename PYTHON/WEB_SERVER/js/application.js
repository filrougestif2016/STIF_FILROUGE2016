//var app = angular.module("app", ["xeditable", "ngMockE2E"]);
var app = angular.module("app", ["xeditable", "highcharts-ng"]);

app.run(function(editableOptions) {
  editableOptions.theme = 'bs3';
});

app.directive('htmldiv', function($compile, $parse) {
return {
  restrict: 'E',
  link: function(scope, element, attr) {
    scope.$watch(attr.content, function() {
      element.html($parse(attr.content)(scope));
      $compile(element.contents())(scope);
    }, true);
  }
}
});

app.directive('barChart', function(){
            var chart = d3.custom.barChart();
            return {
                restrict: 'E',
                replace: true,
                template: '<div class="chart"></div>',
                scope:{
                    width: '=width',
                    height: '=height',
                    top: '=top',
                    bottom: '=bottom',
                    data: '=data',
                    hovered: '&hovered'
                },
                link: function(scope, element, attrs) {
                    var chartEl = d3.select(element[0]);
                    chart.on('customHover', function(d, i){
                        scope.hovered({args:d});
                    });

                    scope.$watch('data', function (newVal, oldVal) {
                        chartEl.datum(newVal).call(chart);
                    });

                    scope.$watch('width', function(d, i){
                        chartEl.call(chart.width(scope.width));
                    });

                    scope.$watch('height', function(d, i){
                        chartEl.call(chart.height(scope.height));
                    });

                    scope.$watch('top', function(d, i){
                        chartEl.call(chart.top(scope.top));
                    });

                    scope.$watch('bottom', function(d, i){
                        chartEl.call(chart.bottom(scope.bottom));
                    });
                }
            }
        });

app.directive('chartForm', function(){
            return {
                restrict: 'E',
                replace: true,
                controller: function AppCtrl ($scope) {
                    $scope.update = function(d, i){ $scope.data = randomData(); };
                    function randomData(){
                        return d3.range(~~(Math.random()*50)+1).map(function(d, i){return ~~(Math.random()*1000);});
                    }
                },
                template: '<div class="form">' +
                        'Height: {{options.height}}<br />' +
                        '<input type="range" ng-model="options.height" min="100" max="800"/>' +
                        '<br /><button ng-click="update()">Update Data</button>' +
                        '<br />Hovered bar data: {{barValue}}</div>'
            }
        });
