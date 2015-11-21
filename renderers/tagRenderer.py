

import re

import renderer

# stolen from Post::ExtractTags, should DRY-ify this.
TAG_PATTERN = re.compile(r'(^|\s)#([a-zA-Z0-9][a-zA-Z0-9_-]*[a-zA-Z0-9])')

class TagRenderer(renderer.RenderBase):
   ''' Finds instances of #tag markup in the source and converts into 

      [#tag](http://link.to.tag)

      Uses the UrlBuilder function handler as set in the renderer module. If that's 
      not set, it will use a default function that's used in testing.

   '''

   def RenderText(self):
      #self.text = TAG_PATTERN.sub("\g<1>FIX_URL(#\g<2>, tag, \g<2>)", self.text)
      def MakeTagLink(matchObj):
         prefix = matchObj.group(1)
         tag = matchObj.group(2)
         url = renderer.UrlBuilder('tag', tag)
         return '{0}[#{1}]({2})'.format(prefix, tag, url)

      self.text = TAG_PATTERN.sub(MakeTagLink, self.text)