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


class LikePost(Handler):
    """ this class handles Liking a post submission """
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        plike = db.get(key)
        if not plike:
            self.error(404)
            return
        lpliked_by = plike.liked_by
        luser = plike.username
        if (self.user and luser != self.user.name and
                lpliked_by.count(self.user.name) == 0):
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
