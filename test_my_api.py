"""
test script to verify Twitter API works
"""

import os
from twitter_api import TwitterAPI
from twitter_objects import Tweet

def test_api():
    """test all API methods"""
    MYSQL_USER = "root"
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = "twitter_db"

    # initialize API
    api = TwitterAPI(MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
    print("connected successfully")
    
    # post a tweet
    test_tweet = Tweet(user_id=1, tweet_text="test tweet")
    api.post_tweet(test_tweet)
    print("tweet posted successfully")
    
    # post some tweets
    for i in range(5):
        tweet = Tweet(user_id=2, tweet_text=f"test tweet number {i}")
        api.post_tweet(tweet)
    print("a few tweets posted successfully")
    
    # get followees
    followees = api.get_followees(user_id=1)
    print(f"user 1 follows: {followees}")
    
    # get followers
    followers = api.get_followers(user_id=2)
    print(f"user 2 is followed by: {followers}")
    
    # get user's own tweets
    tweets = api.get_tweets(user_id=2, limit=5)
    print(f"retrieved {len(tweets)} tweets from User 2:")
    for tweet in tweets:
        print(f"   - {tweet}")
    
    # get home timeline
    print("getting timeline for User 1 (who follows users: {})".format(followees))
    timeline = api.get_home_timeline(user_id=1)
    print(f"retrieved {len(timeline)} tweets in home timeline:")
    for tweet in timeline:
        print(f"   - {tweet}")
    
    # Close connection
    api.close()


if __name__ == '__main__':
    test_api()
