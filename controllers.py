
'''
   controllers.py -- a Controller layer to sit between the web view/URL 
   handlers code and the lower level model objects in (e.g.) post.py.
'''

import config
import post

import datetime

# for testing, we can replace this with another function that gives 
# a datetime of our choice.
RightNow = datetime.datetime.now

def controlVisibility(theUser):
   '''
      Build part of a Mongo search filter that (depending on the value of 
      theUser) either requests things that are public OR gets public things as well
      as anything private to the logged-in user. 
   '''

   retval = {}
   if theUser.is_authenticated:
      retval = { 
         "$or": [
               {"public": True}, 
               {"public": False, "author": theUser.userId}
            ]
         }

   else:
      retval = {"public" : True}

   return retval


def getPublishedPosts(db, theUser, perPage, pageNum=0):
   ''' get a page worth of post objects, respecting the visibility of things
      that should be there for the current user.
   '''

   filterDict = controlVisibility(theUser)
   # only get posts that have been published.
   filterDict['status'] = "published"
   # and have a publication date that's less than right now.
   filterDict['published'] = {"$lte": RightNow()}

   posts = post.Post.Search(db, filterDict, pageNum*perPage, perPage)

   return posts

