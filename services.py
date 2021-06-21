from google.appengine.api import users
from google.appengine.ext import ndb

from usermodel import UserModel
from user import User

class Services(object):

    def create_user(self,user_id):

        myuser = User(id=user_id, user_id=str(user_id))
        myuser.user_name = ""
        myuser.user_following = []
        myuser.put()
        return myuser

    def get_current_user(self):
        return users.get_current_user()


    def get_current_user_id(self):
        return users.get_current_user().user_id()


    def get_login_user(self):
        myuser_key = ndb.Key("User", Services().get_current_user_id())
        return  myuser_key.get()

    def search_by_tweet(self,text):
        limit = text[:-1] + chr(ord(text[-1]) + 1)
        return UserModel.query(UserModel.share_text >= text, UserModel.share_text < limit)

    def search_by_user(self,text):
        limit = text[:-1] + chr(ord(text[-1]) + 1)
        return UserModel.query(UserModel.user_name >= text, UserModel.user_name < limit)

    def delete_tweet(self,tweet_id):

        myuser = Services().get_login_user()
        tweet_ids = myuser.tweet_ids
        tweet_ids.remove(int(tweet_id))
        myuser.tweet_ids = tweet_ids
        myuser.put()

        tweet_key = ndb.Key("UserModel", int(tweet_id))
        tweet = tweet_key.get()
        tweet.key.delete()

    def get_tweet(self,tweet_id):

        tweet_key = ndb.Key("UserModel", int(tweet_id))
        tweet = tweet_key.get()
        return tweet

    def get_all_user_tweets(self):
        myuser = Services().get_login_user()
        feeds = []
        for feed in UserModel.query().order(-UserModel.time).fetch():
            if feed.user_id in myuser.user_following or feed.user_id == myuser.key.id():
                feeds.append(feed)
        return feeds


