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


class DeleteComment(Handler):
    """ this class handles deleting a comment submission """
    def get(self, comment_id):
        key = db.Key.from_path('Comment', int(comment_id))
        cdelete = db.get(key)
        if not cdelete:
            self.error(404)
            return
        cpostid = cdelete.post.key().id()
        cudname = cdelete.comusername
        if cdelete is not None and cpostid is not None:
            if self.user and cudname == self.user.name:
                cdelete.delete()
                self.redirect('/blog/%s' % str(cpostid))
                return
            elif self.user:
                self.redirect('/blog/%s' % str(cpostid))
                return
            else:
                self.redirect('/login')
                return
        elif cdelete is not None and cpostid is None:
            self.redirect('/blog/%s' % str(cpostid))
            return
        else:
            self.redirect('/blog')
            return
