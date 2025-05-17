from time import sleep

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        isUp = False
        while isUp == False:
            try:
                self.check(databases=["default"])
                isUp = True
            except (Psycopg2Error, OperationalError):
                self.stderr.write("Database unavailable, writing 1 second ...")
                sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
