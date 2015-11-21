

import unittest

from tagRenderer import TagRenderer


class TestTagRenderer(unittest.TestCase):
   def setUp(self):
      pass

   def testSimpleTag(self):
      tr = TagRenderer("#tag")
      self.assertEqual(tr.Render(), '[#tag](tag/tag)')

   def testMultiple(self):
      tr = TagRenderer("Multiple #foo #bar")
      self.assertEqual(tr.Render(),
         'Multiple [#foo](tag/foo) [#bar](tag/bar)')