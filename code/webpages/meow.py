import os
import urllib

import webapp2

from html_constants import *

MEOW_PAGE_HTML= '''\
<html>
  <body>
    <center>
    <iframe width="840" height="600"
      src="http://www.youtube.com/embed/DXUAyRRkI6k?rel=0&autoplay=1 ">
    </iframe> 
    </center>
  </body>
</html>
'''

class MeowPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MEOW_PAGE_HTML)
        self.response.write(ALIGN_HTML.substitute(align="center"))
        self.response.write(FORM_HTML.substitute(action="/", method="link"))
        self.response.write(SUBMIT_HTML.substitute(value="Return to Main Page"))
        self.response.write("</form></div>")

