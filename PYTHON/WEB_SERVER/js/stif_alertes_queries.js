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

query_agg = {
"size": 0,
"aggs" : {
    "_source" : {
        "terms" : { "field" : "created_at", "size":100 }
    }
}}


query_alerts_for_date = {
    "fields": ["_source"],
    "query": {
        "range": {
            "created_at": {
            "gte": "19/02/2016",
            "lte": "20/02/2016",
            "format": "dd/MM/yyyy"
            }
        }
    },
   "sort" : {"created_at" : {"order" : "desc"}}
}

query_line_alerts_for_date = {
    "fields": ["_source"],
    "query": {
	"bool": {
	"must":[
        {"range": {
            "created_at": {
            "gte": "19/02/2016",
            "lte": "20/02/2016",
            "format": "dd/MM/yyyy"
            }
        }},
	{"match":{"transport":"ligne2"}}]
	}
    },
   "sort" : {"created_at" : {"order" : "desc"}}
}
query_msg_per_user = {
 "size":0,
  "aggs": {
    "USERID": {
      "terms": {
        "field": "user.id",
        "size": 200
      }
    }
  }
}

query_nbalerts = {
 "size":0,
  "query": {
    "filtered": {
      "filter": {
         "bool": {
          "must_not": [
            {"missing": {"field": "classe"}}
          ],
          "must": [
          {"match": {"classe": "Classe_1"}},
          {"range": {"created_at": {"gte": "16/02/2016 18:00:00","lte": "25/02/2016 21:00:00","format": "dd/MM/yyyy HH:mm:ss"}}}
          ]
        }
      }
    }
  },
 "aggs" : {
        "_source" : {
            "date_histogram" : {
                "field" : "created_at",
                "interval" : "day"
            }
        }
    }
}

query_nb_stif_alerts = {
 "size":0,
  "query": {
    "filtered": {
      "filter": {
        "range": {
            "pub_date": {
            "gte": "16/02/2016 21:00:00",
            "lte": "25/02/2016 07:00:00",
            "format": "dd/MM/yyyy HH:mm:ss"
            }
        }
      }
    }
  },
 "aggs" : {
        "_source" : {
            "date_histogram" : {
                "field" : "pub_date",
                "interval" : "day"
            }
        }
    }
}

query_alerts = {
  "query": {
    "filtered": {
      "filter": {
         "bool": {
          "must_not": [
            {"missing": {"field": "classe"}}
          ],
          "must": [
          {"match": {"classe": "Classe_1"}},
          {"range": {"created_at": {"gte": "16/02/2016 18:00:00","lte": "25/02/2016 21:00:00","format": "dd/MM/yyyy HH:mm:ss"}}}
          ]
        }
      }
    }
  },
   "sort" : {"created_at" : {"order" : "asc"}}
}

query_stif_alerts = {
  "query": {
    "filtered": {
      "filter": {
        "range": {
            "pub_date": {
            "gte": "16/02/2016 21:00:00",
            "lte": "25/02/2016 07:00:00",
            "format": "dd/MM/yyyy HH:mm:ss"
            }
        }
      }
    }
  },
   "sort" : {"pub_date" : {"order" : "asc"}}
}


