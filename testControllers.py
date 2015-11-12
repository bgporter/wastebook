
'''
   testControllers.py -- test suite to exercise our controller functions/classes.
'''

import unittest
from datetime import datetime


import config
import controllers
import post

from testData.devSeedData import *

from pymongo import MongoClient


class FakeUser(object):
   def __init__(self, userId, is_authenticated):
      self.userID = userId
      self.is_authenticated = is_authenticated


db = None

def setUpModule():
   global db
   client = MongoClient(config.MONGO_IP)
   db = client['wastebook_test']

def testDownModule():
   db.posts.drop()


def CreatePosts(posts):
   for dct in posts:
      p = post.Post(dct)
      # make sure that slug, tags, etc. are set correctly.
      p.title = dct['title']
      p.text = ""
      p.text = dct['text']
      postId = p.Save(db.posts)

class TestIndex(unittest.TestCase):
   @classmethod
   def setUpClass(cls):
      db.posts.drop()
      CreatePosts(POST_DATA_1)

   @classmethod
   def tearDownClass(cls):
      db.posts.drop()

   def test_OldPosts(self):

      controllers.RightNow = lambda: datetime(2016, 1, 1)
      user1 = FakeUser("", False)
      cur = controllers.getPosts(db.posts, user1, 10)
      self.assertEqual(1, cur.count())

      user2 = FakeUser('bgporter', True)
      cur = controllers.getPosts(db.posts, user1, 10)
      self.assertEqual(1, cur.count())

