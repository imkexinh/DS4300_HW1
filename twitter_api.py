"""
Twitter Database API for MySQL
"""

from dbutils import DBUtils
from twitter_objects import Tweet

class TwitterAPI:
    """
    API for interacting with the Twitter database
    """
    
    def __init__(self, user, password, database, host="localhost"):
        """
        initialize the Twitter API with database connection
        """
        self.dbu = DBUtils(user, password, database, host)
    
    def close(self):
        """close the database connection"""
        self.dbu.close()
    
    def post_tweet(self, tweet):
        """
        post a new tweet to the database
        """
        sql = "INSERT INTO tweet (user_id, tweet_ts, tweet_text) VALUES (%s, NOW(), %s)"
        val = (tweet.user_id, tweet.tweet_text)
        self.dbu.insert_one(sql, val)
    
    def get_home_timeline(self, user_id):
        """
        get the 10 most recent tweets from users that this user follows
        """
        sql = """
            SELECT tweet_id, user_id, tweet_ts, tweet_text
            FROM tweet
            WHERE user_id IN (
                SELECT followee_id 
                FROM follows 
                WHERE follower_id = %s
            )
            ORDER BY tweet_ts DESC
            LIMIT 10
        """
        # need to pass user_id
        sql_with_param = sql.replace('%s', str(user_id))
        df = self.dbu.execute(sql_with_param)
        
        # convert dataframe rows to Tweet objects
        tweets = []
        for i in range(len(df)):
            row = df.iloc[i]
            tweet = Tweet(
                user_id=row['user_id'],
                tweet_text=row['tweet_text'],
                tweet_id=row['tweet_id'],
                tweet_ts=row['tweet_ts']
            )
            tweets.append(tweet)
        
        return tweets
    
    def get_followees(self, user_id):
        """
        get a list of user IDs that this user follows
        """
        sql = f"SELECT followee_id FROM follows WHERE follower_id = {user_id}"
        df = self.dbu.execute(sql)
        return df['followee_id'].tolist()
    
    def get_followers(self, user_id):
        """
        get a list of user IDs that follow this user
        """
        sql = f"SELECT follower_id FROM follows WHERE followee_id = {user_id}"
        df = self.dbu.execute(sql)
        return df['follower_id'].tolist()
    
    def get_tweets(self, user_id, limit=10):
        """
        get the most recent tweets posted by a specific user
        """
        sql = f"""
            SELECT tweet_id, user_id, tweet_ts, tweet_text
            FROM tweet
            WHERE user_id = {user_id}
            ORDER BY tweet_ts DESC
            LIMIT {limit}
        """
        df = self.dbu.execute(sql)
        
        tweets = []
        for i in range(len(df)):
            row = df.iloc[i]
            tweet = Tweet(
                user_id=row['user_id'],
                tweet_text=row['tweet_text'],
                tweet_id=row['tweet_id'],
                tweet_ts=row['tweet_ts']
            )
            tweets.append(tweet)
        
        return tweets
