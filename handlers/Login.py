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

from models.User import User


class Login(Handler):
    """ handles User Login submission """
    def get(self):
        # auto-logout a loggedin user if they wander to login page manually
        self.logout()
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog/welcome')
            return
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)
