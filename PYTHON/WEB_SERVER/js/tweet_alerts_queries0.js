/**
* Return all distinct created_at dates existing in tweet_alerts_index
*/
query_all_dates = {
    "size": 0,
    "aggs" : {
        "_source" : {
            "date_histogram" : {
                "field" : "created_at",
                "interval" : "day"
            }
        }
    }
}

/**
* Retrieve all alerts identified for a given date
*/
query_alerts_for_date = {
    "fields": ["_source"],
    "query": {
        "range": {
            "created_at": {
            "gte": "20160219000000",
            "lte": "20160220000000",
            "format": "yyyyMMddHHmmss"
            }
        }
    }
}

/**
* Tweet alerts angular js controller
*/
app.controller('TweetAlertsCtrl', function($scope, $filter, $http) {

    /*
    * Define all relevant ElasticSearch servers
    */
    $scope.esServers = ["http://lame14.enst.fr:50014", "http://lame14.enst.fr:50012"];
    $scope.esSelectedServer = $scope.esServers[0];

    $scope.selectDistinctDates = function() {
        $http({
            url: $scope.esSelectedServer+'/tweet_alerts_/_search',
            method: "POST",
            data: query_all_dates,
        }).success(function (data, status, headers, config) {
            // keep only buckets
            $scope.allDates = data['aggregations']['_source']['buckets']
        });
        /*
        // keep only key and convert it to date
        dates = dates.map(function(x) {
            dt = new Date(x['key']);
            return new Date(dt.getFullYear(), dt.getMonth(), dt.getDate())
        });
        // remove duplicates
        dates = dates.filter(function(value, index, self) {
            return self.indexOf(value) === index;
        });
        */
    }

    $scope.selectDistinctDates()
});
