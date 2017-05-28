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

from utils.Utils import *
from models.User import User


class Handler(webapp2.RequestHandler, Utils):
    """ webapp2.RequestHandler """
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        usable_string = Utils.render_str(template, **params)
        return usable_string

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = Utils.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie',
                                         '%s=%s; Path=/blog' % (name,
                                                                cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies. get(name)
        return cookie_val and Utils.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/blog')

    # 'initialize' function checks if user is loggedin to allow making posts
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
