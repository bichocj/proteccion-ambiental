from django.contrib.auth.models import Group, User
from django.db import models
from django.template import defaultfilters
from django.utils.translation import ugettext as _


class Calendar(models.Model):
    title = models.CharField(_('title'), max_length=200, null=False, blank=None)
    slug = models.SlugField(max_length=100)
    assigned = models.ForeignKey(User, null=True, verbose_name=_('assigned to'))
    users = models.ManyToManyField(User, related_name="users", verbose_name=_('shared with'))
    min_time = models.TimeField(_('min time'), null=True, blank=True)
    max_time = models.TimeField(_('max time'), null=True, blank=True)
    created_by = models.ForeignKey(User, related_name="created_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Calendar')
        verbose_name_plural = _('Calendars')
        permissions = (
            ("view_calendars", "Can see existing calendars"),
        )

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(self.title)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exists = Calendar.objects.get(slug=slug)
                    if slug_exists:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Calendar.DoesNotExist:
                    self.slug = slug
                    break
        super(Calendar, self).save(*args, **kwargs)


class Accessibility(models.Model):
    calendar = models.ForeignKey(Calendar)
    group = models.ForeignKey(Group)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Events(models.Model):
    calendar = models.ForeignKey(Calendar)
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    observation = models.TextField(blank=True, null=True)
    member = models.ForeignKey(User)
    is_cancelled = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, related_name="created_by_event")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
