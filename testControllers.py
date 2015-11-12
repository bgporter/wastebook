
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
      self.userId = userId
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

   def testOldPosts(self):
      controllers.RightNow = lambda: datetime(2016, 1, 1)
      user1 = FakeUser("", False)
      c = controllers.PostController(user1)
      c.DateFilter("published", datetime(2016, 1, 1))
      c.SetPagination(0, 10)
      c.SetFilterAttribute("status", "published")
      cur = c.Search(db.posts)

      self.assertEqual(1, cur.count())
      self.assertEqual(False, c.moreResults) 


      user2 = FakeUser('bgporter', True)
      c = controllers.PostController(user2)
      c.DateFilter("published", datetime(2016, 1, 1))
      c.SetPagination(0, 10)
      c.SetFilterAttribute("status", "published")

      cur = c.Search(db.posts)
      self.assertEqual(2, cur.count())
      self.assertEqual(False, c.moreResults) 

   def testFuturePosts(self):
      # posts with a publication date in the future can't be gotten.
      user1 = FakeUser("", False)

      c = controllers.PostController(user1)
      c.DateFilter("published", datetime(2015, 1, 1))
      c.SetPagination(0, 10)
      c.SetFilterAttribute("status", "published")
      cur = c.Search(db.posts)

      self.assertEqual(0, cur.count())
      self.assertEqual(False, c.moreResults) 


      # ...even if we're the authenticated owner.
      user2 = FakeUser('bgporter', True)
      c = controllers.PostController(user2)
      c.DateFilter("published", datetime(2015, 1, 1))
      c.SetPagination(0, 10)
      c.SetFilterAttribute("status", "published")
      cur = c.Search(db.posts)

      self.assertEqual(0, cur.count())
      self.assertEqual(False, c.moreResults) 


class TestPagination(unittest.TestCase):
   @classmethod
   def setUpClass(cls):
      db.posts.drop()
      CreatePosts(POST_DATA_2)

   @classmethod
   def tearDownClass(cls):
      db.posts.drop()

   def testMore(self):
      user1 = FakeUser("", False)
      c = controllers.PostController(user1)      
      c.DateFilter("published", datetime(2016, 1, 1))
      c.SetPagination(0, 5)
      c.SetFilterAttribute("status", "published")
      cur = c.Search(db.posts)

      self.assertEqual(5, cur.count(True))
      self.assertEqual(True, c.moreResults) 

      c.SetPagination(1, 5)
      cur = c.Search(db.posts)

      self.assertEqual(5, cur.count(True))
      self.assertEqual(True, c.moreResults) 

      c.SetPagination(2, 5)
      cur = c.Search(db.posts)

      self.assertEqual(1, cur.count(True))
      self.assertEqual(False, c.moreResults) 
