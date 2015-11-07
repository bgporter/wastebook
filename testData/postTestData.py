'''
   A secret file with data that we can use in unit tests without needing to 
   clutter up that file with a bunch of raw data structures. 
'''

from datetime import datetime


SEARCH_TEST_DATA = [
   {
      "created" :    datetime(2015, 10, 1),
      "published":   datetime(2015, 10, 1),
      "author":      "bgporter",
      "public":      True,
      "status":      "published",
      "title":       "First Post",
      "slug":        "",
      "text":        "a bunch of words",
      "tags":        [],
      "type":        "Post"
   },
   {
      "created" :    datetime(2015, 10, 2),
      "published":   datetime(2015, 10, 2),
      "author":      "bgporter",
      "public":      True,
      "title":       "Second Post",
      "status":      "published",
      "slug":        "",
      "text":        "a bunch more words",
      "tags":        [],
      "type":        "Post"

   }
   
   



]