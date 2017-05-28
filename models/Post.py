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
from User import User


class Post(db.Model, Utils):
    """ this class creates a Post object related to a User in the database """
    user = db.ReferenceProperty(User, collection_name='user_posts')
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)
    username = db.StringProperty(required=True)
    liked_by = db.StringListProperty(required=True)
    disd_by = db.StringListProperty(required=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return Utils.render_str("post.html", p=self, plks=len(self.liked_by),
                                  pdss=len(self.disd_by))
