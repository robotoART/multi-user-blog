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

from utils.Utils import *


class EditPost(Handler):
    """
    goes to the Edit Post Form page and handles editing a post submissions
    """
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if post is not None:
            subject = post.subject
            content = post.content
            if self.user and self.user.name == post.username:
                self.render("editpost.html", subject=subject, content=content)
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
                    # REGION DEBUGGER used to wipe likes and dislikes
                    # p.liked_by = []
                    # p.disd_by = []
                    p.put()
                    self.redirect('/blog/%s' % str(p.key().id()))
                    return
                else:
                    error = "subject and content, please!"
                    self.render("editpost.html", subject=subject,
                                content=content, error=error)
            elif self.user:
                self.redirect('/blog/%s' % str(p.key().id()))
                return
            else:
                self.redirect('/login')
                return
        else:
            self.redirect('/blog')
            return
