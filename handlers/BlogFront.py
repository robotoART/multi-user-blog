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


class BlogFront(Handler):
    """ this class goes to the front page with the latest 10 Posts """
    def get(self):
        query_select = "select * from Post order by created desc limit 10"
        posts = db.GqlQuery(query_select)
        if self.user:
            self.render('front.html', posts=posts,
                        loggedinusername=self.user.name)
        else:
            self.render('front.html', posts=posts)
