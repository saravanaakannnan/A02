from google.appengine.ext import ndb
from google.appengine.api import users

class AnagramList(ndb.Model):
    words = ndb.StringProperty(repeated = True)
    lexicographical = ndb.StringProperty()
    no_of_words = ndb.IntegerProperty()
    letters_in_the_word =  ndb.IntegerProperty()
    email = ndb.StringProperty()
