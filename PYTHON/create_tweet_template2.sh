#! /bin/sh

curl -XPUT http://lame14.enst.fr:50012/_template/tweet_tpl -d '
{
	"template" : "tweets_stif-*",
	"mappings" : {
	"tweet2" : {
		"_timestamp" : { "enabled" : true },
                "properties": {
                    "coordinates": {
                        "properties": {
                            "coordinates": {
                                "type": "double"
                            },
                            "type": {
                                "type": "string"
                            }
                        }
                    },
                    "created_at": {
                        "type": "date", "format": "EEE MMM dd HH:mm:ss Z yyyy"
                    },
                    "entities": {
                        "properties": {
                            "hashtags": {
                                "properties": {
                                    "indices": {
                                        "type": "long"
                                    },
                                    "text": {
                                        "type": "string"
                                    }
                                }
                            },
                            "media": {
                                "properties": {
                                    "display_url": {
                                        "type": "string"
                                    },
                                    "expanded_url": {
                                        "type": "string"
                                    },
                                    "id": {
                                        "type": "long"
                                    },
                                    "id_str": {
                                        "type": "string"
                                    },
                                    "indices": {
                                        "type": "long"
                                    },
                                    "media_url": {
                                        "type": "string"
                                    },
                                    "media_url_https": {
                                        "type": "string"
                                    },
                                    "sizes": {
                                        "properties": {
                                            "large": {
                                                "properties": {
                                                    "h": {
                                                        "type": "long"
                                                    },
                                                    "resize": {
                                                        "type": "string"
                                                    },
                                                    "w": {
                                                        "type": "long"
                                                    }
                                                }
                                            },
                                            "medium": {
                                                "properties": {
                                                    "h": {
                                                        "type": "long"
                                                    },
                                                    "resize": {
                                                        "type": "string"
                                                    },
                                                    "w": {
                                                        "type": "long"
                                                    }
                                                }
                                            },
                                            "small": {
                                                "properties": {
                                                    "h": {
                                                        "type": "long"
                                                    },
                                                    "resize": {
                                                        "type": "string"
                                                    },
                                                    "w": {
                                                        "type": "long"
                                                    }
                                                }
                                            },
                                            "thumb": {
                                                "properties": {
                                                    "h": {
                                                        "type": "long"
                                                    },
                                                    "resize": {
                                                        "type": "string"
                                                    },
                                                    "w": {
                                                        "type": "long"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "source_status_id": {
                                        "type": "long"
                                    },
                                    "source_status_id_str": {
                                        "type": "string"
                                    },
                                    "source_user_id": {
                                        "type": "long"
                                    },
                                    "source_user_id_str": {
                                        "type": "string"
                                    },
                                    "type": {
                                        "type": "string"
                                    },
                                    "url": {
                                        "type": "string"
                                    }
                                }
                            },
                            "symbols": {
                                "properties": {
                                    "indices": {
                                        "type": "long"
                                    },
                                    "text": {
                                        "type": "string"
                                    }
                                }
                            },
                            "urls": {
                                "properties": {
                                    "display_url": {
                                        "type": "string"
                                    },
                                    "expanded_url": {
                                        "type": "string"
                                    },
                                    "indices": {
                                        "type": "long"
                                    },
                                    "url": {
                                        "type": "string"
                                    }
                                }
                            },
                            "user_mentions": {
                                "properties": {
                                    "id": {
                                        "type": "long"
                                    },
                                    "id_str": {
                                        "type": "string"
                                    },
                                    "indices": {
                                        "type": "long"
                                    },
                                    "name": {
                                        "type": "string"
                                    },
                                    "screen_name": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    },
                    "extended_entities": {
                        "properties": {
                            "media": {
                                "properties": {
                                    "display_url": {
                                        "type": "string"
                                    },
                                    "expanded_url": {
                                        "type": "string"
                                    },
                                    "id": {
                                        "type": "long"
                                    },
                                    "id_str": {
                                        "type": "string"
                                    },
                                    "indices": {
                                        "type": "long"
                                    },
                                    "media_url": {
                                        "type": "string"
                                    },
                                    "media_url_https": {
                                        "type": "string"
                                    },
                                    "sizes": {
                                        "properties": {
                                            "large": {
                                                "properties": {
                                                    "h": {
                                                        "type": "long"
                                                    },
                                                    "resize": {
                                                        "type": "string"
                                                    },
                                                    "w": {
                                                        "type": "long"
                                                    }
                                                }
                                            },
                                            "medium": {
                                                "properties": {
                                                    "h": {
                                                        "type": "long"
                                                    },
                                                    "resize": {
                                                        "type": "string"
                                                    },
                                                    "w": {
                                                        "type": "long"
                                                    }
                                                }
                                            },
                                            "small": {
                                                "properties": {
                                                    "h": {
                                                        "type": "long"
                                                    },
                                                    "resize": {
                                                        "type": "string"
                                                    },
                                                    "w": {
                                                        "type": "long"
                                                    }
                                                }
                                            },
                                            "thumb": {
                                                "properties": {
                                                    "h": {
                                                        "type": "long"
                                                    },
                                                    "resize": {
                                                        "type": "string"
                                                    },
                                                    "w": {
                                                        "type": "long"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "source_status_id": {
                                        "type": "long"
                                    },
                                    "source_status_id_str": {
                                        "type": "string"
                                    },
                                    "source_user_id": {
                                        "type": "long"
                                    },
                                    "source_user_id_str": {
                                        "type": "string"
                                    },
                                    "type": {
                                        "type": "string"
                                    },
                                    "url": {
                                        "type": "string"
                                    },
                                    "video_info": {
                                        "properties": {
                                            "aspect_ratio": {
                                                "type": "long"
                                            },
                                            "duration_millis": {
                                                "type": "long"
                                            },
                                            "variants": {
                                                "properties": {
                                                    "bitrate": {
                                                        "type": "long"
                                                    },
                                                    "content_type": {
                                                        "type": "string"
                                                    },
                                                    "url": {
                                                        "type": "string"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "favorite_count": {
                        "type": "long"
                    },
                    "favorited": {
                        "type": "boolean"
                    },
                    "filter_level": {
                        "type": "string"
                    },
                    "geo": {
                        "properties": {
                            "coordinates": {
                                "type": "double"
                            },
                            "type": {
                                "type": "string"
                            }
                        }
                    },
                    "id": {
                        "type": "long"
                    },
                    "id_str": {
                        "type": "string"
                    },
                    "in_reply_to_screen_name": {
                        "type": "string"
                    },
                    "in_reply_to_status_id": {
                        "type": "long"
                    },
                    "in_reply_to_status_id_str": {
                        "type": "string"
                    },
                    "in_reply_to_user_id": {
                        "type": "long"
                    },
                    "in_reply_to_user_id_str": {
                        "type": "string"
                    },
                    "is_quote_status": {
                        "type": "boolean"
                    },
                    "lang": {
                        "type": "string"
                    },
                    "limit": {
                        "properties": {
                            "timestamp_ms": {
                                "type": "string"
                            },
                            "track": {
                                "type": "long"
                            }
                        }
                    },
                    "place": {
                        "properties": {
                            "attributes": {
                                "type": "object"
                            },
                            "bounding_box": {
                                "properties": {
                                    "coordinates": {
                                        "type": "double"
                                    },
                                    "type": {
                                        "type": "string"
                                    }
                                }
                            },
                            "country": {
                                "type": "string"
                            },
                            "country_code": {
                                "type": "string"
                            },
                            "full_name": {
                                "type": "string"
                            },
                            "id": {
                                "type": "string"
                            },
                            "name": {
                                "type": "string"
                            },
                            "place_type": {
                                "type": "string"
                            },
                            "url": {
                                "type": "string"
                            }
                        }
                    },
                    "possibly_sensitive": {
                        "type": "boolean"
                    },
                    "quoted_status": {
                        "properties": {
                            "coordinates": {
                                "properties": {
                                    "coordinates": {
                                        "type": "double"
                                    },
                                    "type": {
                                        "type": "string"
                                    }
                                }
                            },
                            "created_at": {
                                "type": "string"
                            },
                            "entities": {
                                "properties": {
                                    "hashtags": {
                                        "properties": {
                                            "indices": {
                                                "type": "long"
                                            },
                                            "text": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "media": {
                                        "properties": {
                                            "display_url": {
                                                "type": "string"
                                            },
                                            "expanded_url": {
                                                "type": "string"
                                            },
                                            "id": {
                                                "type": "long"
                                            },
                                            "id_str": {
                                                "type": "string"
                                            },
                                            "indices": {
                                                "type": "long"
                                            },
                                            "media_url": {
                                                "type": "string"
                                            },
                                            "media_url_https": {
                                                "type": "string"
                                            },
                                            "sizes": {
                                                "properties": {
                                                    "large": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    },
                                                    "medium": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    },
                                                    "small": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    },
                                                    "thumb": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            "source_status_id": {
                                                "type": "long"
                                            },
                                            "source_status_id_str": {
                                                "type": "string"
                                            },
                                            "source_user_id": {
                                                "type": "long"
                                            },
                                            "source_user_id_str": {
                                                "type": "string"
                                            },
                                            "type": {
                                                "type": "string"
                                            },
                                            "url": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "symbols": {
                                        "properties": {
                                            "indices": {
                                                "type": "long"
                                            },
                                            "text": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "urls": {
                                        "properties": {
                                            "display_url": {
                                                "type": "string"
                                            },
                                            "expanded_url": {
                                                "type": "string"
                                            },
                                            "indices": {
                                                "type": "long"
                                            },
                                            "url": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "user_mentions": {
                                        "properties": {
                                            "id": {
                                                "type": "long"
                                            },
                                            "id_str": {
                                                "type": "string"
                                            },
                                            "indices": {
                                                "type": "long"
                                            },
                                            "name": {
                                                "type": "string"
                                            },
                                            "screen_name": {
                                                "type": "string"
                                            }
                                        }
                                    }
                                }
                            },
                            "extended_entities": {
                                "properties": {
                                    "media": {
                                        "properties": {
                                            "display_url": {
                                                "type": "string"
                                            },
                                            "expanded_url": {
                                                "type": "string"
                                            },
                                            "id": {
                                                "type": "long"
                                            },
                                            "id_str": {
                                                "type": "string"
                                            },
                                            "indices": {
                                                "type": "long"
                                            },
                                            "media_url": {
                                                "type": "string"
                                            },
                                            "media_url_https": {
                                                "type": "string"
                                            },
                                            "sizes": {
                                                "properties": {
                                                    "large": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    },
                                                    "medium": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    },
                                                    "small": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    },
                                                    "thumb": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            "source_status_id": {
                                                "type": "long"
                                            },
                                            "source_status_id_str": {
                                                "type": "string"
                                            },
                                            "source_user_id": {
                                                "type": "long"
                                            },
                                            "source_user_id_str": {
                                                "type": "string"
                                            },
                                            "type": {
                                                "type": "string"
                                            },
                                            "url": {
                                                "type": "string"
                                            },
                                            "video_info": {
                                                "properties": {
                                                    "aspect_ratio": {
                                                        "type": "long"
                                                    },
                                                    "duration_millis": {
                                                        "type": "long"
                                                    },
                                                    "variants": {
                                                        "properties": {
                                                            "bitrate": {
                                                                "type": "long"
                                                            },
                                                            "content_type": {
                                                                "type": "string"
                                                            },
                                                            "url": {
                                                                "type": "string"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "favorite_count": {
                                "type": "long"
                            },
                            "favorited": {
                                "type": "boolean"
                            },
                            "filter_level": {
                                "type": "string"
                            },
                            "geo": {
                                "properties": {
                                    "coordinates": {
                                        "type": "double"
                                    },
                                    "type": {
                                        "type": "string"
                                    }
                                }
                            },
                            "id": {
                                "type": "long"
                            },
                            "id_str": {
                                "type": "string"
                            },
                            "in_reply_to_screen_name": {
                                "type": "string"
                            },
                            "in_reply_to_status_id": {
                                "type": "long"
                            },
                            "in_reply_to_status_id_str": {
                                "type": "string"
                            },
                            "in_reply_to_user_id": {
                                "type": "long"
                            },
                            "in_reply_to_user_id_str": {
                                "type": "string"
                            },
                            "is_quote_status": {
                                "type": "boolean"
                            },
                            "lang": {
                                "type": "string"
                            },
                            "possibly_sensitive": {
                                "type": "boolean"
                            },
                            "quoted_status_id": {
                                "type": "long"
                            },
                            "quoted_status_id_str": {
                                "type": "string"
                            },
                            "retweet_count": {
                                "type": "long"
                            },
                            "retweeted": {
                                "type": "boolean"
                            },
                            "scopes": {
                                "properties": {
                                    "followers": {
                                        "type": "boolean"
                                    }
                                }
                            },
                            "source": {
                                "type": "string"
                            },
                            "text": {
                                "type": "string"
                            },
                            "truncated": {
                                "type": "boolean"
                            },
                            "user": {
                                "properties": {
                                    "contributors_enabled": {
                                        "type": "boolean"
                                    },
                                    "created_at": {
                                        "type": "string"
                                    },
                                    "default_profile": {
                                        "type": "boolean"
                                    },
                                    "default_profile_image": {
                                        "type": "boolean"
                                    },
                                    "description": {
                                        "type": "string"
                                    },
                                    "favourites_count": {
                                        "type": "long"
                                    },
                                    "followers_count": {
                                        "type": "long"
                                    },
                                    "friends_count": {
                                        "type": "long"
                                    },
                                    "geo_enabled": {
                                        "type": "boolean"
                                    },
                                    "id": {
                                        "type": "long"
                                    },
                                    "id_str": {
                                        "type": "string"
                                    },
                                    "is_translator": {
                                        "type": "boolean"
                                    },
                                    "lang": {
                                        "type": "string"
                                    },
                                    "listed_count": {
                                        "type": "long"
                                    },
                                    "location": {
                                        "type": "string"
                                    },
                                    "name": {
                                        "type": "string"
                                    },
                                    "profile_background_color": {
                                        "type": "string"
                                    },
                                    "profile_background_image_url": {
                                        "type": "string"
                                    },
                                    "profile_background_image_url_https": {
                                        "type": "string"
                                    },
                                    "profile_background_tile": {
                                        "type": "boolean"
                                    },
                                    "profile_banner_url": {
                                        "type": "string"
                                    },
                                    "profile_image_url": {
                                        "type": "string"
                                    },
                                    "profile_image_url_https": {
                                        "type": "string"
                                    },
                                    "profile_link_color": {
                                        "type": "string"
                                    },
                                    "profile_sidebar_border_color": {
                                        "type": "string"
                                    },
                                    "profile_sidebar_fill_color": {
                                        "type": "string"
                                    },
                                    "profile_text_color": {
                                        "type": "string"
                                    },
                                    "profile_use_background_image": {
                                        "type": "boolean"
                                    },
                                    "protected": {
                                        "type": "boolean"
                                    },
                                    "screen_name": {
                                        "type": "string"
                                    },
                                    "statuses_count": {
                                        "type": "long"
                                    },
                                    "time_zone": {
                                        "type": "string"
                                    },
                                    "url": {
                                        "type": "string"
                                    },
                                    "utc_offset": {
                                        "type": "long"
                                    },
                                    "verified": {
                                        "type": "boolean"
                                    }
                                }
                            }
                        }
                    },
                    "quoted_status_id": {
                        "type": "long"
                    },
                    "quoted_status_id_str": {
                        "type": "string"
                    },
                    "retweet_count": {
                        "type": "long"
                    },
                    "retweeted": {
                        "type": "boolean"
                    },
                    "retweeted_status": {
                        "properties": {
                            "coordinates": {
                                "properties": {
                                    "coordinates": {
                                        "type": "double"
                                    },
                                    "type": {
                                        "type": "string"
                                    }
                                }
                            },
                            "created_at": {
                                "type": "string"
                            },
                            "entities": {
                                "properties": {
                                    "hashtags": {
                                        "properties": {
                                            "indices": {
                                                "type": "long"
                                            },
                                            "text": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "media": {
                                        "properties": {
                                            "display_url": {
                                                "type": "string"
                                            },
                                            "expanded_url": {
                                                "type": "string"
                                            },
                                            "id": {
                                                "type": "long"
                                            },
                                            "id_str": {
                                                "type": "string"
                                            },
                                            "indices": {
                                                "type": "long"
                                            },
                                            "media_url": {
                                                "type": "string"
                                            },
                                            "media_url_https": {
                                                "type": "string"
                                            },
                                            "sizes": {
                                                "properties": {
                                                    "large": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    },
                                                    "medium": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    },
                                                    "small": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    },
                                                    "thumb": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            "source_status_id": {
                                                "type": "long"
                                            },
                                            "source_status_id_str": {
                                                "type": "string"
                                            },
                                            "source_user_id": {
                                                "type": "long"
                                            },
                                            "source_user_id_str": {
                                                "type": "string"
                                            },
                                            "type": {
                                                "type": "string"
                                            },
                                            "url": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "symbols": {
                                        "properties": {
                                            "indices": {
                                                "type": "long"
                                            },
                                            "text": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "urls": {
                                        "properties": {
                                            "display_url": {
                                                "type": "string"
                                            },
                                            "expanded_url": {
                                                "type": "string"
                                            },
                                            "indices": {
                                                "type": "long"
                                            },
                                            "url": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "user_mentions": {
                                        "properties": {
                                            "id": {
                                                "type": "long"
                                            },
                                            "id_str": {
                                                "type": "string"
                                            },
                                            "indices": {
                                                "type": "long"
                                            },
                                            "name": {
                                                "type": "string"
                                            },
                                            "screen_name": {
                                                "type": "string"
                                            }
                                        }
                                    }
                                }
                            },
                            "extended_entities": {
                                "properties": {
                                    "media": {
                                        "properties": {
                                            "display_url": {
                                                "type": "string"
                                            },
                                            "expanded_url": {
                                                "type": "string"
                                            },
                                            "id": {
                                                "type": "long"
                                            },
                                            "id_str": {
                                                "type": "string"
                                            },
                                            "indices": {
                                                "type": "long"
                                            },
                                            "media_url": {
                                                "type": "string"
                                            },
                                            "media_url_https": {
                                                "type": "string"
                                            },
                                            "sizes": {
                                                "properties": {
                                                    "large": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    },
                                                    "medium": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    },
                                                    "small": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    },
                                                    "thumb": {
                                                        "properties": {
                                                            "h": {
                                                                "type": "long"
                                                            },
                                                            "resize": {
                                                                "type": "string"
                                                            },
                                                            "w": {
                                                                "type": "long"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            "source_status_id": {
                                                "type": "long"
                                            },
                                            "source_status_id_str": {
                                                "type": "string"
                                            },
                                            "source_user_id": {
                                                "type": "long"
                                            },
                                            "source_user_id_str": {
                                                "type": "string"
                                            },
                                            "type": {
                                                "type": "string"
                                            },
                                            "url": {
                                                "type": "string"
                                            },
                                            "video_info": {
                                                "properties": {
                                                    "aspect_ratio": {
                                                        "type": "long"
                                                    },
                                                    "duration_millis": {
                                                        "type": "long"
                                                    },
                                                    "variants": {
                                                        "properties": {
                                                            "bitrate": {
                                                                "type": "long"
                                                            },
                                                            "content_type": {
                                                                "type": "string"
                                                            },
                                                            "url": {
                                                                "type": "string"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "favorite_count": {
                                "type": "long"
                            },
                            "favorited": {
                                "type": "boolean"
                            },
                            "filter_level": {
                                "type": "string"
                            },
                            "geo": {
                                "properties": {
                                    "coordinates": {
                                        "type": "double"
                                    },
                                    "type": {
                                        "type": "string"
                                    }
                                }
                            },
                            "id": {
                                "type": "long"
                            },
                            "id_str": {
                                "type": "string"
                            },
                            "in_reply_to_screen_name": {
                                "type": "string"
                            },
                            "in_reply_to_status_id": {
                                "type": "long"
                            },
                            "in_reply_to_status_id_str": {
                                "type": "string"
                            },
                            "in_reply_to_user_id": {
                                "type": "long"
                            },
                            "in_reply_to_user_id_str": {
                                "type": "string"
                            },
                            "is_quote_status": {
                                "type": "boolean"
                            },
                            "lang": {
                                "type": "string"
                            },
                            "place": {
                                "properties": {
                                    "attributes": {
                                        "type": "object"
                                    },
                                    "bounding_box": {
                                        "properties": {
                                            "coordinates": {
                                                "type": "double"
                                            },
                                            "type": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "country": {
                                        "type": "string"
                                    },
                                    "country_code": {
                                        "type": "string"
                                    },
                                    "full_name": {
                                        "type": "string"
                                    },
                                    "id": {
                                        "type": "string"
                                    },
                                    "name": {
                                        "type": "string"
                                    },
                                    "place_type": {
                                        "type": "string"
                                    },
                                    "url": {
                                        "type": "string"
                                    }
                                }
                            },
                            "possibly_sensitive": {
                                "type": "boolean"
                            },
                            "quoted_status": {
                                "properties": {
                                    "coordinates": {
                                        "properties": {
                                            "coordinates": {
                                                "type": "double"
                                            },
                                            "type": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "created_at": {
                                        "type": "string"
                                    },
                                    "entities": {
                                        "properties": {
                                            "hashtags": {
                                                "properties": {
                                                    "indices": {
                                                        "type": "long"
                                                    },
                                                    "text": {
                                                        "type": "string"
                                                    }
                                                }
                                            },
                                            "media": {
                                                "properties": {
                                                    "display_url": {
                                                        "type": "string"
                                                    },
                                                    "expanded_url": {
                                                        "type": "string"
                                                    },
                                                    "id": {
                                                        "type": "long"
                                                    },
                                                    "id_str": {
                                                        "type": "string"
                                                    },
                                                    "indices": {
                                                        "type": "long"
                                                    },
                                                    "media_url": {
                                                        "type": "string"
                                                    },
                                                    "media_url_https": {
                                                        "type": "string"
                                                    },
                                                    "sizes": {
                                                        "properties": {
                                                            "large": {
                                                                "properties": {
                                                                    "h": {
                                                                        "type": "long"
                                                                    },
                                                                    "resize": {
                                                                        "type": "string"
                                                                    },
                                                                    "w": {
                                                                        "type": "long"
                                                                    }
                                                                }
                                                            },
                                                            "medium": {
                                                                "properties": {
                                                                    "h": {
                                                                        "type": "long"
                                                                    },
                                                                    "resize": {
                                                                        "type": "string"
                                                                    },
                                                                    "w": {
                                                                        "type": "long"
                                                                    }
                                                                }
                                                            },
                                                            "small": {
                                                                "properties": {
                                                                    "h": {
                                                                        "type": "long"
                                                                    },
                                                                    "resize": {
                                                                        "type": "string"
                                                                    },
                                                                    "w": {
                                                                        "type": "long"
                                                                    }
                                                                }
                                                            },
                                                            "thumb": {
                                                                "properties": {
                                                                    "h": {
                                                                        "type": "long"
                                                                    },
                                                                    "resize": {
                                                                        "type": "string"
                                                                    },
                                                                    "w": {
                                                                        "type": "long"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    },
                                                    "source_status_id": {
                                                        "type": "long"
                                                    },
                                                    "source_status_id_str": {
                                                        "type": "string"
                                                    },
                                                    "source_user_id": {
                                                        "type": "long"
                                                    },
                                                    "source_user_id_str": {
                                                        "type": "string"
                                                    },
                                                    "type": {
                                                        "type": "string"
                                                    },
                                                    "url": {
                                                        "type": "string"
                                                    }
                                                }
                                            },
                                            "symbols": {
                                                "properties": {
                                                    "indices": {
                                                        "type": "long"
                                                    },
                                                    "text": {
                                                        "type": "string"
                                                    }
                                                }
                                            },
                                            "urls": {
                                                "properties": {
                                                    "display_url": {
                                                        "type": "string"
                                                    },
                                                    "expanded_url": {
                                                        "type": "string"
                                                    },
                                                    "indices": {
                                                        "type": "long"
                                                    },
                                                    "url": {
                                                        "type": "string"
                                                    }
                                                }
                                            },
                                            "user_mentions": {
                                                "properties": {
                                                    "id": {
                                                        "type": "long"
                                                    },
                                                    "id_str": {
                                                        "type": "string"
                                                    },
                                                    "indices": {
                                                        "type": "long"
                                                    },
                                                    "name": {
                                                        "type": "string"
                                                    },
                                                    "screen_name": {
                                                        "type": "string"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "extended_entities": {
                                        "properties": {
                                            "media": {
                                                "properties": {
                                                    "display_url": {
                                                        "type": "string"
                                                    },
                                                    "expanded_url": {
                                                        "type": "string"
                                                    },
                                                    "id": {
                                                        "type": "long"
                                                    },
                                                    "id_str": {
                                                        "type": "string"
                                                    },
                                                    "indices": {
                                                        "type": "long"
                                                    },
                                                    "media_url": {
                                                        "type": "string"
                                                    },
                                                    "media_url_https": {
                                                        "type": "string"
                                                    },
                                                    "sizes": {
                                                        "properties": {
                                                            "large": {
                                                                "properties": {
                                                                    "h": {
                                                                        "type": "long"
                                                                    },
                                                                    "resize": {
                                                                        "type": "string"
                                                                    },
                                                                    "w": {
                                                                        "type": "long"
                                                                    }
                                                                }
                                                            },
                                                            "medium": {
                                                                "properties": {
                                                                    "h": {
                                                                        "type": "long"
                                                                    },
                                                                    "resize": {
                                                                        "type": "string"
                                                                    },
                                                                    "w": {
                                                                        "type": "long"
                                                                    }
                                                                }
                                                            },
                                                            "small": {
                                                                "properties": {
                                                                    "h": {
                                                                        "type": "long"
                                                                    },
                                                                    "resize": {
                                                                        "type": "string"
                                                                    },
                                                                    "w": {
                                                                        "type": "long"
                                                                    }
                                                                }
                                                            },
                                                            "thumb": {
                                                                "properties": {
                                                                    "h": {
                                                                        "type": "long"
                                                                    },
                                                                    "resize": {
                                                                        "type": "string"
                                                                    },
                                                                    "w": {
                                                                        "type": "long"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    },
                                                    "source_status_id": {
                                                        "type": "long"
                                                    },
                                                    "source_status_id_str": {
                                                        "type": "string"
                                                    },
                                                    "source_user_id": {
                                                        "type": "long"
                                                    },
                                                    "source_user_id_str": {
                                                        "type": "string"
                                                    },
                                                    "type": {
                                                        "type": "string"
                                                    },
                                                    "url": {
                                                        "type": "string"
                                                    },
                                                    "video_info": {
                                                        "properties": {
                                                            "aspect_ratio": {
                                                                "type": "long"
                                                            },
                                                            "duration_millis": {
                                                                "type": "long"
                                                            },
                                                            "variants": {
                                                                "properties": {
                                                                    "bitrate": {
                                                                        "type": "long"
                                                                    },
                                                                    "content_type": {
                                                                        "type": "string"
                                                                    },
                                                                    "url": {
                                                                        "type": "string"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "favorite_count": {
                                        "type": "long"
                                    },
                                    "favorited": {
                                        "type": "boolean"
                                    },
                                    "filter_level": {
                                        "type": "string"
                                    },
                                    "geo": {
                                        "properties": {
                                            "coordinates": {
                                                "type": "double"
                                            },
                                            "type": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "id": {
                                        "type": "long"
                                    },
                                    "id_str": {
                                        "type": "string"
                                    },
                                    "in_reply_to_screen_name": {
                                        "type": "string"
                                    },
                                    "in_reply_to_status_id": {
                                        "type": "long"
                                    },
                                    "in_reply_to_status_id_str": {
                                        "type": "string"
                                    },
                                    "in_reply_to_user_id": {
                                        "type": "long"
                                    },
                                    "in_reply_to_user_id_str": {
                                        "type": "string"
                                    },
                                    "is_quote_status": {
                                        "type": "boolean"
                                    },
                                    "lang": {
                                        "type": "string"
                                    },
                                    "possibly_sensitive": {
                                        "type": "boolean"
                                    },
                                    "quoted_status_id": {
                                        "type": "long"
                                    },
                                    "quoted_status_id_str": {
                                        "type": "string"
                                    },
                                    "retweet_count": {
                                        "type": "long"
                                    },
                                    "retweeted": {
                                        "type": "boolean"
                                    },
                                    "scopes": {
                                        "properties": {
                                            "followers": {
                                                "type": "boolean"
                                            }
                                        }
                                    },
                                    "source": {
                                        "type": "string"
                                    },
                                    "text": {
                                        "type": "string"
                                    },
                                    "truncated": {
                                        "type": "boolean"
                                    },
                                    "user": {
                                        "properties": {
                                            "contributors_enabled": {
                                                "type": "boolean"
                                            },
                                            "created_at": {
                                                "type": "string"
                                            },
                                            "default_profile": {
                                                "type": "boolean"
                                            },
                                            "default_profile_image": {
                                                "type": "boolean"
                                            },
                                            "description": {
                                                "type": "string"
                                            },
                                            "favourites_count": {
                                                "type": "long"
                                            },
                                            "followers_count": {
                                                "type": "long"
                                            },
                                            "friends_count": {
                                                "type": "long"
                                            },
                                            "geo_enabled": {
                                                "type": "boolean"
                                            },
                                            "id": {
                                                "type": "long"
                                            },
                                            "id_str": {
                                                "type": "string"
                                            },
                                            "is_translator": {
                                                "type": "boolean"
                                            },
                                            "lang": {
                                                "type": "string"
                                            },
                                            "listed_count": {
                                                "type": "long"
                                            },
                                            "location": {
                                                "type": "string"
                                            },
                                            "name": {
                                                "type": "string"
                                            },
                                            "profile_background_color": {
                                                "type": "string"
                                            },
                                            "profile_background_image_url": {
                                                "type": "string"
                                            },
                                            "profile_background_image_url_https": {
                                                "type": "string"
                                            },
                                            "profile_background_tile": {
                                                "type": "boolean"
                                            },
                                            "profile_banner_url": {
                                                "type": "string"
                                            },
                                            "profile_image_url": {
                                                "type": "string"
                                            },
                                            "profile_image_url_https": {
                                                "type": "string"
                                            },
                                            "profile_link_color": {
                                                "type": "string"
                                            },
                                            "profile_sidebar_border_color": {
                                                "type": "string"
                                            },
                                            "profile_sidebar_fill_color": {
                                                "type": "string"
                                            },
                                            "profile_text_color": {
                                                "type": "string"
                                            },
                                            "profile_use_background_image": {
                                                "type": "boolean"
                                            },
                                            "protected": {
                                                "type": "boolean"
                                            },
                                            "screen_name": {
                                                "type": "string"
                                            },
                                            "statuses_count": {
                                                "type": "long"
                                            },
                                            "time_zone": {
                                                "type": "string"
                                            },
                                            "url": {
                                                "type": "string"
                                            },
                                            "utc_offset": {
                                                "type": "long"
                                            },
                                            "verified": {
                                                "type": "boolean"
                                            }
                                        }
                                    }
                                }
                            },
                            "quoted_status_id": {
                                "type": "long"
                            },
                            "quoted_status_id_str": {
                                "type": "string"
                            },
                            "retweet_count": {
                                "type": "long"
                            },
                            "retweeted": {
                                "type": "boolean"
                            },
                            "scopes": {
                                "properties": {
                                    "followers": {
                                        "type": "boolean"
                                    }
                                }
                            },
                            "source": {
                                "type": "string"
                            },
                            "text": {
                                "type": "string"
                            },
                            "truncated": {
                                "type": "boolean"
                            },
                            "user": {
                                "properties": {
                                    "contributors_enabled": {
                                        "type": "boolean"
                                    },
                                    "created_at": {
                                        "type": "string"
                                    },
                                    "default_profile": {
                                        "type": "boolean"
                                    },
                                    "default_profile_image": {
                                        "type": "boolean"
                                    },
                                    "description": {
                                        "type": "string"
                                    },
                                    "favourites_count": {
                                        "type": "long"
                                    },
                                    "followers_count": {
                                        "type": "long"
                                    },
                                    "friends_count": {
                                        "type": "long"
                                    },
                                    "geo_enabled": {
                                        "type": "boolean"
                                    },
                                    "id": {
                                        "type": "long"
                                    },
                                    "id_str": {
                                        "type": "string"
                                    },
                                    "is_translator": {
                                        "type": "boolean"
                                    },
                                    "lang": {
                                        "type": "string"
                                    },
                                    "listed_count": {
                                        "type": "long"
                                    },
                                    "location": {
                                        "type": "string"
                                    },
                                    "name": {
                                        "type": "string"
                                    },
                                    "profile_background_color": {
                                        "type": "string"
                                    },
                                    "profile_background_image_url": {
                                        "type": "string"
                                    },
                                    "profile_background_image_url_https": {
                                        "type": "string"
                                    },
                                    "profile_background_tile": {
                                        "type": "boolean"
                                    },
                                    "profile_banner_url": {
                                        "type": "string"
                                    },
                                    "profile_image_url": {
                                        "type": "string"
                                    },
                                    "profile_image_url_https": {
                                        "type": "string"
                                    },
                                    "profile_link_color": {
                                        "type": "string"
                                    },
                                    "profile_sidebar_border_color": {
                                        "type": "string"
                                    },
                                    "profile_sidebar_fill_color": {
                                        "type": "string"
                                    },
                                    "profile_text_color": {
                                        "type": "string"
                                    },
                                    "profile_use_background_image": {
                                        "type": "boolean"
                                    },
                                    "protected": {
                                        "type": "boolean"
                                    },
                                    "screen_name": {
                                        "type": "string"
                                    },
                                    "statuses_count": {
                                        "type": "long"
                                    },
                                    "time_zone": {
                                        "type": "string"
                                    },
                                    "url": {
                                        "type": "string"
                                    },
                                    "utc_offset": {
                                        "type": "long"
                                    },
                                    "verified": {
                                        "type": "boolean"
                                    }
                                }
                            }
                        }
                    },
                    "source": {
                        "type": "string"
                    },
                    "text": {
                        "type": "string"
                    },
                    "timestamp_ms": {
                        "type": "string"
                    },
                    "truncated": {
                        "type": "boolean"
                    },
                    "user": {
                        "properties": {
                            "contributors_enabled": {
                                "type": "boolean"
                            },
                            "created_at": {
                                "type": "string"
                            },
                            "default_profile": {
                                "type": "boolean"
                            },
                            "default_profile_image": {
                                "type": "boolean"
                            },
                            "description": {
                                "type": "string"
                            },
                            "favourites_count": {
                                "type": "long"
                            },
                            "followers_count": {
                                "type": "long"
                            },
                            "friends_count": {
                                "type": "long"
                            },
                            "geo_enabled": {
                                "type": "boolean"
                            },
                            "id": {
                                "type": "long"
                            },
                            "id_str": {
                                "type": "string"
                            },
                            "is_translator": {
                                "type": "boolean"
                            },
                            "lang": {
                                "type": "string"
                            },
                            "listed_count": {
                                "type": "long"
                            },
                            "location": {
                                "type": "string"
                            },
                            "name": {
                                "type": "string"
                            },
                            "profile_background_color": {
                                "type": "string"
                            },
                            "profile_background_image_url": {
                                "type": "string"
                            },
                            "profile_background_image_url_https": {
                                "type": "string"
                            },
                            "profile_background_tile": {
                                "type": "boolean"
                            },
                            "profile_banner_url": {
                                "type": "string"
                            },
                            "profile_image_url": {
                                "type": "string"
                            },
                            "profile_image_url_https": {
                                "type": "string"
                            },
                            "profile_link_color": {
                                "type": "string"
                            },
                            "profile_sidebar_border_color": {
                                "type": "string"
                            },
                            "profile_sidebar_fill_color": {
                                "type": "string"
                            },
                            "profile_text_color": {
                                "type": "string"
                            },
                            "profile_use_background_image": {
                                "type": "boolean"
                            },
                            "protected": {
                                "type": "boolean"
                            },
                            "screen_name": {
                                "type": "string"
                            },
                            "statuses_count": {
                                "type": "long"
                            },
                            "time_zone": {
                                "type": "string"
                            },
                            "url": {
                                "type": "string"
                            },
                            "utc_offset": {
                                "type": "long"
                            },
                            "verified": {
                                "type": "boolean"
                            }
                        }
                    }
                }
	}
	}
}'
