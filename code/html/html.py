from string import Template

OPEN_HTML=Template('''\
<html>
  $head
  <body>
''')

FORM_HTML=Template('''\
<form action="$action" method="$method">
''')

SUBMIT_BUTTON_HTML=Template('''\
<div><input type="submit" value="$value"></div>
''')

RADIO_BUTTON_HTML=Template('''\
<input type="radio" name="$name" value="$value">$text<br>
''')

CHECKBOX_HTML=Template('''\
<input type="checkbox" name="$name" value="$value">$text<br>
''')

TEXTBOX_HTML=Template('''\
<div><textarea name="$name" rows="$row" cols="$col" value="$text"></textarea></div>
''')

CLOSE_HTML='''\
  </body>
</html>
'''
