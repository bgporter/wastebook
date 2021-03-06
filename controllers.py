
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

   def __init__(self, user, db):
      self.filterDict = {}
      # after we run a query, this will be either True or False.
      self.moreResults = None
      self.skip = 0
      self.limit = config.POSTS_PER_PAGE
      self.sort = self.dataType.defaultSort

      self.dateAttribute = "published"
      self.beforeDate = datetime.datetime.now()
      self.afterDate = None

      # by default, we only look at things that have been  marked 
      # as published.
      self.status = "published"

      self.visibility = {}
      self.additionalFilters = {}

      self.SetUser(user)
      self.db = db


   def SetUser(self, user):
      visibility = {}
      if user.is_authenticated:
         self.visibility = { 
            "$or": [
                  {"public": True}, 
                  {"public": False, "author": user.userId}
               ]
            }
      else:
         self.visibility = {"public" : True}      

   def SetPagination(self, pageNum, perPage):
      self.skip = pageNum * perPage
      self.limit = perPage

   def SetFilterAttribute(self, attr, value):
      self.additionalFilters[attr] = value


   def SetSort(self, sortList):
      ''' the default sort is reverse chron by publication date. You can 
         replace that by passing in a list of tuples in the format 
         that PyMongo understands.
      '''
      self.sort = sortList

   def DateFilter(self, attribute, beforeDate, afterDate=None):
      self.dateAttribute = attribute
      self.beforeDate = beforeDate
      self.afterDate = afterDate

   def BuildFilter(self):
      filterDict = {}
      # what can this user see?
      if self.visibility:
         filterDict.update(self.visibility)

      # what dates-worth of stuff should they see?
      if self.beforeDate:
         dateDict = {"$lt" : self.beforeDate}
         if self.afterDate:
            dateDict['$gte'] = self.afterDate
         filterDict[self.dateAttribute] = dateDict      

      if self.status:
         filterDict['status'] = self.status

      # ...and don't forget to add any additional filter settings
      # that we've been given.
      filterDict.update(self.additionalFilters)
      return filterDict


   def Load(self, slugOrId):
      # Remember that loading posts needs to take visibilty into account:
      # 1. Public posts still need an appropriate publication state and date
      # 2. Private posts need to be restricted to the currently logged-in user.
      filterDict = self.BuildFilter()
      thePost = self.dataType.Load(self.db, slugOrId, filterDict)

      return thePost


   def Search(self):
      # build a filter Dict from our attributes.
      filterDict = self.BuildFilter()

      cur = self.dataType.Search(self.db, 
         filterDict, 
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


