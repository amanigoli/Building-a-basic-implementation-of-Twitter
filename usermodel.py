from google.appengine.ext import ndb

class UserModel(ndb.Model):

    share_text = ndb.StringProperty()
    user_id = ndb.StringProperty()
    user_name = ndb.StringProperty()
    time = ndb.DateTimeProperty()
    display = ndb.BlobKeyProperty()