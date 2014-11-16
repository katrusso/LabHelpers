from string import Template

OPEN_HTML=Template('''\
<!DOCTYPE html>
<html>
  <head>
    $head
  </head>
  <body>
''')

def write_css_html(page): 

    page.response.write(CSS_CLASS_HTML.substitute(id="header"))
    page.response.write('<h1> <img src="stylesheets/emc24.png" alt="E=mc^2 image" width="40px" height="25px"> Lab Helpers </h1>')
    page.response.write(CLOSE_CSS_HTML)#header
    
    page.response.write(CSS_CLASS_HTML.substitute(id="sub-heading"))
    page.response.write('Lab 17: Exam 2 Review <br><br><br>')
    page.response.write(CLOSE_CSS_HTML)#sub-heading

CSS_HTML=Template('''\
<div id=$id>
''')
CSS_CLASS_HTML = Template('''\
<div class=$id>
''')

LINK_HTML=Template('''\
<a href=$link> $text </a>
''')

FORM_HTML=Template('''\
<form action="$action" method="$method">
''')

ALIGN_HTML=Template('''\
<div align=$align>
''')

SUBMIT_HTML=Template('''\
<div><input type="submit" value="$value"></div>
''')

RADIO_HTML=Template('''\
<input type="radio" name="$name" $checked value="$value">$text<br>
''')

CHECKBOX_HTML=Template('''\
<input type="checkbox" name="$name" $checked value=$value>$text<br>
''')

TEXTBOX_HTML=Template('''\
<div><textarea name="$name" rows="$row" cols="$col">$text</textarea></div>
''')

TAB_HTML = '''\
&nbsp &nbsp &nbsp &nbsp &nbsp
'''

OPEN_TABLE_HTML = Template('''\
<table style="width:$percent%">
''')

TABLE_COLUMN_HTML = Template('''\
<td> <div align="center">$text </div></td>
''')

CLOSE_ALIGN_HTML = '''\
</div>
'''

CLOSE_TABLE_HTML = '''\
</table>
'''

CLOSE_FORM_HTML = '''\
</form>
'''

CLOSE_CSS_HTML = '''\
</div>
'''

CLOSE_HTML='''\
  </body>
</html>
'''

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

