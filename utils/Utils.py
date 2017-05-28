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

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

secret = '111-infinity0+infinity&beyond999'


def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)


# user functions
def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, pw, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, pw, salt)


def users_key(group='default'):
    return db.Key.from_path('users', group)


# blog stuff
def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class Utils(object):
    """ contains global functions commonly used """
    @classmethod
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    @classmethod
    def make_secure_val(self, nonsecure_val):
        return "%s|%s" % (nonsecure_val,
                          hmac.new(secret, nonsecure_val).hexdigest())

    @classmethod
    def check_secure_val(self, secure_val):
        val = secure_val.split('|')[0]
        if secure_val == Utils.make_secure_val(val):
            return val
