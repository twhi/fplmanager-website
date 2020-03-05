from django.core import serializers
from django.db.models.query import QuerySet
from .models import Player
import json

class Lineup:

    def __init__(self, team, param):
        self.formations = {
            '532': [1, 5, 3, 2],
            '523': [1, 5, 2, 3],
            '541': [1, 5, 4, 1],
            '451': [1, 4, 5, 1],
            '442': [1, 4, 4, 2],
            '433': [1, 4, 3, 3],
            '352': [1, 3, 5, 2],
            '343': [1, 3, 4, 3],
        }
        self.positions = ['G', 'D', 'M', 'F']
        self.team_by_position = {
                'G': [],
                'D': [],
                'M': [],
                'F': []
            }
        self.param = param

        if isinstance(team, QuerySet) or isinstance(team[0], Player):
            team_sorted = self.sort_team_by_param(team)
            self.team_serialized = self.serialize_team(team_sorted)
        else:
            self.team_serialized = team

        self.sort_team_by_position(self.team_serialized)

    def serialize_team(self, team_sorted):
        team_serialized = json.loads(serializers.serialize('json', team_sorted))
        
        # add player id into serialized team
        for player in team_serialized:
            player['fields']['player_id'] = player['pk']  

        return [pl['fields'] for pl in team_serialized]

    def sort_team_by_param(self, team):
        return sorted(team, key=lambda k: getattr(k, self.param), reverse=True)

    def sort_team_by_position(self, team_serialized):
        for player in team_serialized:
            self.team_by_position[player['position']].append(player)

    def get_full_squad_sorted_by_position(self):
        SORT_ORDER = {'G': 0, 'D': 1, 'M': 2, 'F': 3}
        return sorted(self.team_serialized, key=lambda x: SORT_ORDER[x['position']])
    
    def choose_optimal_lineup(self):
        best_score = 0
        for formation in self.formations:
            # add players to squad
            lineup = []
            subs = []
            for pos, num in zip(self.positions, self.formations[formation]):
                lineup += self.team_by_position[pos][:num]
                subs += self.team_by_position[pos][num:]

            # calculate the score
            score_11 = sum(p[self.param] for p in lineup)
            score_subs = sum(p[self.param] for p in subs)
            score_tot = score_11 + score_subs

            # find max value i.e. captain choice
            cap = max(lineup, key=lambda x: x[self.param])

            # if it's the best one yet then save it
            if score_11 > best_score:
                best_score = score_11
                best = {
                    'formation': self.formations[formation],
                    'score_11': round(score_11, 1),
                    'score_tot': round(score_tot, 1),
                    'param': self.param,
                    'lineup': lineup,
                    'captain': cap['name'],
                    'subs': subs,
                }
        best['cost'] = round(sum(p['opt_cost'] for p in lineup) + sum(p['opt_cost'] for p in subs), 1)
        return best
    
    def lineup_from_serialized_team(self, is_sub_dict):
        formation_dict = {'G': 0, 'D': 0, 'M': 0, 'F': 0}
        team_by_pos = self.get_full_squad_sorted_by_position()
        cost = sum(p['opt_cost'] for p in self.team_serialized)  
        lineup = []
        subs = []
        
        for p in team_by_pos:
            if is_sub_dict[int(p['player_id'])]:
                subs.append(p)
            else:
                formation_dict[p['position']] += 1
                lineup.append(p)

        formation = [formation_dict['G'], formation_dict['D'], formation_dict['M'], formation_dict['F']]

        return {
            'team_serialized': self.team_serialized,
            'cost': cost,
            'formation': formation,
            'lineup': lineup,
            'subs': subs,
        }