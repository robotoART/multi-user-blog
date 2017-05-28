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


class MainPage(Handler):
    """ goes to the signup page """
    def get(self):
        self.redirect('/signup')
