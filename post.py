
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

