import requests
import pandas as pd


def _error_query_500(interval='1d'):
    """
    Error logs where response type was 500
    :type interval: string d/h/m/s/ms Ref: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-datehistogram-aggregation.html
    :return string: ES query which would fetch error logs per interval.
    """
    fixed_interval_error_query_500 = """{
                "query": {
                    "bool": {
                        "must": [{
                            "match": {
                                "http.response.status_code": "500"
                            }
                        },{
                            "match": {
                                "agent.hostname": "ninad-ubuntu-server-5"
                            }
                        }
                        ],
                        "must_not": {
                            "wildcard": {
                                "url.original" : "*/kibana*"
                            }
                        }
                    }
                },
                "aggs": {
                "group_by_time": {
                  "date_histogram": {
                    "field": "@timestamp",
                    "fixed_interval": "%s"
                  }     
                }
            }
        }"""
    ikit_fixed_interval_error_query_500 = """
    {
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "http.response.status_code": "500"
                    }
                },
                {
                    "match": {
                        "agent.hostname": "RDCkf"
                    }
                }
            ],
            "must_not": [
                {
                    "bool": {
                        "should": [
                            {
                                "wildcard": {
                                    "url.original": "*.php*"
                                }
                            },
                            {
                                "wildcard": {
                                    "url.original": "*/ocs*"
                                }
                            }, 
                            {
                                "wildcard": {
                                    "url.original": "/kibana*"
                                }
                            },
                            {
                                "wildcard": {
                                    "url.original": "/socket.io-client*"
                                }
                            },
                            {
                                "match": {
                                    "http.request.method": "HEAD"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    },
    "aggs": {
        "group_by_time": {
            "date_histogram": {
                "field": "@timestamp",
                "fixed_interval": "%s"
            }
        }
    }
}
    """
    ikit_fixed_interval_error_query_500_v2 = """
    {
    "size": 0,
    "query": {
        "bool": {
            "minimum_should_match": 1,
            "boost": 1,
            "should": [
                {
                    "term": {
                        "http.response.status_code": "400"
                    }
                },
                {
                    "term": {
                        "http.response.status_code": "500"
                    }
                },
                {
                    "term": {
                        "http.response.status_code": "401"
                    }
                },{
                    "term": {
                        "http.response.status_code": "404"
                    }
                }
            ],
            "must": [
                {
                    "range": {
                        "@timestamp" : {
                            "gte" : "now-200d/d",
                            "lt": "now/d"
                        }
                    }
                },
                {
                    "match": {
                        "host.hostname": "kf6-stage"
                    }
                }
            ],
            "must_not": [
                {
                    "match": {
                        "url.original": "*.php*"
                    }
                },
                {
                    "wildcard": {
                        "url.original": "/ocs*"
                    }
                },
                {
                    "wildcard": {
                        "url.original": "/kibana/*"
                    }
                },
                {
                    "wildcard": {
                        "url.original": "/es/*"
                    }
                },
                {
                    "match": {
                        "http.request.method": "HEAD"
                    }
                },
                {
                    "match": {
                        "user_agent.os.name" : "Windows Vista"
                    }
                }
            ]
        }
    },
    "aggs": {
        "group_by_time": {
            "date_histogram": {
                "field": "@timestamp",
                "fixed_interval": "%s"
            }
        }
    }
}

    """
    return ikit_fixed_interval_error_query_500_v2 % interval


