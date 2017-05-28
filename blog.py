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

from utils.Utils import Utils

from models.Comment import Comment
from models.Post import Post
from models.User import User

from handlers.BlogFront import BlogFront
from handlers.DeleteComment import DeleteComment
from handlers.DeletePost import DeletePost
from handlers.DisPost import DisPost
from handlers.EditComment import EditComment
from handlers.EditPost import EditPost
from handlers.LikePost import LikePost
from handlers.Login import Login
from handlers.Logout import Logout
from handlers.MainPage import MainPage
from handlers.NewPost import NewPost
from handlers.PostPage import PostPage
from handlers.Signup import *
from handlers.Welcome import Welcome


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
    ], debug=True)
