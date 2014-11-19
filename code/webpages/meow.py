import os
import urllib

import webapp2

from html_constants import *


class MeowPage(webapp2.RequestHandler):     #EMBEDS YOUTUBE VIDEO
    def get(self):
        self.response.write(MEOW_PAGE_HTML)
        self.response.write(ALIGN_HTML.substitute(align="center"))
        self.response.write(LINK_HTML.substitute(link="/", 
                                                 text="Return to Main Page"))
        self.response.write("</div>")