def _access_query(interval='1d'):
    """
    Generate ES Search query for fetching access logs per interval
    :param freq:
    :return string: ES query which would fetch access logs per interval.
    """
    fixed_interval_access_log = """{
                "query": {
                    "bool": {
                        "must": [{
                            "match": {
                                "http.response.status_code": "200"
                            }
                        }
                        ],
    
                        "must_not":[
                        {
                        "bool":{
                             "should": [
    
                            {"wildcard": {
                                "url.original" : "*.php*"
                            }
                        },
                        {
                            "wildcard": {
                                "url.original" : "*/ocs*"
                            }
                        },
                        {
                            "wildcard": {
                                "url.original" : "/kibana*"
                            }
                        },
                        {
                            "match": {
                                "http.request.method" : "HEAD"
                            }
                        }
                        ]
                        }
                        }
    
                    ]
                }
                },
                "aggs": {
                "group_by_time": {
                  "date_histogram": {
                    "field": "@timestamp",
                    "fixed_interval": "%s"
                  }
    
                }
              }
            }"""
    ikit_fixed_interval_access_log = """
    {
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "http.response.status_code": "200"
                    }
                },
                {
                    "match": {
                        "agent.hostname": "RDCkf"
                    }
                }
            ],
            "must_not": [
                {
                    "bool": {
                        "should": [
                            {
                                "wildcard": {
                                    "url.original": "*.php*"
                                }
                            },
                            {
                                "wildcard": {
                                    "url.original": "*/ocs*"
                                }
                            }, 
                            {
                                "wildcard": {
                                    "url.original": "/kibana*"
                                }
                            },
                            {
                                "wildcard": {
                                    "url.original": "/socket.io-client*"
                                }
                            },
                            {
                                "match": {
                                    "http.request.method": "HEAD"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    },
    "aggs": {
        "group_by_time": {
            "date_histogram": {
                "field": "@timestamp",
                "fixed_interval": "%s"
            }
        }
    }
}
    """
    ikit_fixed_interval_access_log_v2 = """
    {
    "size": 0,
    "query": {
        "bool": {
            "minimum_should_match": 1,
            "boost": 1,
            "should": [
                {
                    "term": {
                        "http.response.status_code": "206"
                    }
                },
                {
                    "term": {
                        "http.response.status_code": "200"
                    }
                },
                {
                    "term": {
                        "http.response.status_code": "201"
                    }
                },
                {
                    "term": {
                        "http.response.status_code": "304"
                    }
                }
            ],
            "must": [
                {
                    "range": {
                        "@timestamp" : {
                            "gte" : "now-200d/d",
                            "lt": "now/d"
                        }
                    }
                },
                {
                    "match": {
                        "host.hostname": "kf6-stage"
                    }
                }
            ],
            "must_not": [
                {
                    "match": {
                        "url.original": "*.php*"
                    }
                },
                {
                    "wildcard": {
                        "url.original": "/ocs*"
                    }
                },
                {
                    "wildcard": {
                        "url.original": "/kibana/*"
                    }
                },
                {
                    "wildcard": {
                        "url.original": "/es/*"
                    }
                },
                {
                    "match": {
                        "http.request.method": "HEAD"
                    }
                },
                {
                    "match": {
                        "user_agent.os.name" : "Windows Vista"
                    }
                }
            ]
        }
    },
    "aggs": {
        "group_by_time": {
            "date_histogram": {
                "field": "@timestamp",
                "fixed_interval": "%s"
            }
        }
    }
}
"""

    return ikit_fixed_interval_access_log_v2 % interval


class elasticSearch:

    def __init__(self, url="http://localhost:9200/_search"):
        self.URL = url

    def _fetch_data_from_es(self, query):
        r = requests.get(url=self.URL, headers={'Content-type': 'application/json'}, data=query)
        data = r.json()
        return data['aggregations']['group_by_time']['buckets']

    def get_nginx_reliability(self, interval='1d'):
        """
        Get reliability data from nginx log.
        :param interval: string [int] d/h/m/s/ms Ref: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-datehistogram-aggregation.html
        :return: dataframe : [buckets, access_counts,error_counts, reliability]
        """

        error_logs_histograms = self._fetch_data_from_es(_error_query_500(interval))
        access_logs_histograms = self._fetch_data_from_es(_access_query(interval))

        buckets = []
        error_counts = []
        for eachbucket in error_logs_histograms:
            buckets.append(eachbucket['key_as_string'])  # Left column as interval bucket index ( day /hour)
            error_counts.append(eachbucket['doc_count'])  # Right Column as the respective count.
        error_dataframe = pd.DataFrame({'buckets': buckets, 'error_counts': error_counts})
        error_dataframe["error_counts"] = error_dataframe["error_counts"].astype(int)
        buckets = []
        access_count = []
        for eachbucket in access_logs_histograms:
            buckets.append(eachbucket['key_as_string'])
            access_count.append(eachbucket['doc_count'])
        access_dataframe = pd.DataFrame({'buckets': buckets, 'access_counts': access_count})
        access_dataframe["access_counts"] = access_dataframe["access_counts"].astype(int)
        df = pd.merge(access_dataframe, error_dataframe, on='buckets', how="left")
        df = df.fillna(0) # To fill in error counts as 0 since some days ersorr count would not exist
        df['reliability'] = 1 - (df['error_counts'] / (df['access_counts'] + df['error_counts']))
        df = df.fillna(1)  # Since 0/0 is a Nan, we need to convert that to 1 (
        #df = df.dropna() # Just removing those rows where 0 req exist... if requird!

        return df
