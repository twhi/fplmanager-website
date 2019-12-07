from .models import Player
from pulp import LpMinimize, LpMaximize, LpProblem, LpVariable, LpInteger, lpSum
import json
from django.core import serializers


class Opt:
    max_players_per_position = {
        'G': 2,
        'D': 5,
        'M': 5,
        'F': 3
    }

    def __init__(self, opt_parameter, max_budget, team, n_subs=None, include=None, exclude=None):
        self.opt_parameter = opt_parameter
        self.max_budget = max_budget
        self.team = team
        self.n_subs = n_subs
        self.include = include
        self.exclude = exclude

        # based on n_subs, determine if wildcard sim or not
        self.is_wildcard = False if self.n_subs else True

        self.players = Player.objects.all()
        self.set_opt_cost()
        self.data_length = range(len(self.players))

        self.opt_param_list = self.get_opt_param_list()
        self.opt_id_list = self.get_opt_id_list()
        self.opt_cost_list = self.get_opt_cost_list()

        if not self.is_wildcard:
            self.opt_owned_players_list = self.get_opt_owned_players_list()

        if self.include:
            self.opt_include_players_list = self.get_opt_include_players_list()

        if self.exclude:
            self.opt_exclude_players_list = self.get_opt_exclude_players_list()

        self.opt_pos_constraints = self.get_pos_constraints()
        self.opt_team_constraints = self.get_team_constraints()
        results_ids = self.run_optimisation()
        self.results = self.lookup_team_by_ids(results_ids)

    def set_opt_cost(self):
        player_found = False
        for p in self.players:
            for p_t in self.team:
                if p.player_id == p_t['player_id']:
                    player_found = True
                    p.opt_cost = p_t['opt_cost']
                    break
            if not player_found:
                p.opt_cost = p.now_cost
            player_found = False
    
    def lookup_team_by_ids(self, results_ids):
        team_list = []
        for res in results_ids:
            for p in self.players:
                if p.player_id == res:
                    team_list.append(p)
        return team_list
    
    def run_optimisation(self):
        # Declare problem instance, max/min problem
        self.prob = LpProblem("Squad", LpMaximize)

        # Declare decision variable - 1 if a player is part of the squad else 0
        self.decision = LpVariable.matrix(
            "decision", list(self.data_length), 0, 1, LpInteger)

        # Objective function -> Maximize specified optimisation parameter
        self.prob += lpSum(self.opt_param_list[i] * self.decision[i] for i in self.data_length)

        # Constraint definition
        self.add_constraints()

        # solve problem
        self.prob.solve()

        # extract selected players and return
        return [self.opt_id_list[i] for i in self.data_length if self.decision[i].varValue]

    def add_constraints(self):

        # team constraints
        # maximum of 3 players per team
        for team in self.opt_team_constraints:
            self.prob += lpSum(self.opt_team_constraints[team][i] * self.decision[i] for i in self.data_length) <= 3

        # position constraints
        # constrains the team to have 2 GK, 5 DEF, 5 MIN and 3 FW
        for pos in self.opt_pos_constraints:
            self.prob += lpSum(self.opt_pos_constraints[pos][i] * self.decision[i] for i in self.data_length) == self.max_players_per_position[pos]

        # price constraint
        # limits the overall price of the team to the specified budget
        self.prob += lpSum(self.opt_cost_list[i] * self.decision[i] for i in self.data_length) <= self.max_budget

        # players to include in the team constraint
        if self.include:
            self.prob += lpSum(self.opt_include_players_list[i] * self.decision[i] for i in self.data_length) == len(self.include)

        # players to exclude from the team constrain
        if self.exclude:
            self.prob += lpSum(self.opt_exclude_players_list[i] * self.decision[i] for i in self.data_length) == 0

        # initial squad constraint - ONLY USE IN TRANSFER SIMULATION
        # ensures that the final team has (15 - number of subs) players from the initial team
        if not self.is_wildcard:
            self.prob += lpSum(self.opt_owned_players_list[i] * self.decision[i] for i in self.data_length) == 15 - self.n_subs
    
    def get_team_constraints(self):
        teams = list(range(1, 21))
        outlist = {}

        for t in teams:
            list_result = []
            for p in self.players:
                if int(p.team_id) == t:
                    list_result.append(1)
                else:
                    list_result.append(0)
            outlist[t] = list_result
        return outlist

    def get_pos_constraints(self):
        pos_lookup = ['G', 'D', 'M', 'F']
        pos_constraints = {}
        for pos in pos_lookup:
            temp_result = []
            for p in self.players:
                if p.position == pos:
                    temp_result.append(1)
                else:
                    temp_result.append(0)
            pos_constraints[pos] = temp_result
        return pos_constraints

    def get_opt_include_players_list(self):
        opt_include_players_list = [0]*len(self.players)
        for idx, p in enumerate(self.players):
            for p_i in self.include:
                if p.player_id == p_i:
                    opt_include_players_list[idx] = 1
                    break
        return opt_include_players_list

    def get_opt_exclude_players_list(self):
        opt_exclude_players_list = [0]*len(self.players)
        for idx, p in enumerate(self.players):
            for p_e in self.exclude:
                if p.player_id == p_e:
                    opt_exclude_players_list[idx] = 1
                    break
        return opt_exclude_players_list

    def get_opt_owned_players_list(self):
        opt_owned_players_list = [0]*len(self.players)
        for idx, p in enumerate(self.players):
            for p_t in self.team:
                if p.player_id == p_t['player_id']:
                    opt_owned_players_list[idx] = 1
                    break
        return opt_owned_players_list

    def get_opt_param_list(self):
        # TODO: need to add multiplier for number of games next gameweek
        return [getattr(p, self.opt_parameter) for p in self.players]

    def get_opt_id_list(self):
        return [p.player_id for p in self.players]

    def get_opt_cost_list(self):
        return [float(p.opt_cost) for p in self.players]
