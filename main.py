import webapp2
import jinja2
import os
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore

from profile import Profile
from uploadhandler import UploadHandler
from photohandler import PhotoHandler

from services import Services
from user import User
from usermodel import UserModel


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=["jinja2.ext.autoescape"],
                                       autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        user = Services().get_current_user()
        myuser = None
        feeds = None
        editfeed = None

        if user:
            url = users.create_logout_url(self.request.uri)
            myuser_key = ndb.Key("User", Services().get_current_user_id())
            myuser = myuser_key.get()

            if myuser == None:
                myuser = Services().create_user(user_id= user.user_id())

            user_name = self.request.GET.get("user_name")
            bio_text = self.request.GET.get("bio_text")

            if user_name != None and user_name != "" and bio_text != None and bio_text != "":

                user_query = User.query(User.user_name == user_name).fetch()

                if len(user_query) > 0:
                    self.redirect("/")
                    return

                myuser.user_name = user_name
                myuser.bio_text = bio_text
                myuser.put()

            feeds = UserModel.query().order(-UserModel.time)
            search_type = self.request.GET.get("query_type")

            if search_type == "user" or search_type == "post":

                search_text = self.request.GET.get("search_text")

                if len(search_text) > 0:

                    if search_type == "user":
                        feeds = Services().search_by_user(text=search_text)
                    else:
                        feeds = Services().search_by_tweet(text=search_text)


            elif search_type == "Delete" or search_type == "Edit":

                query_type = self.request.GET.get("query_type")
                tweet_id = self.request.GET.get("feed_id")

                if query_type == "Edit":
                    editfeed = Services().get_tweet(tweet_id = tweet_id)
                    feeds = Services().get_all_user_tweets()

                else:
                    Services().delete_tweet(tweet_id = tweet_id)
                    self.redirect("/")

            else:
                feeds = Services().get_all_user_tweets()

        else:
            url = users.create_login_url(self.request.uri)


        template_values = {
            "url": url,
            "myuser": myuser,
            "feeds":feeds,
            "editfeed":editfeed,
            "upload_url" : blobstore.create_upload_url('/upload_photo')
        }

        template = JINJA_ENVIRONMENT.get_template("main.html")
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ("/profile", Profile),
    ("/upload_photo", UploadHandler),
    ('/view_photo/([^/]+)?', PhotoHandler)
], debug=True)







