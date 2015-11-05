
'''
   post.py -- code for the Wastebook implementation of Post and Page objects, 
   and assorted collateral things that make sense to be bundled here.
'''

TEMPLATE_POST = {
   "published":        None,    # datetime
   "modified":         None,    # datetime
   "author":           "",      # string
   "public":           True,    # bool
   "tags":             [],      # list of strings
   "title":            "",      # string
   "slug":             "",      # string, generated from the title
   "image":            "",      # string, name of an image file
   "draft":            "",      # string, draft text not yet published
   "text":             "",      # text as last published
   "summary":          "",      # string, short description of contents
   "viewCount":        0,       # int
   "status":           "draft", # string, one of 'draft', 'published', 'deleted'
   "renderedText":     "",      # string, HTML rendered version of text. 
   "rendered":         None,    # datetime when the renderedText was generated
   # optional fields, only present when we need to change the URL of an
   # already published post":
   "redirectUrl":      "",      # if present, where to redirect the user
   "redirectCode":     None     # if present, HTTP error code (probably 301)
   
}

import copy
import datetime
import re
import string
import unicodedata
import urllib

REPLACE_PUNCTUATION = re.compile(r"[{}]".format(string.punctuation))
CONDENSE_SPACE = re.compile(r"\s+")

def slugify(txt):
   ''' convert the input title text into a format that's usable in a URL:
      - all lowercase
      - any punctuation characters removed (well, replaced with a space)
      - multiple spaces condensed to single spaces
      - leading/trailing spaces stripped away.
      - spaces converted to dashes
      - unicode converted to UTF-8, any non-ASCII chars percent encoded
   '''
   slug = txt.lower()
   slug = REPLACE_PUNCTUATION.sub(u" ", slug)
   slug = CONDENSE_SPACE.sub(u" ", slug)
   slug = slug.strip()
   slug = re.sub(r"\s", '-', slug)
   # handle IRI issues...
   # first, normalize the string
   slug = unicodedata.normalize("NFC", slug)
   # convert to UTF-8
   slug = slug.encode("utf-8")
   # percent-encode any non-ASCII code points that remain.
   slug = urllib.quote(slug)

   return slug

class Post(object):
   def __init__(self, data=None):
      if data is None:
         data = {}
      # The post/page data is held in a separate dict, not the object's 
      # main __dict__   
      self._data = data

      # A dict mapping post elements with special-case methods
      # to update their value (e.g., making sure that titles and slugs
      # are always updated together)
      self._setExceptions = {}
      self.AddSetException('title', self.SetTitle)

   def AddSetException(self, key, handler):
      self._setExceptions[key] = handler

   def __getattr__(self, name):
      if not name.startswith("_"):
         return self._data[name]

   def __setattr__(self, name, value):
      if name.startswith("_"):
         self.__dict__[name] = value
      else:
         if name in self._setExceptions.keys():
            # call the special-case code:
            self._setExceptions[name](name, value)
         else:
            self._data[name] = value

   @classmethod
   def Create(cls):
      data = copy.deepcopy(TEMPLATE_POST)
      retval = cls(data)
      retval.type = retval.__class__.__name__
      retval.created = datetime.datetime.now()
      return retval


   def SetTitle(self, key, title):
      ''' update the title and also generate the slug for this post/page. '''
      # We don't want leading/trailing whitespace -- get rid of it
      title = title.strip()
      self._data[key] = title
      newSlug = slugify(title)
      if self.slug and newSlug != self.slug:
         # !!! handle the need for a new redirect object in the database to connect
         # the old slug/URL to the new location.
         pass
      self._data['slug'] = newSlug




class Page(Post):
   pass