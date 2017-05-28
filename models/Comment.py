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
from Post import Post
from User import User


class Comment(db.Model, Utils):
    """
     this class creates a Comment object related to a Post
     and a User in the database
    """
    post = db.ReferenceProperty(Post, collection_name='post_comments')
    comcontent = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    comusername = db.StringProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)

    def render(self):
        self._render_text = self.comcontent.replace('\n', '<br>')
        return Utils.render_str("comment.html", c=self)
