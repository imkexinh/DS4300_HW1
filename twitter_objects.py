"""
tweet object class for Twitter database
"""

class Tweet:
    """
    represents a tweet in the Twitter system
    """
    
    def __init__(self, user_id, tweet_text, tweet_id=None, tweet_ts=None):
        """
        initialize a Tweet object
        """
        self.user_id = user_id
        self.tweet_text = tweet_text
        self.tweet_id = tweet_id
        self.tweet_ts = tweet_ts
    
    def __str__(self):
        """
        string representation of the tweet
        """
        if self.tweet_ts:
            return f"tweet {self.tweet_id} by User {self.user_id} at {self.tweet_ts}: {self.tweet_text}"
        else:
            return f"tweet by User {self.user_id}: {self.tweet_text}"
    
    def __repr__(self):
        return self.__str__()
