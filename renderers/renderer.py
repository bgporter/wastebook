
'''
   Base class that defines the API that any class that wants to get into
   our text rendering process needs to support. The base class implements
   the API as do-nothing versions of the API, so derived classes can omit 
   pre/post render steps if there's nothing to do there.
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

      