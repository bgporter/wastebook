#! /usr/bin/env python

'''
   wastebook.py -- Flask/MongoDb blogging/publishing engine. 
   Fall 2015, Bg Porter

   The MIT License (MIT)

   Copyright (c) 2015 Brett g Porter

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.

'''

from flask import abort
from flask import Flask 
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import send_file
from flask import url_for

from pymongo import MongoClient

import flask_login
from flask_login import login_required
from flask_login import current_user


import datetime

# model code
import post
from post import Post
import user
import controllers

import config

app = Flask(__name__)


app.config.from_object('config')

# connect to the database
db = MongoClient(config.MONGO_IP)
postDb = db[config.DATABASE][config.POSTS]

# get flask-login set up.
loginManager = flask_login.LoginManager()
loginManager.login_view = "login"
loginManager.init_app(app)



RightNow = datetime.datetime.now



def FixUrl(text):

   def DoFix(matchObj):
      fields = matchObj.group(0)
      fields = [f.strip() for f in fields.split(',')]
      linkText = fields[0]
      endPoint = fields[1]
      path = fields[2:]

      return '<a href="{0}">{1}</a>'.format(url_for(endPoint, *path), linkText)

   return FIX_PATTERN.sub(DoFix, text)



@loginManager.user_loader
def loadUser(userId):
   return user.loadUser(db, userId)


@app.route("/")
def index():
   ''' main index page showing posts. '''
   return posts(1)

### Let's do all of the 'posts' things first. 

@app.route("/posts/<int:pageNum>/")
def posts(pageNum=1):
   # note that page num can't be less than 1. 
   pageNum = max(1, pageNum)
   c = controllers.PostController(current_user, postDb)
   c.DateFilter("published", RightNow())
   c.SetPagination(pageNum-1, config.POSTS_PER_PAGE)
   c.SetFilterAttribute("status", "published")

   cursor = c.Search()

   return "\n".join(str(p) for p in cursor)

@app.route("/post/<idOrSlug>")
def post(idOrSlug):
   thePost = Post.Load(postDb, idOrSlug)
   if thePost:
      return thePost
   else: 
      abort(404)


if __name__ == "__main__":
   app.run()
