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
def is_selectable(field):
    widget = field.field.widget
    class__ = widget.__class__
    return class__.__name__ == 'Select'


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


@register.filter
def get_by_key(list, keyword):
    try:
        # return list.get(key=key)

        list_filter = list.filter(key__istartswith=keyword)
        if list_filter.count() == 1:
            return list_filter.first()
        return list_filter
    except:
        pass
    return ''


@register.filter()
def clean(word, replace):
    return word.replace(replace, '')


@register.filter
def numerator(value):
    try:
        return value.numerator
    except:
        return ''


@register.filter
def denominator(value):
    try:
        return value.denominator
    except:
        return ''
