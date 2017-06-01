import datetime

from django.core.management.base import BaseCommand, CommandError

from main.models import Format, HistoryFormats


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        formats = Format.objects.all()
        for format in formats:
            try:
                history = HistoryFormats.objects.filter(format=format)
                if history.count() <= 0:
                    history = HistoryFormats()
                    history.format = format
                    history.file = format.file
                    history.date_time = datetime.now()
                    history.save()
            except HistoryFormats.DoesNotExist:
                history = HistoryFormats()
                history.format = format
                history.file = format.file
                history.date_time = datetime.now()
                history.save()
