import mistune
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="mistune", is_safe=True)
def mistune_html_no_highlight(text):
    markdown = mistune.create_markdown(
        plugins=["strikethrough", "footnotes", "table"],
    )
    return mark_safe(markdown(text))
