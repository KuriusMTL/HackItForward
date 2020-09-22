from django_jinja import library


@library.filter
def get_class_name(model):
    return model.__class__.__name__
