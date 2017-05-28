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


class EditComment(Handler):
    """
     handles editing a comment submission
    """
    def post(self, comment_id):
        edit_com_txtarea_name = 'comedit' + comment_id
        ctextupdate = self.request.get(edit_com_txtarea_name)
        key = db.Key.from_path('Comment', int(comment_id))
        cedit = db.get(key)
        if not cedit:
            self.error(404)
            return
        cpostid = cedit.post.key().id()
        cuename = cedit.comusername
        if cedit is not None:
            if self.user and cuename == self.user.name:
                cedit.comcontent = ctextupdate
                cedit.put()
                self.redirect('/blog/%s' % str(cpostid))
                return
            elif self.user:
                self.redirect('/blog/%s' % str(cpostid))
                return
            else:
                self.redirect('/login')
                return
        else:
            self.redirect('/blog/%s' % str(cpostid))
            return
