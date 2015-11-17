

import re

import renderer



LINK_PATTERN = re.compile(r'(^|\s)(http(?:s)?://[^ \<]+\w)')


class LinkRenderer(renderer.RenderBase):
   '''
      Converts standalone http or https links in text into the Markdown
      equivalent, so 

      lorem ipsum http://www.example.com, etc

      becomes

      lorem ipsum [http://www.example.com](http://www.example.com), etc

   '''


   def RenderText(self):
      self.text = LINK_PATTERN.sub('\g<1>[\g<2>](\g<2>)', self.text)