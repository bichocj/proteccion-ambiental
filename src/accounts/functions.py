from django.contrib.auth.models import User, Group

from proteccion_ambiental import settings

__author__ = 'bicho'


def generate_username(base, correlative=''):
    if ' ' in base:
        base = base[:base.index(' ')]
    username = base + str(correlative)
    try:
        User.objects.get(username=username)
        if correlative == '':
            correlative = 0
        correlative = int(correlative)
        correlative += 1
        return generate_username(username, str(correlative))
    except User.DoesNotExist:
        return username


def get_member_group():
    try:
        return Group.objects.get(name=settings.MEMBER_GROUP)
    except Group.DoesNotExist:
        group = Group(name=settings.MEMBER_GROUP)
        group.save()
        return group


def get_users_of_member_group():
    return get_member_group().user_set.all().order_by('first_name')
