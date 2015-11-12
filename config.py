
## Edit to fit local conditions

MONGO_IP = "zappa"
DEBUG = True
SECRET_KEY = '\xa7{T\xe8Y\x9cW\xa3t\xefm\xbc\xe6\xf3\x15\x89\x9dtl\xe3\xc0\t\x0e\x9a'

if DEBUG:
   DATABASE = "wastebook_dev"
else:
   DATABASE = "wastebook"

# collection names.    
POSTS = "posts"
USERS = "users"


# site-specific settings

POSTS_PER_PAGE = 10
PAGES_PER_PAGE = 10


