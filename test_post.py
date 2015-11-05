

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
      




