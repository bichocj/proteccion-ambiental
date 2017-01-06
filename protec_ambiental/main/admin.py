from django.contrib import admin
from .models import Calendar, Format, Report, Task, Accident, Meeting, HistoryFormats, Company

admin.site.register(Calendar)
admin.site.register(Format)
admin.site.register(Report)
admin.site.register(Task)
admin.site.register(Accident)
admin.site.register(Meeting)
admin.site.register(HistoryFormats)
admin.site.register(Company)
