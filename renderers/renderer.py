
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


def PlaceholderUrlBuilder(endpoint, *pathComponents):
   pathComponents = list(pathComponents)
   pathComponents.insert(0, endpoint)
   return "/".join(pathComponents)

UrlBuilder = PlaceholderUrlBuilder


class RenderBase(object):
   '''
      Base class that defines the API used in the wastebook to perform multi-stage 
      rendering of marked-up text to HTML. The last step in the process is to run 
      the text through Markdown, so any renderers that come before that are free to 
      just generate markdown instead of HTML. 

      The only method that should be called directly from client code is the 
      `Render()` method, which accepts a block of text as a single string and 
      returns its results as a single string. 

      Derived renderer classes must at least provide implementations of the `RenderText()`
      method, which actually implements the text processing logic for that renderer. This 
      method operates on the member variable self.text, and should not return anything. 

      You may also provide implementations of the `PreRenderText()` and 
      `PostRenderText()` methods, which can do anything they need to do to prepare for and 
      clean up after the render step. For example, it might be useful in the `Pre` 
      handler to do something like `self.text = self.text.splitlines()`, perform your 
      render logic a line at a time, and then in the `Post` handler, have code that does
      `self.text = "\n".join(self.text)`

   '''
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

 

