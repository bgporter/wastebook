

from markdown import markdown

import renderer

class MarkdownRenderer(renderer.RenderBase):

   def RenderText(self):
      self.text = markdown(self.text)