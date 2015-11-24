
'''
   testControllers.py -- test suite to exercise our controller functions/classes.
'''

import unittest
from datetime import datetime
from datetime import timedelta


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


def CreatePosts(postDb, posts):
   for dct in posts:
      p = post.Post(dct)
      # make sure that slug, tags, etc. are set correctly.
      p.title = dct['title']
      p.text = ""
      p.text = dct['text']
      postId = p.Save(postDb)

class TestIndex(unittest.TestCase):
   @classmethod
   def setUpClass(cls):
      db.posts.drop()
      CreatePosts(db.posts, POST_DATA_1)

   @classmethod
   def tearDownClass(cls):
      db.posts.drop()

   def testOldPosts(self):
      controllers.RightNow = lambda: datetime(2016, 1, 1)
      user1 = FakeUser("", False)
      c = controllers.PostController(user1, db.posts)
      c.DateFilter("published", datetime(2016, 1, 1))
      cur = c.Search()

      self.assertEqual(1, cur.count())
      self.assertEqual(False, c.moreResults) 


      user2 = FakeUser('bgporter', True)
      c = controllers.PostController(user2, db.posts)
      c.DateFilter("published", datetime(2016, 1, 1))

      cur = c.Search()
      self.assertEqual(2, cur.count())
      self.assertEqual(False, c.moreResults) 

   def testFuturePosts(self):
      # posts with a publication date in the future can't be gotten.
      user1 = FakeUser("", False)

      c = controllers.PostController(user1, db.posts)
      c.DateFilter("published", datetime(2015, 1, 1))
      cur = c.Search()

      self.assertEqual(0, cur.count())
      self.assertEqual(False, c.moreResults) 


      # ...even if we're the authenticated owner.
      user2 = FakeUser('bgporter', True)
      c = controllers.PostController(user2, db.posts)
      c.DateFilter("published", datetime(2015, 1, 1))
      cur = c.Search()

      self.assertEqual(0, cur.count())
      self.assertEqual(False, c.moreResults) 

   def testSearchTags(self):
      user1 = FakeUser("", False)

      c = controllers.PostController(user1, db.posts)
      c.DateFilter("published", datetime(2016, 1, 1))
      c.SetFilterAttribute("tags", "foo")

      cur = c.Search()

      self.assertEqual(1, cur.count())      


class TestPagination(unittest.TestCase):
   @classmethod
   def setUpClass(cls):
      db.posts.drop()
      CreatePosts(db.posts, POST_DATA_2)

   @classmethod
   def tearDownClass(cls):
      db.posts.drop()

   def testMore(self):
      user1 = FakeUser("", False)
      c = controllers.PostController(user1, db.posts)      
      c.DateFilter("published", datetime(2016, 1, 1))
      c.SetPagination(0, 5)
      cur = c.Search()

      self.assertEqual(5, cur.count(True))
      self.assertEqual(True, c.moreResults) 

      c.SetPagination(1, 5)
      cur = c.Search()

      self.assertEqual(5, cur.count(True))
      self.assertEqual(True, c.moreResults) 

      c.SetPagination(2, 5)
      cur = c.Search()

      self.assertEqual(1, cur.count(True))
      self.assertEqual(False, c.moreResults) 

class TestDateRange(unittest.TestCase):
   @classmethod
   def setUpClass(cls):
      db.posts.drop()
      CreatePosts(db.posts, POST_DATA_2)

   @classmethod
   def tearDownClass(cls):
      db.posts.drop()


   def MonthSearch(self, year, month):
      user1 = FakeUser("", False)
      c = controllers.PostController(user1, db.posts)      
      start = datetime(year, month, 1)
      end = (start + timedelta(days=31)).replace(day=1)
      c.DateFilter("published", end, start)

      cur = c.Search()
      return cur.count()

   def test_MonthRange(self):
      self.assertEqual(1, self.MonthSearch(2015, 10))
      self.assertEqual(3, self.MonthSearch(2015, 6))
      self.assertEqual(2, self.MonthSearch(2015, 5))


class TestPostLoad(unittest.TestCase):
   ''' under normal cisrumstances, we should only be able to 
      load posts that:
      1. Have been published.
      2. We have permission to see (either public, or private and we 
         have rights to see it)
   '''
   @classmethod
   def setUpClass(cls):
      db.posts.drop()
      CreatePosts(db.posts, POST_DATA_1)

   @classmethod
   def tearDownClass(cls):
      db.posts.drop()


   def setUp(self):
      self.anonymous = FakeUser('', False)
      self.loggedIn = FakeUser('bgporter', True)

   def test_PostNotFound(self):
      c = controllers.PostController(self.anonymous, db.posts)
      thePost = c.Load('non-existent-post')
      self.assertIs(thePost, None)
      

   def test_PublicPublishedPost(self):
      '''
      ''' 
      c = controllers.PostController(self.anonymous, db.posts)
      thePost = c.Load('first-post')
      self.assertIsNot(thePost, None)

      c = controllers.PostController(self.loggedIn, db.posts) 
      thePost = c.Load('first-post')
      self.assertIsNot(thePost, None)

   def test_PublicUnpublishedPost(self):
      c = controllers.PostController(self.anonymous, db.posts)
      # published, but in the future
      c.DateFilter("published", datetime(2015, 1, 1))
      thePost = c.Load('first-post')
      self.assertIs(thePost, None)
      
      # date is okay, status is not
      c.DateFilter("published", datetime(2016, 1, 1))
      thePost = c.Load('fourth-post')
      self.assertIs(thePost, None)

      # even if I'm logged in, I shouldn't have a draft post 
      # show up on the main page.
      c = controllers.PostController(self.loggedIn, db.posts) 
      c.DateFilter("published", datetime(2016, 1, 1))
      thePost = c.Load('fourth-post')
      self.assertIs(thePost, None)

   def test_PrivatePublishedPost(self):
      c = controllers.PostController(self.anonymous, db.posts)
      c.DateFilter("published", datetime(2016, 1, 1))
      thePost = c.Load("second-post")
      self.assertIs(thePost, None)

      c = controllers.PostController(self.loggedIn, db.posts)
      c.DateFilter("published", datetime(2016, 1, 1))
      thePost = c.Load("second-post")
      self.assertIsNot(thePost, None)


   def test_PrivateUnpublishedPost(self):
      c = controllers.PostController(self.anonymous, db.posts)
      c.DateFilter("published", datetime(2015, 1, 1))
      thePost = c.Load("second-post")
      self.assertIs(thePost, None)

      c = controllers.PostController(self.loggedIn, db.posts)
      c.DateFilter("published", datetime(2015, 1, 1))
      thePost = c.Load("second-post")
      self.assertIs(thePost, None)



