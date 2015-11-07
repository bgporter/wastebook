
'''
   post.py -- code for the Wastebook implementation of Post and Page objects, 
   and assorted collateral things that make sense to be bundled here.
'''

TEMPLATE_POST = {
   ## Metadata
   "created":          None,    # datetime, only settable once.
   "published":        None,    # datetime
   "modified":         None,    # datetime
   "rendered":         None,    # datetime when the renderedText was generated
   "author":           "",      # string
   "public":           True,    # bool
   "viewCount":        0,       # int
   "slug":             "",      # string, generated from the title
   "status":           "draft", # string, one of 'draft', 'published', 'deleted'

   ## Content
   "title":            "",      # string
   "image":            "",      # string, name of an image file
   "summary":          "",      # string, short description of contents
   "draft":            "",      # string, draft text not yet published
   "text":             "",      # text as last published
   "renderedText":     "",      # string, HTML rendered version of text. 
   "tags":             [],      # list of strings
}

import copy
import datetime
import pymongo
import re
import string
import unicodedata
import urllib

from bson.objectid import ObjectId

REPLACE_PUNCTUATION = re.compile(r"[{}]".format(string.punctuation))
CONDENSE_SPACE = re.compile(r"\s+")


RightNow = datetime.datetime.now

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


def ExtractTags(txt):
   ''' given input text, look for #tag instances in it, and return a list 
      of those tags without the leading '#'. If there are no tags, we return
      an empty list.

      Before returning the list, we:
      - remove dupes
      - sort the tags alphabetically
   '''

   TAG_PATTERN = re.compile(r'(?:^|\s)#(\w+)', re.M)
   tagList = TAG_PATTERN.findall(txt)

   return sorted(list(set([t.lower() for t in tagList])))

class Post(object):
   def __init__(self, data=None):
      '''
         The Post object -- note that Pages and Posts are structurally identical
         (at least to start out with), and differ only in their type name, which is 
         also used to separate them in the database. 

         When we create a Post/Page, we initialize it with a dict that is either 
         a copy of the template post (above) or has been fetched from the database.

         We use a getattr/setattr hack here: actual member variables are always
         prefixed with an underscore, and the values that need to go into the 
         database are not underscore-prefixed. 

      '''
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
      self.AddSetException('created', self.SetCreated)
      self.AddSetException('text', self.SetText)

   def AddSetException(self, key, handler):
      ''' some attributes need extra logic applied to them before sticking them
         into the _data dict. If we weren't using the setattr hack that we are, 
         we could just use properties for this. Instead, we provide this hook into the
         guts of that hack and give ourself a way to insert that logic. (e.g., 
         the 'created' timestamp is write-once. We use a SetException to 
         enforce that.)
      '''
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
      retval.created = RightNow()
      return retval

   @classmethod
   def TypeName(cls):
      ''' return the name of the class that's being invoked here. '''
      # create a disposable object so we can get the typename
      o = cls({})
      return o.__class__.__name__

   @classmethod
   def Load(cls, postDb, slugOrId):
      '''
         Retrieve a single page or post from the database, using either its
         slug or objectId as the key. Returns a Post/Page object on success, 
         None if not found.
      '''
      theType = cls.TypeName()

      thePost = None
      # if we're being passed an object ID, it will be a 24-char long string
      # that is a hex value.
      if 24 == len(slugOrId):
         try:
            int(slugOrId, 16)
            # if we get here, we didn't throw an error. 
            thePost = postDb.find_one({"_id": ObjectId(slugOrId)})
         except ValueError:
            pass
      if thePost is None:
         searchDict = {
            "type" : theType,
            "slug":  slugOrId
         }
         thePost = postDb.find_one(searchDict)

      retval = None
      if thePost:
         retval = cls(thePost)

      return retval


   @classmethod
   def Search(cls, postDb, filter, skip=0, limit=0, sort=None):
      # create a disposable object so we can get the typename
      typeName = cls.TypeName()

      filter['type'] = typeName

      if sort is None:
         # by default, we sort in reverse order on date published.
         sort = [("published", pymongo.DESCENDING)]

      return postDb.find(filter, None, skip, limit, sort=sort)




   def Save(self, postDb):
      ''' store this post into the database. '''
      # if the slug has changed, we need to filter on the *old* slug, not
      # the new one that we'll be replacing!
      
      redirectDict = None
      if self._redirectFrom:
         searchSlug = self._redirectFrom
         redirectDict = {
            "type":     self.type,
            "slug":     self._redirectFrom,
            "location": self.slug,
            "created":  RightNow(),
            "code":     301,
         }

      else:
         searchSlug = self.slug

      filterDict = {
         "type":     self.type,
         "slug":     searchSlug,
         "created":  self.created
      }

      # no -- we're only modified if the text changes (or is that right?) We're
      # using modified to act as a flag that we need to re-render the HTML output.
      #self.modified = datetime.datetime.now()

      result = postDb.replace_one(filterDict, self._data, upsert=True)

      if redirectDict is not None:
         # create a new record so someone trying to access the old post/page
         result2 = postDb.insert_one(redirectDict)

      # if we just upserted a new entry, we'll return a string version of the 
      # new record's ID. If this already was in the database, we already know its
      # object id.
      return str(result.upserted_id)


   def SetTitle(self, key, title):
      ''' update the title and also generate the slug for this post/page. '''
      # We don't want leading/trailing whitespace -- get rid of it
      title = title.strip()
      self._data[key] = title
      newSlug = slugify(title)
      if self.slug and newSlug != self.slug:
         # !!! handle the need for a new redirect object in the database to connect
         # the old slug/URL to the new location.
         # When we save, we need to test for this _redirectFrom attribute and if it's 
         # present, create a new record in the database. 
         self._redirectFrom = self.slug
      self.slug = newSlug

   def SetCreated(self, key, timestamp):
      ''' The timestamp of creation can only be set once, when we actually
         do create the post object for the first time. We don't raise anything
         if someone tries to change our create date, we just ignore it. 
      '''
      if self._data['created'] is None:
         self._data['created'] = timestamp

   def SetText(self, key, newText):
      ''' update our text. If it's different than it was before, also set 
         the 'modified' timestamp as well.
      '''
      if self.text != newText:
         self._data['text'] = newText
         self.tags = ExtractTags(newText)
         self.modified = RightNow()






class Page(Post):
   pass