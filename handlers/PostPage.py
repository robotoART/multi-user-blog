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

from models.Comment import Comment
from models.Post import Post
from models.User import User


class PostPage(Handler):
    """ this class goes to a specific Post permalink page """
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        ppost = db.get(key)
        pauthor = ppost.username
        pliked_by = ppost.liked_by
        plikes_qty = len(pliked_by)
        pdisd_by = ppost.disd_by
        pdiss_qty = len(pdisd_by)
        plby = False
        pdby = False
        comments = sorted(ppost.post_comments,
                          key=lambda comments: comments.last_modified,
                          reverse=True)
        if not ppost:
            self.error(404)
            return
        if self.user:
            loggeduser = self.user.name
            if pliked_by.count(loggeduser) > 0:
                plby = True
            if pdisd_by.count(loggeduser) > 0:
                pdby = True
            self.render("permalink.html", ppost=ppost, plby=plby, pdby=pdby,
                        pls=plikes_qty, pid=post_id,
                        loggedinusername=loggeduser, pauthor=pauthor,
                        pkey=key, pds=pdiss_qty, plb=pliked_by,
                        pdb=pdisd_by, comments=comments)
        else:
            self.render("permalink.html", ppost=ppost, comments=comments)

    def post(self, post_id):
        if self.request.get('add_com'):
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            p = db.get(key)
            comcontent = self.request.get('comment')
            if not p:
                self.error(404)
                return
            if comcontent and self.user:
                c = Comment(comcontent=comcontent,
                            comusername=self.user.name, post=key)
                c.put()
                self.redirect('/blog/%s' % str(p.key().id()))
                return
            else:
                self.render("permalink.html", ppost=key, comments=comments)
        else:
            self.redirect('/blog/%s' % str(p.key().id()))
            return
