import webapp2
import jinja2
##from itertools import groupby
from google.appengine.api import users
from google.appengine.ext import ndb
from anagramlist import AnagramList
import os

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # and also a string to represent this
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        anagram_list = None
        a=[]
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            key = ndb.Key('AnagramList', user.user_id())
            email = users.get_current_user().email()
            word = self.request.get('word_text')
            sorted_word = ''.join(sorted(set(word.lower())))
            query=AnagramList.query(AnagramList.email==email)
            string8=None
            my_list1=None
            for i in query:
                if i.lexicographical in sorted_word:
                    if i.lexicographical==sorted_word:
                        pass
                    else:
                        string8=i.lexicographical
                        if string8==None:
                            pass
                        else:
                            key1=ndb.Key('MyList',string8+email)
                            my_list1=key1.get()
                            a.append(my_list1)
            key = ndb.Key('AnagramList', sorted_word+email)
            anagram_list = key.get()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {'url':url,'url_string':url_string,'user':user,'welcome':welcome, 'anagramlist1':anagram_list,'anagram_list':anagram_list,'a':a}
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))
    def post(self):
        self.response.headers['content-Type'] = 'text/html'
        user = users.get_current_user()
        word = self.request.get('word')
        sorted_word = ''.join(sorted(set(word.lower())))
        email_id = users.get_current_user().email()
        key = ndb.Key('AnagramList',sorted_word+email_id)
        anagram_list = key.get()
        if anagram_list==None:
            anagram_list = AnagramList(id=sorted_word+email_id)
            anagram_list.put()
        anagram_list = key.get()
        action = self.request.get('submit')
        if action == 'add':
            word = self.request.get('word')
            if word == None or word == '':
                self.redirect('/')
                return
            anagram_list.words.append(word)
            anagram_list.lexicographical = sorted_word
            anagram_list.no_of_words = len(anagram_list.words)
            anagram_list.letters_in_the_word = len(anagram_list.lexicographical)
            anagram_list.email = email_id
        anagram_list.put()
        self.redirect('/add')


class AddPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.out.write("<html><head></head><body>")
        self.response.out.write("""<form align ="center" method="post" action="/">
        word:<input type="text" name="word" pattern="[a-zA-Z]+" required = "true"/><br/>
        <input type="submit" name="submit" value="add"/>
        </form>""")
        self.response.out.write("<b><p><a href='/'>Home</a></p></b>")
        self.response.out.write("</body></html>")


class UniqueAnagram(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user().email()
        query = AnagramList.query(AnagramList.email == users.get_current_user().email())
        template_values = {'query':query}
        template = JINJA_ENVIRONMENT.get_template('uniqueanagram.html')
        self.response.write(template.render(template_values))

class ListofWords(webapp2.RequestHandler):
    def get(self):
        self.response.headers['content-type'] = 'text/html'
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('listofwords.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['content-type'] = 'text/html'
        user = users.get_current_user().email()
        tfile = self.request.get("fileToBeUploaded")
        tfile = tfile.split()
        for y in tfile:
            line = ''.join(sorted(set(y.lower())))
            key = ndb.Key('AnagramList', line+user)
            anagram_list = key.get()
            if anagram_list == None:
                anagram_list = AnagramList(id=line+user)
                anagram_list.put()
            anagram_list = key.get()
            anagram_list.words.append(y)
            anagram_list.lexicographical=line
            anagram_list.no_of_words = len(anagram_list.words)
            anagram_list.letters_in_the_word = len(anagram_list.lexicographical)
            anagram_list.email = user
            anagram_list.put()
        self.redirect('/')




app = webapp2.WSGIApplication([
('/', MainPage),('/add', AddPage),('/uniqueanagram', UniqueAnagram),('/listofwords', ListofWords)
], debug=True)
