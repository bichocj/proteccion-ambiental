from django.db.models import Q
from fullcalendar.models import Calendar

__author__ = 'jona'


def calendars_by_user(request):
    if not request.user.is_authenticated():
        return []
    calendar_query = Calendar.objects.filter(Q(assigned=request.user) | Q(users=request.user))
    return {'calendars_by_user': calendar_query}
