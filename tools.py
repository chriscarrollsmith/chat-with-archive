tools = [
    {
        "name": "get_tweet_urls",
        "url": "https://fabxmporizzqflnftavs.supabase.co/rest/v1/tweet_urls",
        "method": "GET",
        "headers": {
            "apikey": "{{COMMUNITY_ARCHIVE_API_KEY}}",
            "Authorization": "Bearer {{COMMUNITY_ARCHIVE_API_KEY}}"
        },
        "description": "Retrieves URLs associated with tweets from the 'tweet_urls' PostgREST endpoint of the Twitter Community Archive API. It allows filtering by tweet ID and provides the flexibility to access the primary and expanded URLs. Must use PostgREST operators (e.g., eq, neq, gt, gte, lt, lte, like, ilike) for filtering.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Filter URLs by a specific ID. Use with 'eq' operator. Example: id=eq.123. Note: This is a Primary Key.<pk/>"
                },
                "url": {
                    "type": "string",
                    "description": "Filter by the short URL associated with the tweet. Use with 'eq' or 'like' operators. Example: url=like.*twitter*"
                },
                "expanded_url": {
                    "type": "string",
                    "description": "Filter by the fully expanded URL associated with the tweet. Use with 'eq' or 'like' operators. Example: expanded_url=like.*example.com*"
                },
                "display_url": {
                    "type": "string",
                    "description": "Filter by the display URL associated with the tweet. Use with 'eq' or 'like' operators. Example: display_url=eq.example.com"
                },
                "tweet_id": {
                    "type": "string",
                    "description": "Filter URLs by a specific tweet ID. Use with 'eq' operator. Example: tweet_id=eq.1234567890. Note: This is a Foreign Key to tweets.tweet_id.<fk table='tweets' column='tweet_id'/>"
                },
                "select": {
                    "type": "string",
                    "description": "Specify which fields to return in the response. Use '*' for all fields or provide a comma-separated list of field names."
                },
                "order": {
                    "type": "string",
                    "description": "Specify the field(s) and direction for ordering results. Format: field.asc or field.desc. Use comma for multiple fields."
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of records to skip before starting to return results."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return."
                }
            },
            "required": [],
            "optional": [
                "id",
                "url",
                "expanded_url",
                "display_url",
                "tweet_id",
                "select",
                "order",
                "offset",
                "limit"
            ],
            "additionalProperties": true
        }
    },
    {
        "name": "get_mentioned_users",
        "url": "https://fabxmporizzqflnftavs.supabase.co/rest/v1/mentioned_users",
        "method": "GET",
        "headers": {
            "apikey": "{{COMMUNITY_ARCHIVE_API_KEY}}",
            "Authorization": "Bearer {{COMMUNITY_ARCHIVE_API_KEY}}"
        },
        "description": "Retrieves a list of users that have been mentioned in tweets from the 'mentioned_users' PostgREST endpoint of the Twitter Community Archive API. It provides key details on each user. Must use PostgREST operators (e.g., eq, neq, gt, gte, lt, lte, like, ilike) for filtering.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "Filter mentioned users by a specific user ID. Use with 'eq' operator. Example: user_id=eq.123456. Note: This is a Primary Key.<pk/>"
                },
                "name": {
                    "type": "string",
                    "description": "Filter mentioned users by their name. Use with 'eq' or 'ilike' operators. Example: name=ilike.*John*"
                },
                "screen_name": {
                    "type": "string",
                    "description": "Filter mentioned users by their screen name. Use with 'eq' or 'ilike' operators. Example: screen_name=eq.johndoe"
                },
                "updated_at": {
                    "type": "string",
                    "description": "Filter mentioned users by the last updated timestamp. Use 'gt', 'gte', 'lt', 'lte' for comparison. Format: timestamp with time zone. Example: updated_at=gte.2023-01-01T00:00:00Z"
                },
                "select": {
                    "type": "string",
                    "description": "Specify which fields to return in the response. Use '*' for all fields or provide a comma-separated list of field names."
                },
                "order": {
                    "type": "string",
                    "description": "Specify the field(s) and direction for ordering results. Format: field.asc or field.desc. Use comma for multiple fields."
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of records to skip before starting to return results."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return."
                }
            },
            "required": [],
            "optional": [
                "user_id",
                "name",
                "screen_name",
                "updated_at",
                "select",
                "order",
                "offset",
                "limit"
            ],
            "additionalProperties": true
        }
    },
    {
        "name": "get_followers",
        "url": "https://fabxmporizzqflnftavs.supabase.co/rest/v1/followers",
        "method": "GET",
        "headers": {
            "apikey": "{{COMMUNITY_ARCHIVE_API_KEY}}",
            "Authorization": "Bearer {{COMMUNITY_ARCHIVE_API_KEY}}"
        },
        "description": "Retrieves a list of follower relationships from the 'followers' PostgREST endpoint of the Twitter Community Archive API, providing insights into user interactions and connections. Must use PostgREST operators (e.g., eq, neq, gt, gte, lt, lte, like, ilike) for filtering.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Filter by a specific ID of the follower relationship. Use with 'eq' operator. Example: id=eq.123. Note: This is a Primary Key.<pk/>"
                },
                "account_id": {
                    "type": "string",
                    "description": "Filter follower relationships by a specific account ID. Use with 'eq' operator. Example: account_id=eq.abc123. Note: This is a Foreign Key to `account.account_id`.<fk table='account' column='account_id'/>"
                },
                "follower_account_id": {
                    "type": "string",
                    "description": "Filter by a specific follower account ID. Use with 'eq' operator. Example: follower_account_id=eq.xyz789."
                },
                "archive_upload_id": {
                    "type": "integer",
                    "description": "Filter by archive upload ID. Use with 'eq' operator. Example: archive_upload_id=eq.456. Note: This is a Foreign Key to `archive_upload.id`.<fk table='archive_upload' column='id'/>"
                },
                "select": {
                    "type": "string",
                    "description": "Specify which fields to return in the response. Use '*' for all fields or provide a comma-separated list of field names."
                },
                "order": {
                    "type": "string",
                    "description": "Specify the field(s) and direction for ordering results. Format: field.asc or field.desc. Use comma for multiple fields."
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of records to skip before starting to return results."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return."
                }
            },
            "required": [],
            "optional": [
                "id",
                "account_id",
                "follower_account_id",
                "archive_upload_id",
                "select",
                "order",
                "offset",
                "limit"
            ],
            "additionalProperties": true
        }
    },
    {
        "name": "get_archive_uploads",
        "url": "https://fabxmporizzqflnftavs.supabase.co/rest/v1/archive_upload",
        "method": "GET",
        "headers": {
            "apikey": "{{COMMUNITY_ARCHIVE_API_KEY}}",
            "Authorization": "Bearer {{COMMUNITY_ARCHIVE_API_KEY}}"
        },
        "description": "Retrieves information about Twitter data uploads from the 'archive_uploads' PostgREST endpoint of the Twitter Community Archive. Must use PostgREST operators (e.g., eq, neq, gt, gte, lt, lte, like, ilike) for filtering.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Filter by a specific upload ID. Use with 'eq' operator. Example: id=eq.123. Note: This is a Primary Key.<pk/>"
                },
                "account_id": {
                    "type": "string",
                    "description": "Filter uploads by a specific account ID. Use with 'eq' operator. Example: account_id=eq.abc123. Note: This is a Foreign Key to account.account_id.<fk table='account' column='account_id'/>"
                },
                "archive_at": {
                    "type": "string",
                    "description": "Filter uploads by the archive timestamp. Use 'gt', 'gte', 'lt', 'lte' for comparisons. Example: archive_at=gte.2023-01-01. Format: timestamp with time zone"
                },
                "created_at": {
                    "type": "string",
                    "description": "Filter uploads by the creation timestamp. Use 'gt', 'gte', 'lt', 'lte' for comparisons. Example: created_at=lt.2023-12-31. Format: timestamp with time zone"
                },
                "select": {
                    "type": "string",
                    "description": "Specify which fields to return in the response. Use '*' for all fields or provide a comma-separated list of field names."
                },
                "order": {
                    "type": "string",
                    "description": "Specify the field(s) and direction for ordering results. Format: field.asc or field.desc. Use comma for multiple fields."
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of records to skip before starting to return results."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return."
                }
            },
            "required": [],
            "optional": [
                "id",
                "account_id",
                "archive_at",
                "created_at",
                "select",
                "order",
                "offset",
                "limit"
            ],
            "additionalProperties": true
        }
    },
    {
        "name": "get_liked_tweets",
        "url": "https://fabxmporizzqflnftavs.supabase.co/rest/v1/liked_tweets",
        "method": "GET",
        "headers": {
            "apikey": "{{COMMUNITY_ARCHIVE_API_KEY}}",
            "Authorization": "Bearer {{COMMUNITY_ARCHIVE_API_KEY}}"
        },
        "description": "Retrieves tweets liked by users from the 'liked_tweets' PostgREST endpoint of the Twitter Community Archive, with the option to filter by tweet ID or full text. You must use PostgREST compatible operators (e.g., eq, neq, gt, gte, lt, lte, ilike, like, fts, plfts, phfts) for filtering.",
        "parameters": {
            "type": "object",
            "properties": {
                "tweet_id": {
                    "type": "string",
                    "description": "Filter by a specific tweet ID. Use with 'eq' operator. Example: tweet_id=eq.1234567890. Note: This is a Primary Key.<pk/>"
                },
                "full_text": {
                    "type": "string",
                    "description": "Filter by the full text of the liked tweets. Use with 'ilike' or 'fts' operators. Example: full_text=ilike.*keyword*"
                },
                "select": {
                    "type": "string",
                    "description": "Specify which fields to return in the response. Use '*' for all fields or provide a comma-separated list of field names."
                },
                "order": {
                    "type": "string",
                    "description": "Specify the field(s) and direction for ordering results. Format: field.asc or field.desc. Use comma for multiple fields."
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of records to skip before starting to return results."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return."
                }
            },
            "required": [],
            "optional": [
                "tweet_id",
                "full_text",
                "select",
                "order",
                "offset",
                "limit"
            ],
            "additionalProperties": true
        }
    },
    {
        "name": "get_following_accounts",
        "url": "https://fabxmporizzqflnftavs.supabase.co/rest/v1/following",
        "method": "GET",
        "headers": {
            "apikey": "{{COMMUNITY_ARCHIVE_API_KEY}}",
            "Authorization": "Bearer {{COMMUNITY_ARCHIVE_API_KEY}}"
        },
        "description": "Retrieves linked account IDs for users who have uploaded their data and users they are following from the 'following' PostgREST endpoint of the Twitter Community Archive. It allows for filtering by account ID and archive upload ID. You must use PostgREST compatible operators (e.g., eq, neq, gt, gte, lt, lte, ilike, like) for filtering.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Filter by specific record ID. Use with 'eq' operator. Example: id=eq.123. Note: This is a Primary Key.<pk/>"
                },
                "account_id": {
                    "type": "string",
                    "description": "Filter results by a specific account ID. Use with 'eq' operator. Example: account_id=eq.abc123. Note: This is a Foreign Key to account.account_id.<fk table='account' column='account_id'/>"
                },
                "following_account_id": {
                    "type": "string",
                    "description": "Filter results by the ID of the account being followed. Use with 'eq' operator. Example: following_account_id=eq.xyz789."
                },
                "archive_upload_id": {
                    "type": "integer",
                    "description": "Filter results by archive upload ID. Use with 'eq' operator. Example: archive_upload_id=eq.456. Note: This is a Foreign Key to archive_upload.id.<fk table='archive_upload' column='id'/>"
                },
                "select": {
                    "type": "string",
                    "description": "Specify which fields to return in the response. Use '*' for all fields or provide a comma-separated list of field names."
                },
                "order": {
                    "type": "string",
                    "description": "Specify the field(s) and direction for ordering results. Format: field.asc or field.desc. Use comma for multiple fields."
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of records to skip before starting to return results."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return."
                }
            },
            "required": [],
            "optional": [
                "id",
                "account_id",
                "following_account_id",
                "archive_upload_id",
                "select",
                "order",
                "offset",
                "limit"
            ],
            "additionalProperties": true
        }
    },
    {
        "name": "get_tweet_media",
        "url": "https://fabxmporizzqflnftavs.supabase.co/rest/v1/tweet_media",
        "method": "GET",
        "headers": {
            "apikey": "{{COMMUNITY_ARCHIVE_API_KEY}}",
            "Authorization": "Bearer {{COMMUNITY_ARCHIVE_API_KEY}}"
        },
        "description": "Retrieves information about media shared in tweets from the 'tweet_media' PostgREST endpoint of the Twitter Community Archive. It includes details such as media URLs, types, and dimensions. You must use PostgREST compatible operators (e.g., eq, neq, gt, gte, lt, lte, like, ilike) for filtering.",
        "parameters": {
            "type": "object",
            "properties": {
                "media_id": {
                    "type": "integer",
                    "description": "Filter media by a specific media ID. Use with 'eq' operator. Example: media_id=eq.123. Note: This is a Primary Key.<pk/>"
                },
                "tweet_id": {
                    "type": "string",
                    "description": "Filter media by the associated tweet ID. Use with 'eq' operator. Example: tweet_id=eq.abc123. Note: This is a Foreign Key to `tweets.tweet_id`.<fk table='tweets' column='tweet_id'/>"
                },
                "media_url": {
                    "type": "string",
                    "description": "Filter by the media URL. Use with 'eq' or 'ilike' operators. Example: media_url=ilike.*example.com*"
                },
                "media_type": {
                    "type": "string",
                    "description": "Filter by the type of media. Use with 'eq' operator. Example: media_type=eq.photo"
                },
                "width": {
                    "type": "integer",
                    "description": "Filter media by width. Use comparison operators such as 'gt', 'lt', 'gte', 'lte'. Example: width=gte.1000"
                },
                "height": {
                    "type": "integer",
                    "description": "Filter media by height. Use comparison operators such as 'gt', 'lt', 'gte', 'lte'. Example: height=lt.800"
                },
                "archive_upload_id": {
                    "type": "integer",
                    "description": "Filter media by archive upload ID. Use with 'eq' operator. Example: archive_upload_id=eq.456. Note: This is a Foreign Key to `archive_upload.id`.<fk table='archive_upload' column='id'/>"
                },
                "select": {
                    "type": "string",
                    "description": "Specify which fields to return in the response. Use '*' for all fields or provide a comma-separated list of field names."
                },
                "order": {
                    "type": "string",
                    "description": "Specify the field(s) and direction for ordering results. Format: field.asc or field.desc. Use comma for multiple fields."
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of records to skip before starting to return results."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return."
                }
            },
            "required": [],
            "optional": [
                "media_id",
                "tweet_id",
                "media_url",
                "media_type",
                "width",
                "height",
                "archive_upload_id",
                "select",
                "order",
                "offset",
                "limit"
            ],
            "additionalProperties": true
        }
    },
    {
        "name": "get_account_info",
        "url": "https://fabxmporizzqflnftavs.supabase.co/rest/v1/account",
        "method": "GET",
        "headers": {
            "apikey": "{{COMMUNITY_ARCHIVE_API_KEY}}",
            "Authorization": "Bearer {{COMMUNITY_ARCHIVE_API_KEY}}"
        },
        "description": "Retrieves information about accounts of users who have uploaded their data from the 'account' PostgREST endpoint of the Twitter Community Archive, including URLs. Must use PostgREST operators (e.g., eq, neq, gt, gte, lt, lte, like, ilike) for filtering.",
        "parameters": {
            "type": "object",
            "properties": {
                "account_id": {
                    "type": "string",
                    "description": "Filter accounts by a specific account ID. Use with 'eq' operator. Example: account_id=eq.123456. Note: This is a Primary Key.<pk/>"
                },
                "created_via": {
                    "type": "string",
                    "description": "Filter accounts based on how they were created. Use with 'eq' or 'ilike' operators. Example: created_via=eq.mobile"
                },
                "username": {
                    "type": "string",
                    "description": "Filter accounts by specific username. Use with 'eq' for exact match or 'ilike' for case-insensitive pattern matching. Example: username=eq.johndoe or username=ilike.*john*"
                },
                "created_at": {
                    "type": "string",
                    "description": "Filter accounts by creation timestamp. Use with 'gt', 'gte', 'lt', 'lte' operators. Format: timestamp with time zone. Example: created_at=gte.2023-01-01T00:00:00Z"
                },
                "account_display_name": {
                    "type": "string",
                    "description": "Filter accounts by display name. Use with 'eq' for exact match or 'ilike' for case-insensitive pattern matching. Example: account_display_name=ilike.*John Doe*"
                },
                "select": {
                    "type": "string",
                    "description": "Specify which fields to return in the response. Use '*' for all fields or provide a comma-separated list of field names."
                },
                "order": {
                    "type": "string",
                    "description": "Specify the field(s) and direction for ordering results. Format: field.asc or field.desc. Use comma for multiple fields."
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of records to skip before starting to return results."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return."
                }
            },
            "required": [],
            "optional": [
                "account_id",
                "created_via",
                "username",
                "created_at",
                "account_display_name",
                "select",
                "order",
                "offset",
                "limit"
            ],
            "additionalProperties": true
        }
    },
    {
        "name": "get_user_profiles",
        "url": "https://fabxmporizzqflnftavs.supabase.co/rest/v1/profile",
        "method": "GET",
        "headers": {
            "apikey": "{{COMMUNITY_ARCHIVE_API_KEY}}",
            "Authorization": "Bearer {{COMMUNITY_ARCHIVE_API_KEY}}"
        },
        "description": "Retrieves profile information for Twitter users who have uploaded their data from the 'profile' PostgREST endpoint of the Twitter Community Archive. It allows filtering by various attributes using PostgREST operators (e.g., eq, neq, gt, gte, lt, lte, like, ilike).",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Filter profiles by a specific user profile ID. Use with 'eq' operator. Example: id=eq.123. Note: This is a Primary Key.<pk/>"
                },
                "account_id": {
                    "type": "string",
                    "description": "Filter profiles by a specific account ID. Use with 'eq' operator. Example: account_id=eq.abc123. Note: This is a Foreign Key to account.account_id.<fk table='account' column='account_id'/>"
                },
                "archive_upload_id": {
                    "type": "integer",
                    "description": "Filter profiles by archive upload ID. Use with 'eq' operator. Example: archive_upload_id=eq.456. Note: This is a Foreign Key to archive_upload.id.<fk table='archive_upload' column='id'/>"
                },
                "bio": {
                    "type": "string",
                    "description": "Filter profiles that include specific text in the bio. Use 'ilike' for case-insensitive pattern matching. Example: bio=ilike.*developer*"
                },
                "website": {
                    "type": "string",
                    "description": "Filter profiles with specific website URLs. Use 'ilike' for case-insensitive pattern matching. Example: website=ilike.*github.com*"
                },
                "location": {
                    "type": "string",
                    "description": "Filter profiles based on location information. Use 'ilike' for case-insensitive pattern matching. Example: location=ilike.*New York*"
                },
                "avatar_media_url": {
                    "type": "string",
                    "description": "Filter profiles by specific avatar media URLs. Use 'ilike' for case-insensitive pattern matching. Example: avatar_media_url=ilike.*profile_pic*"
                },
                "header_media_url": {
                    "type": "string",
                    "description": "Filter profiles by specific header media URLs. Use 'ilike' for case-insensitive pattern matching. Example: header_media_url=ilike.*banner*"
                },
                "select": {
                    "type": "string",
                    "description": "Specify which fields to return in the response. Use '*' for all fields or provide a comma-separated list of field names."
                },
                "order": {
                    "type": "string",
                    "description": "Specify the field(s) and direction for ordering results. Format: field.asc or field.desc. Use comma for multiple fields."
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of records to skip before starting to return results."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return."
                }
            },
            "required": [],
            "optional": [
                "id",
                "account_id",
                "archive_upload_id",
                "bio",
                "website",
                "location",
                "avatar_media_url",
                "header_media_url",
                "select",
                "order",
                "offset",
                "limit"
            ],
            "additionalProperties": true
        }
    },
    {
        "name": "get_tweets",
        "url": "https://fabxmporizzqflnftavs.supabase.co/rest/v1/tweets",
        "method": "GET",
        "headers": {
            "apikey": "{{COMMUNITY_ARCHIVE_API_KEY}}",
            "Authorization": "Bearer {{COMMUNITY_ARCHIVE_API_KEY}}"
        },
        "description": "Retrieves a list of tweets from the 'tweets' PostgREST endpoint of the Twitter Community Archive API. It supports filtering, pagination, and ordering using PostgREST operators (e.g., eq, neq, gt, gte, lt, lte, like, ilike).",
        "parameters": {
            "type": "object",
            "properties": {
                "tweet_id": {
                    "type": "string",
                    "description": "Filter tweets by a specific tweet ID. Use with 'eq' operator. Example: tweet_id=eq.123456789. Note: This is a Primary Key.<pk/>"
                },
                "account_id": {
                    "type": "string",
                    "description": "Filter tweets by a specific account ID. Use with 'eq' operator. Example: account_id=eq.abc123. Note: This is a Foreign Key to `account.account_id`.<fk table='account' column='account_id'/>"
                },
                "created_at": {
                    "type": "string",
                    "description": "Filter tweets by creation timestamp. Use 'gt', 'gte', 'lt', 'lte' for comparison. Format: timestamp with time zone. Example: created_at=gte.2023-01-01T00:00:00Z"
                },
                "full_text": {
                    "type": "string",
                    "description": "Filter tweets by exact text match. Use 'eq' for exact match, 'ilike' for case-insensitive pattern matching, or 'like' for case-sensitive pattern matching. Use 'fts', 'plfts', or 'phfts' for full-text search. Example: full_text=ilike.*important announcement*"
                },
                "retweet_count": {
                    "type": "integer",
                    "description": "Filter tweets by retweet count. Use 'eq', 'gt', 'gte', 'lt', 'lte' for comparison. Example: retweet_count=gte.100"
                },
                "favorite_count": {
                    "type": "integer",
                    "description": "Filter tweets by favorite count. Use 'eq', 'gt', 'gte', 'lt', 'lte' for comparison. Example: favorite_count=gte.50"
                },
                "reply_to_tweet_id": {
                    "type": "string",
                    "description": "Filter tweets that are replies to a specific tweet ID. Use with 'eq' operator. Example: reply_to_tweet_id=eq.987654321"
                },
                "reply_to_user_id": {
                    "type": "string",
                    "description": "Filter tweets that are replies to a specific user ID. Use with 'eq' operator. Example: reply_to_user_id=eq.user123"
                },
                "reply_to_username": {
                    "type": "string",
                    "description": "Filter tweets that are replies to a specific username. Use 'eq' for exact match, 'ilike' for case-insensitive pattern matching. Example: reply_to_username=eq.johndoe"
                },
                "archive_upload_id": {
                    "type": "integer",
                    "description": "Filter tweets by archive upload ID. Use with 'eq' operator. Example: archive_upload_id=eq.789. Note: This is a Foreign Key to `archive_upload.id`.<fk table='archive_upload' column='id'/>"
                },
                "select": {
                    "type": "string",
                    "description": "Specify which fields to return in the response. Use '*' for all fields or provide a comma-separated list of field names."
                },
                "order": {
                    "type": "string",
                    "description": "Specify the field(s) and direction for ordering results. Format: field.asc or field.desc. Use comma for multiple fields."
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of records to skip before starting to return results."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return."
                }
            },
            "required": [],
            "optional": [
                "tweet_id",
                "account_id",
                "created_at",
                "full_text",
                "retweet_count",
                "favorite_count",
                "reply_to_tweet_id",
                "reply_to_user_id",
                "reply_to_username",
                "archive_upload_id",
                "select",
                "order",
                "offset",
                "limit"
            ],
            "additionalProperties": true
        }
    },
    {
        "name": "get_likes",
        "url": "https://fabxmporizzqflnftavs.supabase.co/rest/v1/likes",
        "method": "GET",
        "headers": {
            "apikey": "{{COMMUNITY_ARCHIVE_API_KEY}}",
            "Authorization": "Bearer {{COMMUNITY_ARCHIVE_API_KEY}}"
        },
        "description": "Retrieves a list of likes associated with user accounts and the tweets they have liked from the 'likes' PostgREST endpoint. It provides options for filtering and pagination using PostgREST operators (e.g., eq, neq, gt, gte, lt, lte, like, ilike).",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Filter likes by a specific ID. Use with 'eq' operator. Example: id=eq.123. Note: This is a Primary Key.<pk/>"
                },
                "account_id": {
                    "type": "string",
                    "description": "Filter likes by a specific account ID. Use with 'eq' operator. Example: account_id=eq.abc123. Note: This is a Foreign Key to `account.account_id`.<fk table='account' column='account_id'/>"
                },
                "liked_tweet_id": {
                    "type": "string",
                    "description": "Filter likes by a specific liked tweet ID. Use with 'eq' operator. Example: liked_tweet_id=eq.987654321. Note: This is a Foreign Key to `liked_tweets.tweet_id`.<fk table='liked_tweets' column='tweet_id'/>"
                },
                "archive_upload_id": {
                    "type": "integer",
                    "description": "Filter likes by archive upload ID. Use with 'eq' operator. Example: archive_upload_id=eq.456. Note: This is a Foreign Key to `archive_upload.id`.<fk table='archive_upload' column='id'/>"
                },
                "select": {
                    "type": "string",
                    "description": "Specify which fields to return in the response. Use '*' for all fields or provide a comma-separated list of field names."
                },
                "order": {
                    "type": "string",
                    "description": "Specify the field(s) and direction for ordering results. Format: field.asc or field.desc. Use comma for multiple fields."
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of records to skip before starting to return results."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return."
                }
            },
            "required": [],
            "optional": [
                "id",
                "account_id",
                "liked_tweet_id",
                "archive_upload_id",
                "select",
                "order",
                "offset",
                "limit"
            ],
            "additionalProperties": true
        }
    },
    {
        "name": "get_user_mentions",
        "url": "https://fabxmporizzqflnftavs.supabase.co/rest/v1/user_mentions",
        "method": "GET",
        "headers": {
            "apikey": "{{COMMUNITY_ARCHIVE_API_KEY}}",
            "Authorization": "Bearer {{COMMUNITY_ARCHIVE_API_KEY}}"
        },
        "description": "Retrieves linked IDs for users mentioned and the tweets that mentioned them from the 'user_mentions' PostgREST endpoint of the Twitter Community Archive. Use PostgREST operators (e.g., eq, neq, gt, gte, lt, lte, like, ilike) for filtering.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Retrieve specific user mention by its unique identifier. Use with 'eq' operator. Example: id=eq.789. Note: This is a Primary Key.<pk/>"
                },
                "mentioned_user_id": {
                    "type": "string",
                    "description": "Filter user mentions by the ID of the mentioned user. Use with 'eq' operator. Example: mentioned_user_id=eq.user456. Note: This is a Foreign Key to `mentioned_users.user_id`.<fk table='mentioned_users' column='user_id'/>"
                },
                "tweet_id": {
                    "type": "string",
                    "description": "Filter user mentions by the tweet ID in which the user was mentioned. Use with 'eq' operator. Example: tweet_id=eq.123456789. Note: This is a Foreign Key to `tweets.tweet_id`.<fk table='tweets' column='tweet_id'/>"
                },
                "select": {
                    "type": "string",
                    "description": "Specify which fields to return in the response. Use '*' for all fields or provide a comma-separated list of field names."
                },
                "order": {
                    "type": "string",
                    "description": "Specify the field(s) and direction for ordering results. Format: field.asc or field.desc. Use comma for multiple fields."
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of records to skip before starting to return results."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return."
                }
            },
            "required": [],
            "optional": [
                "id",
                "mentioned_user_id",
                "tweet_id",
                "select",
                "order",
                "offset",
                "limit"
            ],
            "additionalProperties": true
        }
    },
]


def split_tool_schema(tool_schema):
    """
    Splits tool schema into endpoint schema and request schema.

    Args:
        tool_schema: The tool schema to split.
    """    
    for item in tool_schema:
        endpoint = {key: item[key] for key in item if key not in ['description', 'parameters', 'additionalProperties']}
        schema = {key: item[key] for key in item if key in ['name', 'description', 'parameters', 'additionalProperties']}

    return endpoint, schema


def wrap_tool_schema(tool_schema):
    """
    Wraps tool schema in a function that can be used by an OpenAI assistant.

    Args:
        tool_schema: The tool schema to wrap.
    """
    function = {
        "type": "function",
        "function": tool_schema
    }

    return function

def validate_calls(calls):
    """
    Validates the calls to the API.

    Args:
        calls: The calls to validate.
    """
    if calls:
        for call in calls:
            assert isinstance(call, dict), f"Invalid call format: {call}"
            # If there's a key named "action", rename it to "name"
            if "action" in call:
                call["name"] = call.pop("action")
            # If there's a key named "action_input", rename it to "parameters"
            if "action_input" in call:
                call["parameters"] = call.pop("action_input")
    
    return calls
