
'''
   Base class that defines the API that any class that wants to get into
   our text rendering process needs to support. The base class implements
   the API as do-nothing versions of the API, so derived classes can omit 
   pre/post render steps if there's nothing to do there.


   If a class needs to create URLs that are relative to the site that will be 
   serving this text, we don't have enough information here in this code to 
   know what those paths will look like, etc. To keep things loosely coupled, 
   those cases will be handled by having the renderer instead put a placeholder
   in the text that can eventually be processed at a higher level where the 
   knowledge of paths, etc (e.g., using Flask's url_for() function) does 
   exist, and the correct link text can be inserted. 

   Renderers that need to do this should insert
   FIX_URL(link_text, link_endpoint, p1 [, p2, p3...])

   Whereever they need to make use of this, and trust that higher-level
   code will do the final piece of processing that's needed. 

   See tagRenderer.py for an example.
'''


class RenderBase(object):
   def __init__(self, text):
      self.text = text

   def Render(self):
      self.PreRenderText()
      self.RenderText()
      self.PostRenderText()

      return self.text

   def PreRenderText(self):
      pass

   def RenderText(self):
      pass

   def PostRenderText(self):
      pass

      