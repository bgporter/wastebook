

from renderer import RenderBase

# import all of the render filters that we want to invoke, and make 
# sure that they are listed in a sensible sequence in the PIPELINE 
# list.
from markdownRenderer import MarkdownRenderer
from tagRenderer import TagRenderer


PIPELINE = [
   #RenderBase,
   TagRenderer,


   # Keep Markdown as the final render filter, since all of the preceding
   # renderers have the option of converting their input to Markdown for 
   # additional handling.
   MarkdownRenderer
]


def RenderText(txt):
   for renderClass in PIPELINE:
      r = renderClass(txt)
      txt = r.Render()

   return txt