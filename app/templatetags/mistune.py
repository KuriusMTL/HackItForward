import mistune
from django_jinja import library
from django.utils.safestring import mark_safe


@library.filter
def mistune_html_no_highlight(text):
    markdown = mistune.Markdown(
        plugins=["strikethrough", "footnotes", "table"],
    )
    return mark_safe(markdown(text))
