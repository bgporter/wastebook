

import unittest

import post

class TestSlugify(unittest.TestCase):
   def setUp(self):
      pass

   def test_simple(self):
      self.assertEqual("simple", post.slugify(u"Simple"))
      self.assertEqual("simple", post.slugify(" Simple"))
      self.assertEqual("simple", post.slugify("Simple "))
      self.assertEqual("simple", post.slugify(" Simple "))

   def test_dashes(self):
      self.assertEqual("simple-test", post.slugify("SIMPLE TEST"))
      self.assertEqual("simple-test", post.slugify("SIMPLE   TEST"))

   def test_punctuation(self):
      self.assertEqual("remove-the-punctuation", 
         post.slugify("Remove, the? !punctuation..."))
      self.assertEqual("this-that-and-something-else", 
         post.slugify(" This, that, and something else? "))

   def test_unicode(self):
      self.assertEqual("m%C3%BCller", post.slugify(u"M\u00fcller"))