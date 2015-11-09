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

# model code
import post
import user

import config

app = Flask(__name__)


app.config.from_object('config')

# connect to the database
db = MongoClient(config.MONGO_IP)
posts = db[config.DATABASE][config.POSTS]

@app.route("/")
def index():
   ''' main index page showing posts. '''
   return "Yo."


if __name__ == "__main__":
   app.run()
