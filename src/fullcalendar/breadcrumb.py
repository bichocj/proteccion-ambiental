from django.utils.translation import ugettext as _

__author__ = 'jona'

links = {
    'calendar': {
        'name': _('Calendar'),
        'route': None,
        'parent': None,
        'params': False
    },
    'view_calendar': {
        'name': None,
        'route': 'calendar:view_calendar',
        'parent': 'calendar',
        'params': True
    },
    'new_calendar': {
        'name': _('New Calendar'),
        'route': 'calendar:new_calendar',
        'parent': 'calendar',
        'params': False
    },
    'settings_calendar': {
        'name': _('Settings'),
        'route': 'calendar:settings_calendar',
        'parent': 'view_calendar',
        'params': True
    }
}