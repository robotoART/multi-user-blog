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


class DisPost(Handler):
    """ this class handles Disliking a post submission """
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        pdis = db.get(key)
        if not pdis:
            self.error(404)
            return
        lpdisd_by = pdis.disd_by
        luser = pdis.username
        if (self.user and luser != self.user.name and
                lpdisd_by.count(self.user.name) == 0):
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
