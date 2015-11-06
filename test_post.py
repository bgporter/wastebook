

import unittest

import post

from pymongo import MongoClient


db = None

def setUpModule():
   global db
   client = MongoClient("zappa")
   db = client['wastebook_test']

def testDownModule():
   db.posts.drop()



class TestSlugify(unittest.TestCase):
   def setUp(self):
      pass

   def test_simple(self):
      ''' make sure we go lowercase and handle leading/trailing 
         whitespace correctly.
      '''
      self.assertEqual("simple", post.slugify(u"Simple"))
      self.assertEqual("simple", post.slugify(" Simple"))
      self.assertEqual("simple", post.slugify("Simple "))
      self.assertEqual("simple", post.slugify(" Simple "))

   def test_dashes(self):
      ''' spaces replaced with a single dash? '''
      self.assertEqual("simple-test", post.slugify("SIMPLE TEST"))
      self.assertEqual("simple-test", post.slugify("SIMPLE   TEST"))

   def test_punctuation(self):
      ''' punctuation removed, replaced with a single dash like space? '''
      self.assertEqual("remove-the-punctuation", 
         post.slugify("Remove, the? !punctuation..."))
      self.assertEqual("this-that-and-something-else", 
         post.slugify(" This, that, and something else? "))

   def test_unicode(self):
      ''' Unicode converted to acceptable IRI format? '''
      self.assertEqual("m%C3%BCller", post.slugify(u"M\u00fcller"))



class TestTags(unittest.TestCase):
   def setUp(self):
      pass

   def test_tagExtraction(self):
      tags = post.ExtractTags("First test")
      self.assertEqual(tags, [])
      tags = post.ExtractTags("#initial tag")
      self.assertEqual(tags, ['initial'])
      tags = post.ExtractTags("#")
      self.assertEqual(tags, [])

      tags = post.ExtractTags("Should be a #thing")
      self.assertEqual(tags, ['thing'])
      tags = post.ExtractTags("Should be a no#thing")
      self.assertEqual(tags, [])



class TestPostBasic(unittest.TestCase):
   def setUp(self):
      pass


   def test_creation(self):
      ''' make sure that we can create post and pages and that they know what
         their type really is.
      '''
      p = post.Post.Create()
      self.assertEqual(p.type, "Post")
      self.assertEqual(p.public, True)

      p = post.Page.Create()
      self.assertEqual(p.type, "Page")

   def test_setTitle(self):
      ''' verify that we can set the title and set the slug at the same time.'''
      p = post.Post.Create()
      p.title = "This is a Title Test"
      self.assertEqual(p.title, "This is a Title Test")
      self.assertEqual(p.slug, 'this-is-a-title-test')

      p = post.Post.Create()
      p.title = " THIS SHOULD BE STRIPPED  "
      self.assertEqual(p.title, 'THIS SHOULD BE STRIPPED')
      self.assertEqual(p.slug, 'this-should-be-stripped')

      # !!! need to test that when we change the slug that we create a 
      # record in the database that lets redirection work correctly. !!!
      
      # a case where we have a new title that doesn't need a redirection. 
      p.title = 'this should be stripped' 
      self.assertEqual(p.title, 'this should be stripped')
      self.assertEqual(p.slug, 'this-should-be-stripped')
      self.assertEqual(p._redirectFrom, None)

      
      p.title = "This should be strapped"
      self.assertEqual(p.slug, 'this-should-be-strapped')
      self.assertEqual(p._redirectFrom, "this-should-be-stripped")

      page = post.Page.Create()
      page.title = "My First Page?"
      self.assertEqual("my-first-page", page.slug)
      
class TestPostDatabase(unittest.TestCase):
   def setUp(self):
      pass

   def test_savePost(self):
      p = post.Post.Create()
      p.title = "Initial Save Test"
      p.author = "bgporter"
      p.summary = "a test"
      p.text = "This should be longer."
      p.Save(db.posts)

      r = db.posts.find_one({"slug": "initial-save-test", "type": "Post"})
      p2 = post.Post(r)
      self.assertEqual(p.title, p2.title)
      self.assertEqual(p.author, p2.author)
      self.assertEqual(p.summary, p2.summary)
      self.assertEqual(p.text, p2.text)

   def test_saveAndLoadPost(self):
      p = post.Page.Create()
      p.title = "Can We Reload This?"
      p.author = "David Foster Wallace"
      p.text = "No individual moment by itself"

      postId = p.Save(db.posts)

      p2 = post.Page.Load(db.posts, 'can-we-reload-this')
      self.assertEqual(p.title, p2.title)
      self.assertEqual(p.author, p2.author)
      self.assertEqual(p.text, p2.text)

      p3 = post.Page.Load(db.posts, postId)
      self.assertEqual(p.title, p3.title)
      self.assertEqual(p.author, p3.author)
      self.assertEqual(p.text, p3.text)

      p2 = post.Post.Load(db.posts, 'can-we-reload-this')
      self.assertEqual(p2, None)


   def test_titleChangeRedirect(self):
      p = post.Post.Create()
      p.title = "Original Title"
      p.text = "This is the text of the post."

      postId = p.Save(db.posts)

      p.title = "A Second Title"
      postId2 = p.Save(db.posts)

      #self.assertEqual(postId, postId2)

      p3 = post.Post.Load(db.posts, "original-title")
      self.assertEqual(301, p3.code)
      self.assertEqual(p3.location, 'a-second-title')

      p4 = post.Post.Load(db.posts, p3.location)
      self.assertEqual(p4.title, p.title)
      self.assertEqual(p4.text, p.text)

   def test_ExtractAndSaveTags(self):
      p = post.Post.Create()
      p.title = "This Has Tags"
      p.text = "Here is some text with #tags #inside"

      postId = p.Save(db.posts)

      p2 = post.Post.Load(db.posts, 'this-has-tags')
      self.assertEqual(p2.tags, ['inside', 'tags'])


