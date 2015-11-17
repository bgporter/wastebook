

import unittest

from linkRenderer import LinkRenderer


class TestLinkRenderer(unittest.TestCase):
   def setUp(self):
      pass


   def testSimpleLink(self):
      lr = LinkRenderer("http://www.example.com")
      self.assertEqual(lr.Render(), "[http://www.example.com](http://www.example.com)")

   def testAfterSpace(self):
      lr = LinkRenderer("In a sentence: https://www.example.com and more words.")
      self.assertEqual(lr.Render(),
         "In a sentence: [https://www.example.com](https://www.example.com) and more words.")

   def testTrailingPunctuation(self):
      lr = LinkRenderer("In a sentence: https://www.example.com, and more.")
      self.assertEqual(lr.Render(),
         "In a sentence: [https://www.example.com](https://www.example.com), and more.")
      lr = LinkRenderer("End of a sentence: https://www.example.com.")
      self.assertEqual(lr.Render(),
         "End of a sentence: [https://www.example.com](https://www.example.com).")

   def testEndOfLine(self):
      lr = LinkRenderer("End of line: https://www.example.com")
      self.assertEqual(lr.Render(),
         "End of line: [https://www.example.com](https://www.example.com)")

   def testMultipleLinks(self):
      lr = LinkRenderer("1: http://foo.com and http://bar.com")
      self.assertEqual(lr.Render(),
         "1: [http://foo.com](http://foo.com) and [http://bar.com](http://bar.com)")

   def testAlreadyMarkdown(self):
      ''' links that are already inside of Markdown syntax should be left alone. '''
      lr = LinkRenderer("[http://foo.com](http://foo.com)")
      self.assertEqual(lr.Render(), "[http://foo.com](http://foo.com)")

   def testAlreadyHtml(self):
      ''' valid HTML links should be ignored. '''
      lr = LinkRenderer('<a href="http://foo.com">Link</a>')
      self.assertEqual(lr.Render(), '<a href="http://foo.com">Link</a>')

