from django.core.management.base import BaseCommand, CommandError
from main.views import update_players, update_teams

class Command(BaseCommand):
    help = 'Updates the Player and Team databases as per fpl.py'

    def handle(self, *args, **options):
        # attempt to update the Players database
        self.stdout.write('Updating Players table...')
        try:
            update_players()
            self.stdout.write('Players table updated successfully!')
        except Exception as e:
            self.stdout.write('Something went wrong whilst updating the Players table.')
            self.stdout.write('Error message: {}'. format(e))
            self.stdout.write('Rolling back any database changes...')
            self.stdout.write('############\n')
        
        # attempt to update Team database
        self.stdout.write('Updating Teams table...')
        try:
            update_teams()
            self.stdout.write('Team table updated successfully!')
        except Exception as e:
            self.stdout.write('Something went wrong whilst updating the Team table.')
            self.stdout.write('Error message: {}'. format(e))
            self.stdout.write('Rolling back any database changes...')
            self.stdout.write('############\n')
