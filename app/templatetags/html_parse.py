from django_jinja import library
from django.utils.safestring import mark_safe
from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

@library.filter
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return mark_safe(s.get_data())