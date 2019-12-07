from django.db import models


# Create your models here.
class Player(models.Model):
    player_id = models.CharField(default=0, max_length=3)
    name = models.CharField(max_length=200)
    name_raw = models.CharField(default='', max_length=200)
    team_id = models.IntegerField(default=0)
    team_code = models.IntegerField(default=0)
    team_name = models.CharField(default='', max_length=50)
    team_name_short = models.CharField(default='', max_length=3)
    position = models.CharField(default='', max_length=1)

    assists = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    bps = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)
    cost_change_event = models.IntegerField(default=0)
    dreamteam_count = models.IntegerField(default=0)
    event_points = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    own_goals = models.IntegerField(default=0)
    penalties_missed = models.IntegerField(default=0)
    penalties_saved = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    transfers_in = models.IntegerField(default=0)
    transfers_in_event = models.IntegerField(default=0)
    transfers_out = models.IntegerField(default=0)
    transfers_out_event = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)

    creativity = models.FloatField(default=0.0)
    ep_next = models.FloatField(default=0.0)
    ep_this = models.FloatField(default=0.0)
    form = models.FloatField(default=0.0)
    ict_index = models.FloatField(default=0.0)
    influence = models.FloatField(default=0.0)
    now_cost = models.FloatField(default=0.0)
    opt_cost = models.FloatField(default=0.0)
    points_per_game = models.FloatField(default=0.0)
    selected_by_percent = models.FloatField(default=0.0)
    threat = models.FloatField(default=0.0)
    value_form = models.FloatField(default=0.0)
    value_season = models.FloatField(default=0.0)

    updated = models.DateTimeField(auto_now=True)

    # hack to prevent PyCharm inspection errors
    objects = models.Manager()

    def __str__(self):
        return '{}, ({})'.format(self.name, self.team_name)


class Team(models.Model):
    team_id = models.CharField(default='', max_length=3)
    team_code = models.CharField(default='', max_length=3)
    team_name = models.CharField(default='', max_length=50)
    team_name_short = models.CharField(default='', max_length=3)

    next_game_team_id = models.IntegerField(default=0)
    next_game_team_name = models.CharField(default='', max_length=50)
    next_game_difficulty = models.IntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)

    # hack to prevent PyCharm inspection errors
    objects = models.Manager()

    def __str__(self):
        return self.team_name
