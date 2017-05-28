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


class DeletePost(Handler):
    """ this class handles deleting a post submission """
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        pdelete = db.get(key)
        if not pdelete:
            self.error(404)
            return
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
