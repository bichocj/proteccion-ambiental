from django.contrib import admin
from .models import Calendar, Format, Report, Task, Accident, Meeting, HistoryFormats, Company, Requirement, Employee


class FormatAdmin(admin.ModelAdmin):
    list_display = ('requirement', 'company')


admin.site.register(Employee)
admin.site.register(Calendar)
admin.site.register(Requirement)
admin.site.register(Format, FormatAdmin)
admin.site.register(Report)
admin.site.register(Task)
admin.site.register(Accident)
admin.site.register(Meeting)
admin.site.register(HistoryFormats)
admin.site.register(Company)
