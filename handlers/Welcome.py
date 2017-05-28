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


class Welcome(Handler):
    """ goes to the user welcom page """
    def get(self):
        # the following 'user' is from the initialize function above
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')
            return
