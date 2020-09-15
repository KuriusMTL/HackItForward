from django import template

register = template.Library()

@register.filter(name="class_name")
def get_class_name(model):
	return model.__class__.__name__
