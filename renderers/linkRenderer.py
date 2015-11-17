

import re
import string

import renderer



STOP = re.escape(r" ,;:.!?")
LINK_PATTERN = re.compile(r'(^|\s)(http(?:s)?://[^ \<]+\w)')


class LinkRenderer(renderer.RenderBase):

   def RenderText(self):
      self.text = LINK_PATTERN.sub('\g<1>[\g<2>](\g<2>)', self.text)