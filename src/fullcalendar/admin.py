from django.contrib import admin

# Register your models here.
from fullcalendar.models import Events, Calendar

admin.site.register(Events)
admin.site.register(Calendar)
