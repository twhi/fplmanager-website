import requests
import json
import unidecode
from .models import Player, Team


class PlayerTable:
    PLAYER_TABLE_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'

    def __init__(self):
        self.session = requests.Session()

        self.teams = Team.objects.all()

        self.table = self.get_player_table()
        self.process_table()

    def get_player_table(self):
        master_table_s = self.session.get(self.PLAYER_TABLE_URL).text
        master_table = json.loads(master_table_s)
        return master_table['elements']

    def process_table(self):

        # lookup player position i.e. G, D, M or F
        self.add_player_positions()

        # get team name from team_id
        self.add_team_name()

        # correct pricing on players. For example - where £5.0 is 50
        self.correct_pricing_values()

        # this was a temporary fix for an issue with a player have None on ep_next and ep_this
        # might need to be developed into something more permanent
        self.remove_nonetype()

        # removes diacritical characters from players names to aid searching
        self.add_raw_name()

    def add_raw_name(self):
        for p in self.table:
            p['name_raw'] = unidecode.unidecode(p['web_name'])
    
    def remove_nonetype(self):
        for p in self.table:
            if not p['ep_next']:
                p['ep_next'] = 0
            if not p['ep_this']:
                p['ep_this'] = 0

    def add_team_name(self):
        if self.teams:
            for p in self.table:
                p['team_name'] = next((t.team_name for t in self.teams if str(p['team']) == t.team_id), None)
                p['team_name_short'] = next((t.team_name_short for t in self.teams if str(p['team']) == t.team_id), None)

    def add_player_positions(self):
        for p in self.table:
            if p['element_type'] == 1:
                p['position'] = 'G'
            elif p['element_type'] == 2:
                p['position'] = 'D'
            elif p['element_type'] == 3:
                p['position'] = 'M'
            elif p['element_type'] == 4:
                p['position'] = 'F'

    def correct_pricing_values(self):
        for p in self.table:
            p['now_cost'] = p['now_cost'] / 10


class TeamTable:
    TEAM_TABLE_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    PLAYER_TABLE_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    PLAYER_INFO_URL_TEMPLATE = 'https://fantasy.premierleague.com/api/element-summary/{}/'

    def __init__(self):
        self.session = requests.Session()

        self.players = Player.objects.all()

        self.table = self.get_team_table()
        self.process_table()

    def get_team_table(self):
        team_table_s = self.session.get(self.TEAM_TABLE_URL).text
        team_table = json.loads(team_table_s)
        return team_table['teams']

    def process_table(self):
        self.get_next_games()
        pass

    def get_next_games(self):
        if self.players:
            # construct a lookup for team name against team id
            team_id_list = [t['id'] for t in self.table]
            team_name_list = [t['name'] for t in self.table]
            team_names = dict(zip(team_id_list, team_name_list))

            # get the first player id for each team (it doesn't matter which)
            # then lookup this ID to get information for their next game
            player_id_list = [self._get_any_player_id_from_team_id(t_id) for t_id in team_id_list]
            next_team_id_list = []
            next_team_diff_list = []
            for p_id in player_id_list:
                next_team, next_diff = self._extract_fixture_data_from_player_id(p_id)
                next_team_id_list.append(next_team)
                next_team_diff_list.append(next_diff)

            # construct a lookup for next opponent's team id and difficulty
            team_next_game_id = dict(zip(team_id_list, next_team_id_list))
            team_next_game_diff = dict(zip(team_id_list, next_team_diff_list))

            # append new values to table using previously created lookups
            for t in self.table:
                t['next_team_id'] = team_next_game_id[t['id']]
                t['next_team_name'] = team_names[t['next_team_id']]
                t['next_team_diff'] = team_next_game_diff[t['id']]

    def _get_any_player_id_from_team_id(self, team_id):
        return next((p.player_id for p in self.players if team_id == p.team_id), None)

    def _extract_fixture_data_from_player_id(self, player_id):
        fixtures_data = json.loads(self.session.get(self.PLAYER_INFO_URL_TEMPLATE.format(player_id)).text)['fixtures'][0]

        # get next team ID based on is_home attribute
        if fixtures_data['is_home']:
            next_team = fixtures_data['team_a']
        else:
            next_team = fixtures_data['team_h']

        difficulty = fixtures_data['difficulty']

        return next_team, difficulty


if __name__ == "__main__":
    table = TeamTable()