/**
* Tweet alerts angular js controller
*/
app.controller('TweetAlertsCtrl', function($scope,$location,  $http) {

    $scope.init = function(index_name, pgSize) {
        //This function is sort of private constructor for controller
        $scope.index_name = index_name;
        $scope.pgSize = pgSize;
        $scope.selectDistinctDates();
        //$scope.selectNbTweetsAlerts("day", null);
	$scope.transport = $location.search()['transport']
	dt = new Date();
	dt.setHours(0);
	dt.setMinutes(0);
	dt.setSeconds(0);
	$scope.selectMsgPage(dt,15,1);
    };
      /*
    * Define all relevant ElasticSearch servers
    */
    $scope.esServers = ["http://lame14.enst.fr:50014", "http://lame14.enst.fr:50012"];
    $scope.esSelectedServer = $scope.esServers[0];
    //$scope.select_date = "None";

    /**
    * Select all distinct dates in msg index
    */
    $scope.selectDistinctDates = function() {
        $http({
            url: $scope.esSelectedServer+'/'+$scope.index_name+'/_search',
            method: "POST",
            data: query_all_dates,
        }).success(function (data, status, headers, config) {
            // keep only buckets
            dates = data['aggregations']['_source']['buckets']
            // keep only key and convert it to date
            $scope.allDates = dates.map(function(x) {
                dt = new Date(x['key']);
                return new Date(dt.getFullYear(), dt.getMonth(), dt.getDate())
            });
        });
    }

    $scope.pad = function (n) {return n < 10 ? "0"+n : n;}

    $scope.formatDate = function(dateobj) {
        return $scope.pad(dateobj.getDate())+"/"+
        $scope.pad(dateobj.getMonth()+1)+"/"+
        dateobj.getFullYear();
    }

    $scope.utcDate = function(dateobj) {
        return Date.UTC(dateobj.getFullYear(), dateobj.getMonth(), dateobj.getDate(), dateobj.getHours());
    }

    $scope.string2Date = function(str) {
        var pattern = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/;
        var arrayDate = str.match(pattern);
        return new Date(arrayDate[3], arrayDate[2] - 1, arrayDate[1]);
    }

    $scope.regularDate = function(element, index, array) {
        element['key'] = new Date(element['key']);
        element['key'] = $scope.utcDate(element['key']);
    }

    /**
    * Select a page of messages in index
    */
    $scope.selectMsgPage = function(dt, size, numPage) {
        var query = "";
        $scope.select_date = dt;
        if (numPage <= 0) {
            numPage = 1;
        }
        if ((typeof $scope.nbPages !== 'undefined') && (numPage > $scope.nbPages) && $scope.nbPages > 0) {
            numPage = $scope.nbPages;
        }
        $scope.numPage1 = numPage;
        // check select_date is valid
        if (Object.prototype.toString.call(dt) === "[object Date]") {
            // Prepare query (parameters)
            dtMin = dt;
            dtMax = new Date(dtMin);
            dtMax.setDate(dtMin.getDate()+1); // select_date + 1 day
            dtMin = $scope.formatDate(dtMin);
            dtMax = $scope.formatDate(dtMax);
	
	    if ( angular.isUndefined($scope.transport)) {
		query = angular.copy(query_alerts_for_date);
            	query['query']['range']['created_at']['gte'] = dtMin;
            	query['query']['range']['created_at']['lte'] = dtMax;
	    }
	    else {
		query = angular.copy(query_line_alerts_for_date);
            	query['query']['bool']['must'][0]['range']['created_at']['gte'] = dtMin;
            	query['query']['bool']['must'][0]['range']['created_at']['lte'] = dtMax;
            	query['query']['bool']['must'][1]['match']['transport'] = $scope.transport;
	    }
        }
        else {
	    query = angular.copy(query_alerts_for_date);
            dtMin = new Date("02/16/2016 18:00:00");
            dtMax = new Date("02/25/2016 21:00:00");
            dtMin = $scope.formatDate(dtMin);
            dtMax = $scope.formatDate(dtMax);
            query['query']['range']['created_at']['gte'] = dtMin;
            query['query']['range']['created_at']['lte'] = dtMax;
        }
        // Execute query
        sUrl = $scope.esSelectedServer+'/'+$scope.index_name+'/_search?size='+size+'&from='+((numPage-1)*size);
        $http({
            url: sUrl,
            method: "POST",
            data: query,
        }).success(function (data, status, headers, config) {
            // set nb hits
            $scope.nbHits = data['hits']['total']
            $scope.nbPages = ($scope.nbHits / size) >> 0;
            if ($scope.nbHits % size != 0) {
                $scope.nbPages++;
            }
            // keep only hits
            var msg = data['hits']['hits'];
            for (var i=0;i<msg.length;i++) {
                msg[i]['_source']['created_at'] = new Date(msg[i]['_source']['created_at'])
            }
            $scope.pgMessages = msg;
           // $scope.selectAllMsg4Action(false);
        });
    }

    /**
    * Select a page of messages in index
    */
    $scope.selectTweetAlerts = function(dt, size, numPage) {
        var query = angular.copy(query_alerts);
        $scope.sel_date = dt;
        if (numPage <= 0) {
            numPage = 1;
        }
        if ((typeof $scope.nbPages1 !== 'undefined') && (numPage > $scope.nbPages1)) {
            numPage = $scope.nbPages1;
        }
        $scope.numPage1 = numPage;
        // check select_date is valid
        if (Object.prototype.toString.call(dt) === "[object Date]") {
            // Prepare query (parameters)
            dtMin = dt;
            dtMax = new Date(dtMin);
            dtMax.setDate(dtMin.getDate()+1); // select_date + 1 day
            dtMin = $scope.formatDate(dtMin);
            dtMax = $scope.formatDate(dtMax);
            query['query']['filtered']['filter']['bool']['must'][1]['range']['created_at']['gte'] = dtMin;
            query['query']['filtered']['filter']['bool']['must'][1]['range']['created_at']['lte'] = dtMax;
            query['query']['filtered']['filter']['bool']['must'][1]['range']['created_at']['format'] = "dd/MM/yyyy";
        }
        else {
            query['query']['filtered']['filter']['bool']['must'][1]['range']['created_at']['gte'] = "16/02/2016 18:00:00";
            query['query']['filtered']['filter']['bool']['must'][1]['range']['created_at']['lte'] = "25/02/2016 21:00:00";
        }
        // Execute query
        sUrl = $scope.esSelectedServer+'/'+$scope.index_name+'/_search?size='+size+'&from='+((numPage-1)*size);
        $http({
            url: sUrl,
            method: "POST",
            data: query,
        }).success(function (data, status, headers, config) {
            // set nb hits
            $scope.nbHits1 = data['hits']['total']
            $scope.nbPages1 = ($scope.nbHits1 / size) >> 0;
            if ($scope.nbHits1 % size != 0) {
                $scope.nbPages1++;
            }
            // keep only hits
            var msg = data['hits']['hits'];
            for (var i=0;i<msg.length;i++) {
                msg[i]['_source']['created_at'] = new Date(msg[i]['_source']['created_at'])
            }
            $scope.tweetsAlertsMessages = msg;
        });
    }

    $scope.selectStifAlerts = function(dt, size, numPage) {
        var query = angular.copy(query_stif_alerts);
        $scope.stif_sel_date = dt;
        if (numPage <= 0) {
            numPage = 1;
        }
        if ((typeof $scope.nbPages2 !== 'undefined') && (numPage > $scope.nbPages2)) {
            numPage = $scope.nbPages2;
        }
        $scope.numPage2 = numPage;
        // check select_date is valid
        if (Object.prototype.toString.call(dt) === "[object Date]") {
            // Prepare query (parameters)
            dtMin = dt;
            dtMax = new Date(dtMin);
            dtMax.setDate(dtMin.getDate()+1); // select_date + 1 day
            dtMin = $scope.formatDate(dtMin);
            dtMax = $scope.formatDate(dtMax);
            query['query']['filtered']['filter']['range']['pub_date']['gte'] = dtMin;
            query['query']['filtered']['filter']['range']['pub_date']['lte'] = dtMax;
            query['query']['filtered']['filter']['range']['pub_date']['format'] = "dd/MM/yyyy";
        }
        else {
            query['query']['filtered']['filter']['range']['pub_date']['gte'] = "16/02/2016 21:00:00";
            query['query']['filtered']['filter']['range']['pub_date']['lte'] = "25/02/2016 07:00:00";
        }
        // Execute query
        sUrl = $scope.esSelectedServer+'/stif_info_trafic/_search?size='+size+'&from='+((numPage-1)*size);
        $http({
            url: sUrl,
            method: "POST",
            data: query,
        }).success(function (data, status, headers, config) {
            // set nb hits
            $scope.nbHits2 = data['hits']['total']
            $scope.nbPages2 = ($scope.nbHits2 / size) >> 0;
            if ($scope.nbHits2 % size != 0) {
                $scope.nbPages2++;
            }
            // keep only hits
            var msg = data['hits']['hits'];
            for (var i=0;i<msg.length;i++) {
                msg[i]['_source']['pub_date'] = new Date(msg[i]['_source']['pub_date'])
            }
            $scope.stifAlertsMessages = msg;
        });
    }



});
