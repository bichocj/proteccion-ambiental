from django import template


register = template.Library()


@register.filter
def is_checkbox(field):
    widget = field.field.widget
    class__ = widget.__class__
    return class__.__name__ == 'CheckboxInput'


@register.filter
def is_hidden(field):
    widget = field.field.widget
    class__ = widget.__class__
    return class__.__name__ == 'HiddenInput'


@register.filter
def is_password(field):
    widget = field.field.widget
    class__ = widget.__class__
    return class__.__name__ == 'PasswordInput'


@register.filter
def is_file_input(field):
    widget = field.field.widget
    class__ = widget.__class__
    return class__.__name__ == 'ClearableFileInput'


