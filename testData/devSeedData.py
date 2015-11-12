'''
   fake posts to bootstrap a development database. Put any interesting cases 
   useful for development in here. 
'''

from datetime import datetime


POST_DATA_1 = [
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
      "status":      "published",
      "title":       "Second Post",
      "slug":        "",
      "text":        "This is a #secret #post",
      "tags":        [],
      "type":        "Post"
   }


]