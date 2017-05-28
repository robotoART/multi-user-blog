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

from Handler import Handler

from models.Post import Post

from utils.Utils import *


class NewPost(Handler):
    """ goes to the New Post Form page and handles new post submissions """
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
                p = Post(parent=blog_key(), subject=subject, content=content,
                         username=self.user.name)
                p.put()
                self.redirect('/blog/%s' % str(p.key().id()))
                return
            else:
                error = "subject and content, please!"
                self.render("newpost.html", subject=subject, content=content,
                            error=error)
        else:
            self.redirect('/login')
            return
