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
      "text":        "a bunch of words #foo #bar",
      "tags":        [],
      "type":        "Post"
   },
   {
      "created" :    datetime(2015, 10, 2),
      "published":   datetime(2015, 10, 2),
      "author":      "bgporter",
      "public":      False,
      "title":       "Second Post",
      "status":      "published",
      "slug":        "",
      "text":        "a bunch more words #foo #baz",
      "tags":        [],
      "type":        "Post"
   },
   {
      "created" :    datetime(2015, 10, 3),
      "published":   datetime(2015, 10, 3),
      "author":      "tslothrop",
      "public":      True,
      "title":       "Third Post",
      "status":      "published",
      "slug":        "",
      "text":        "a bunch #baz more #bar words",
      "tags":        [],
      "type":        "Post"
   }   

]