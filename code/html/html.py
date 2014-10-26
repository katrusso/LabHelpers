from string import Template

OPEN_HTML=Template('''\
<html>
  $head
  <body>
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
<input type="radio" name="$name" value="$value">$text<br>
''')

CHECKBOX_HTML=Template('''\
<input type="checkbox" name="$name" value="$value">$text<br>
''')

TEXTBOX_HTML=Template('''\
<div><textarea name="$name" rows="$row" cols="$col" value="$text"></textarea></div>
''')

TAB_HTML = '''\
&nbsp &nbsp &nbsp &nbsp &nbsp
'''

CLOSE_HTML='''\
  </body>
</html>
'''