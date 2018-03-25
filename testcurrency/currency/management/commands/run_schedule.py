from django.core import management
from django.core.management.base import BaseCommand, CommandError
from threading import Thread
from currency import scheduler

class Command(BaseCommand):
    help = 'Run schedule and server'

    def handle(self, *args, **options):
        scheduler.job()
        scheduler.run_job()
        # t = Thread(target=scheduler.run_job)
        # t.start()
        # management.call_command('runserver')
