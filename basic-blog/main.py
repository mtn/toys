import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Posts(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateProperty(auto_now_add = True)

class MainPage(Handler):
    def get(self):
        posts = db.GqlQuery("select * from Posts order by created desc limit 10")
        self.render("main.html", posts=posts)

class NewPost(Handler):
    def render_newpage(self, subject = "", post = "", error = ""):
        self.render("new_post.html", subject=subject, post=post, error=error)

    def get(self):
        self.render_newpage()

    def post(self):
        subject = self.request.get('subject')
        post = self.request.get('post')
        error = ""

        if subject and post:
            a = Posts(subject=subject, content=post)
            a.put()
            # TODO redirect to new post permalink
        else:
            error = "Please provide both a subject and a post!"
            self.render_newpage(subject,post,error)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/newpost', NewPost),
                              ],
                              debug = True)