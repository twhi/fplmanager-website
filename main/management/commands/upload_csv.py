import csv
from django.core.management import BaseCommand
from main.models import XgLookup

class Command(BaseCommand):
    help = 'Load a csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt') as f:
            csv_reader = csv.reader(f)
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    x = XgLookup(
                        player_id=row[0],
                        xg_name=row[1],
                        xg_team=row[2]
                    )
                    x.save()
                line_count += 1