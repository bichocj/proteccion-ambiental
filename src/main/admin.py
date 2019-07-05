from django.contrib import admin

from .models import Format, Report, Task, Accident, Meeting, HistoryFormats, Company, Requirement, CountWorker


class FormatAdmin(admin.ModelAdmin):
    list_display = ('requirement', 'company','type_format')


admin.site.register(Requirement)
admin.site.register(Format, FormatAdmin)
admin.site.register(Report)
admin.site.register(Task)
admin.site.register(Accident)
admin.site.register(Meeting)
admin.site.register(HistoryFormats)
admin.site.register(Company)
admin.site.register(CountWorker)
