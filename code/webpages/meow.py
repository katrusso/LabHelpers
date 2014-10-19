import os
import urllib

import webapp2

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
