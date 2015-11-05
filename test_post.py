

import unittest

import post

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


