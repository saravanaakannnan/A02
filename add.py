# import webapp2
# import jinja2
# ##from itertools import groupby
# from google.appengine.api import users
# from google.appengine.ext import ndb
# from anagramlist import AnagramList
# import os
#
# JINJA_ENVIRONMENT = jinja2.Environment(
# loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
# extensions=['jinja2.ext.autoescape'],
# autoescape=True
# )
#
# class AddPage(webapp2.RequestHandler):
#     def get(self):
#         self.response.headers['Content-Type'] = 'text/html'
#         #user = users.get_current_user().email()
#         #query = AnagramList.query(AnagramList.email == users.get_current_user().email())
#         #template_values = {'query':query}
#         template_values = {}
#         template = JINJA_ENVIRONMENT.get_template('add.html')
#         self.response.write(template.render(template_values))
#
#
#     def post(self):
#         self.response.headers['content-Type'] = 'text/html'
#         user = users.get_current_user()
#         word = self.request.get('word')
#         sorted_word = ''.join(sorted(set(word.lower())))
#         email_id = users.get_current_user().email()
#         key = ndb.Key('AnagramList',sorted_word+email_id)
#         anagram_list = key.get()
#         if anagram_list==None:
#             anagram_list = AnagramList(id=sorted_word+email_id)
#             anagram_list.put()
#         anagram_list = key.get()
#         action = self.request.get('submit')
#         if action == 'add':
#             word = self.request.get('word')
#             if word == None or word == '':
#                 self.redirect('/')
#                 return
#             anagram_list.words.append(word)
#             anagram_list.lexicographical = sorted_word
#             anagram_list.no_of_words = len(anagram_list.words)
#             anagram_list.letters_in_the_word = len(anagram_list.lexicographical)
#             anagram_list.email = email_id
#         anagram_list.put()
#         self.redirect('/add')
