

from markdown import markdown

import renderer

class MarkdownRenderer(renderer.RenderBase):
   '''
      Passes the text through Markdown. Should almost certainly be the
      last renderer in the pipeline that text gets sent through.
   '''

   def RenderText(self):
      self.text = markdown(self.text)