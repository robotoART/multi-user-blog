import os
import re
from string import letters
import random
import hashlib
import hmac

import webapp2
import jinja2
from jinja2 import Environment

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class Utils:
    """ contains global functions commonly used """
    secret = '111-infinity0+infinity&beyond999'

    def render_str(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def make_secure_val(nonsecure_val):
        return "%s|%s" % (nonsecure_val, hmac.new(secret, nonsecure_val).hexdigest())

    def check_secure_val(secure_val):
        val = secure_val.split('|')[0]
        if secure_val == make_secure_val(val):
            return val

class Handler(webapp2.RequestHandler, Utils):
    """ webapp2.RequestHandler """
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return Utils.render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = Utils.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/blog' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies. get(name)
        return cookie_val and Utils.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/blog')

    #'initialize' function checks if user is loggedin to allow making posts
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)


### user functions
def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, pw, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, pw, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

##### blog stuff
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

### user class
class User(db.Model):
    """ this class creates a User object in the database """
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent = users_key())
    @classmethod
    def by_name(cls, name):
        u = cls.all().filter('name = ', name).get()
        return u
    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent= users_key(), name= name, pw_hash= pw_hash, email= email)
    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

class Post(db.Model, Utils):
    """ this class creates a Post object related to a User in the database """
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now_add = True)
    username = db.StringProperty(required = True)
    liked_by = db.StringListProperty(required = True)
    disd_by = db.StringListProperty(required = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return Utils.render_str("post.html", p= self, plks= len(self.liked_by), pdss= len(self.disd_by))

class Comment(db.Model, Utils):
    """ this class creates a Comment object related to a Post and a User in the database """
    post = db.ReferenceProperty(Post, collection_name= 'post_comments')
    comcontent = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    comusername = db.StringProperty(required = True)
    last_modified = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        self._render_text = self.comcontent.replace('\n', '<br>')
        return Utils.render_str("comment.html", c= self)

class BlogFront(Handler):
    """ this class goes to the front page with the latest 10 Posts """
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        if self.user:
            self.render('front.html', posts = posts, loggedinusername= self.user.name)
        else:
            self.render('front.html', posts = posts )


class PostPage(Handler):
    """ this class goes to a specific Post page """
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        ppost = db.get(key)
        pauthor = ppost.username
        pliked_by = ppost.liked_by
        plikes_qty = len(pliked_by)
        pdisd_by = ppost.disd_by
        pdiss_qty = len(pdisd_by)
        plby = False
        pdby = False
        comments = sorted(ppost.post_comments, key=lambda comments: comments.last_modified, reverse= True)

        if not ppost:
            self.error(404)
            return

        if self.user:
            loggeduser = self.user.name
            if pliked_by.count(loggeduser) > 0:
                plby = True
            if pdisd_by.count(loggeduser) > 0:
                pdby = True

            self.render("permalink.html", ppost= ppost, plby= plby, pdby= pdby, pls= plikes_qty, pid= post_id,
                         loggedinusername= loggeduser, pauthor= pauthor, pkey= key,
                         pds= pdiss_qty, plb= pliked_by, pdb= pdisd_by, comments= comments)
        else:
            self.render("permalink.html", ppost= ppost, comments= comments)

    def post(self, post_id):
        if self.request.get('add_com'):
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            p = db.get(key)
            comcontent = self.request.get('comment')
            if comcontent and self.user:
                c = Comment(comcontent= comcontent, comusername= self.user.name, post= key)
                c.put()
                self.redirect('/blog/%s' % str(p.key().id()))
                return
            else:
                self.render("permalink.html", ppost= key, comments= comments)
        else:
            self.redirect('/blog/%s' % str(p.key().id()))
            return


class NewPost(Handler):
    """ this class goes to the New Post Form page and handles new post submissions """
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect('/login')
            return

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        if self.user:
            if subject and content:
                p = Post(parent= blog_key(), subject= subject, content= content, username= self.user.name)
                p.put()
                self.redirect('/blog/%s' % str(p.key().id()))
                return
            else:
                error = "subject and content, please!"
                self.render("newpost.html", subject=subject, content=content, error=error)
        else:
            self.redirect('/login')
            return

class EditPost(Handler):
    """ this class goes to the Edit Post Form page and handles editing a post submissions """
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if post is not None:
            subject = post.subject
            content = post.content
            if self.user and self.user.name == post.username:
                self.render("editpost.html", subject= subject, content= content)
            elif self.user:
                self.redirect('/blog/%s' % str(post.key().id()))
                return
            else:
                self.redirect('/login')
                return
        else:
            self.redirect('/blog')
            return

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(key)
        if p is not None:
            subject = self.request.get('subject')
            content = self.request.get('content')
            if self.user and self.user.name == p.username:
                if subject and content:
                    p.subject = subject
                    p.content = content
                    #REGION DEBUGGER used to wipe likes and dislikes
                    # p.liked_by = []
                    # p.disd_by = []
                    p.put()
                    self.redirect('/blog/%s' % str(p.key().id()))
                    return
                else:
                    error = "subject and content, please!"
                    self.render("editpost.html", subject=subject, content=content, error=error)
            elif self.user:
                self.redirect('/blog/%s' % str(p.key().id()))
                return
            else:
                self.redirect('/login')
                return
        else:
            self.redirect('/blog')
            return


class EditComment(Handler):
    """ this class goes to the Edit Comment Form page and handles editing a comment submissions """
    def post(self, comment_id):
        edit_com_txtarea_name = 'comedit' + comment_id
        ctextupdate = self.request.get(edit_com_txtarea_name)
        key = db.Key.from_path('Comment', int(comment_id))
        cedit = db.get(key)
        cpostid = cedit.post.key().id()
        cuename = cedit.comusername
        if cedit is not None:
            if self.user and cuename == self.user.name:
                cedit.comcontent = ctextupdate
                cedit.put()
                self.redirect('/blog/%s' % str(cpostid))
                return
            elif self.user:
                self.redirect('/blog/%s' % str(cpostid))
                return
            else:
                self.redirect('/login')
                return
        else:
            self.redirect('/blog/%s' % str(cpostid))
            return

class DeletePost(Handler):
    """ this class handles deleting a post submission """
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        pdelete = db.get(key)
        pudname = pdelete.username
        if pdelete is not None:
            if self.user and pudname == self.user.name:
                pdelete.delete()
                for c in pdelete.post_comments:
                    c.delete()
                self.redirect('/blog')
                return
            elif self.user:
                self.redirect('/blog/%s' % str(pdelete.key().id()))
                return
            else:
                self.redirect('/login')
                return
        else:
            self.redirect('/blog/%s' % str(pdelete.key().id()))
            return

class DeleteComment(Handler):
    """ this class handles deleting a comment submission """
    def get(self, comment_id):
        key = db.Key.from_path('Comment', int(comment_id))
        cdelete = db.get(key)
        cpostid = cdelete.post.key().id()
        cudname = cdelete.comusername
        if cdelete is not None and cpostid is not None:
            if self.user and cudname == self.user.name:
                cdelete.delete()
                self.redirect('/blog/%s' % str(cpostid))
                return
            elif self.user:
                self.redirect('/blog/%s' % str(cpostid))
                return
            else:
                self.redirect('/login')
                return
        elif cdelete is not None and cpostid == None:
            self.redirect('/blog/%s' % str(cpostid))
            return
        else:
            self.redirect('/blog')
            return

class LikePost(Handler):
    """ this class handles Liking a post submission """
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        plike = db.get(key)
        lpliked_by = plike.liked_by
        luser = plike.username

        if self.user and luser != self.user.name and lpliked_by.count(self.user.name) == 0:
            lpliked_by.append(self.user.name)
            plike.liked_by = lpliked_by
            plike.put()
            self.redirect('/blog/%s' % str(plike.key().id()))
            return
        elif self.user:
            self.redirect('/blog/%s' % str(plike.key().id()))
            return
        else:
            self.redirect('/login')
            return

class DisPost(Handler):
    """ this class handles Disliking a post submission """
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        pdis = db.get(key)
        lpdisd_by = pdis.disd_by
        luser = pdis.username

        if self.user and luser != self.user.name and lpdisd_by.count(self.user.name) == 0:
            lpdisd_by.append(self.user.name)
            pdis.disd_by = lpdisd_by
            pdis.put()
            self.redirect('/blog/%s' % str(pdis.key().id()))
            return
        elif self.user:
            self.redirect('/blog/%s' % str(pdis.key().id()))
            return
        else:
            self.redirect('/login')
            return


def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and USER_RE.match(username)

def valid_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return password and PASS_RE.match(password)

def valid_email(email):
    EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return not email or EMAIL_RE.match(email)

class Signup(Handler):
    """ handles New User signup submission """
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

        def done(self, *a, **kw):
            raise NotImplementedError


class Register(Signup):
    """ confirms Signup submission does not contain an existing username in the database """
    def done(self):
        #check that user doesn't exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists, please try a different Username'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            self.login(u)
            self.redirect('/blog/welcome')
            return


class Login(Handler):
    """ handles User Login submission """
    def get(self):
        #auto-logout a loggedin user if they wander to login page manually
        self.logout()
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog/welcome')
            return
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)


class Logout(Handler):
    """ handles user logout safely """
    def get(self):
        self.logout()
        self.redirect('/login')
        return


class Welcome(Handler):
    """ goes to the user welcom page """
    def get(self):
        #the following 'user' is from the initialize function above
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/signup')
            return

class MainPage(Handler):
    """ goes to the signup page """
    def get(self):
        self.redirect('/signup')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', Register),
    ('/login', Login),
    ('/logout', Logout),
    ('/blog/welcome', Welcome),
    ('/blog/?', BlogFront),
    ('/blog/([0-9]+)', PostPage),
    ('/blog/newpost', NewPost),
    ('/blog/editpost/([0-9]+)', EditPost),
    ('/blog/delete/([0-9]+)', DeletePost),
    ('/blog/like/([0-9]+)', LikePost),
    ('/blog/dis/([0-9]+)', DisPost),
    ('/blog/deletecomment/([0-9]+)', DeleteComment),
    ('/blog/editcomment/([0-9]+)', EditComment)
    ],debug=True)
