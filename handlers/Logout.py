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


class Logout(Handler):
    """ handles user logout safely """
    def get(self):
        self.logout()
        self.redirect('/login')
        return
