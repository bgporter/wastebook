
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



class PostController(object):
   dataType = post.Post

   def __init__(self, user):
      self.filterDict = {}
      # after we run a query, this will be either True or False.
      self.moreResults = None
      self.skip = 0
      self.limit = 0
      self.sort = None


      self.SetUser(user)


   def SetUser(self, user):
      visibility = {}
      if user.is_authenticated:
         visibility = { 
            "$or": [
                  {"public": True}, 
                  {"public": False, "author": user.userId}
               ]
            }
      else:
         visibility = {"public" : True}      

      self.filterDict.update(visibility)

   def SetPagination(self, pageNum, perPage):
      self.skip = pageNum * perPage
      self.limit = perPage

   def SetFilterAttribute(self, attr, value):
      self.filterDict[attr] = value


   def SetSort(self, sortDict):
      ''' the default sort is reverse chron by publication date. You can 
         replace that by passing in a dict in the format that PyMongo understands.
      '''
      self.sort = sortDict

   def DateFilter(self, attribute, beforeDate, afterDate=None):
      dateDict = {"$lt" : beforeDate}
      if afterDate:
         dateDict['$gte'] = afterDate
      self.filterDict[attribute] = dateDict

   def Search(self, db):
      cur = self.dataType.Search(db, 
         self.filterDict, 
         self.skip, 
         self.limit, 
         self.sort)

      allMatches = cur.count()
      thisPageMatches = cur.count(True)

      self.moreResults = False
      if allMatches > (self.skip + thisPageMatches):
         self.moreResults = True

      return cur



class PageController(PostController):
   dataType = post.Page

   pass


