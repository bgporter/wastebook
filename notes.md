# Wastebook Redux

## Database Tables

### Posts

- Publication date
- Modification date
- Author
- Public/private (bool? multi-value state?)
- Tags (list, extracted from text; anything that's _#tagname_)
- Title
- Slug (generated from title, used as friendly URL, not manually editable, must be unique per-user.)
- Image file (if present, packaged with post in e.g. RSS. A post can have any number of embedded image files...)
- Text (do we maintain a list for versioning?, If so, we also need a current version value.)
- Summary/synopsis (short tl;dr version that might be used e.g. in RSS/twitter when available)
- ViewCount
- Status (draft, published, deleted)
- Rendered (we cache a rendered version of the post for fast output)
- RedirectUrl
- RedirectCode (probably 301)

NOTE that because we go from title->slug->URL, if we publish a post and then change the title of it, we have two choices:
1. Accept the fact that the URL and title no longer agree
2. Create a new table entry with the old slug that only exists to store the new URL and redirect the user there with a permanent redirect.

I think that #2 sounds more like a solution that I like.

Another problem here is that this design requires that each post in the system have a unique title...or at least a unique slug. Perhaps that's as easy as 
1. Before each time saving a post for the first time (or when changing title and generating a new slug/URL), we look in the database for any posts that can be gotten to by the regex starting with that slug and ending with (optional) trailing dash and digits. 
2. If we find one or more posts that have the same slug-pattern, we create the next higher number and use that as the slug value.

How do we handle drafts? If we use a list of versions of text with a separate index pointing at the current live version, it's easy to have separate save draft and publish/update controls. 



### Pages

Hmm. The more I think about it, pages and posts are really the same thing, except:

1. They exist in different URL-spaces 
2. Posts are time-sequenced by default
3. Pages don't show in the RSS feed. 


Are Pages best implemented in the same table with posts, but using a type field to identify which we're looking at?


### Tasks
t/b/d


### Users

- username (for display)
- email
- salt
- pw hash

This isn't intended to be a big multi-user CMS so it doesn't seem that there's any reason to implement e.g. a role/permissions based system. If you've got a login to the system, you can create/edit posts/pages (and when tasks are implemented, you can view/edit your own tasks).




### Stats

Just a flat table that saves

- URL
- Referer
- Timestamp
- IP address?
- search string?


### Config 

## URLs

**/** (index) -- displays first page of posts

**/posts/<int:pageNum>** -- if no argument provided, identical to the index. Otherwise, attempts to display that page # of posts. Number of pages per post will need to be a configuration option.

**/post/<postId>** -- display just the specified post. `postId` should be either the slug value of the post or the database ID. 

**/edit/post/<postId>** (GET/POST) Edit a post. If this is a brand new post that hasn't been published, we need to use the database ID. 

**/tag/<tagName>** -- display pages/posts with the specified tag. If there is a page that's also named `tagName`, display its contents before the list of tagged things.

**/pages/<int:pageNum>** -- display a page-worth of links to pages. 


**/page/<pageId>** -- display just the specified page. `pageId` should be either the slug value of the page or the database ID. 


**/edit/page/<pageId>** (GET/POST) Edit a page.

**/blog/feed/<tag>** return the RSS feed of posts. If <tag> is present, filter on that (so we can e.g. tag a post #twitter and use that to push it )

**/upload** (GET/POST) form to upload images (etc.) We should have some sort of image resizing capability as part of the upload process.

**/recent** -- return a list of the last _n_ posts sorted by time. 
**/recent/<type>/<value>** -- return a list of the last _n_ posts sorted by time, specified by e.g., "/tag/foobar" or "/author/bgporter" 


**/preview/<pageOrPost>/<pageId>** -- if you're logged in, view the latest draft of the specified post (or page). The `pageOrPost` path fragment should be either the literal word 'page' or 'post', else 401.


### Someday

- accept scrobbled tracks?
- post by email?



## Plugins/Processors

Markdown does the bulk of the heavy lifting going from user input to rendered HTML output, but we need to do other kinds of rendering:

- converting links to youtube/tweets/etc into their embedded format
- converting standalone http:// links into clickable links. 
- converting #tag markup into links to a tag page. 
- creating the 'Continue reading...' link & truncating the rest of the page text.

