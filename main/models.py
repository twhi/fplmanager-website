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
    top_50_count = models.IntegerField(default=0)

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
    kpi = models.FloatField(default=0.0)
    price_change = models.FloatField(default=0.0)

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


class Usage(models.Model):
    
    """
    SESSION TYPE:
        ID LOGIN
        session_type = 0

        CREDS LOGIN
        session_type = 1

    SIM TYPE:
        TRANSFER
        sim_type = 0
        
        WILDCARD
        sim_type = 1

        LINEUP
        sim_type = 2
    """

    session_type = models.IntegerField()
    user_id = models.IntegerField()
    sim_type = models.IntegerField()
    opt_param = models.CharField(max_length=64)
    n_subs = models.IntegerField(blank=True, null=True, default=0)
    include = models.CharField(blank=True, null=True, default='', max_length=1000)
    exclude = models.CharField(blank=True, null=True, default='', max_length=1000)

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):

        if self.sim_type == 0:
            sim_type_text = 'Transfer Sim'
        elif self.sim_type == 1:
            sim_type_text = 'Wildcard Sim'
        elif self.sim_type == 2:
            sim_type_text = 'Lineup Sim'

        if self.session_type == 0:
            session_type_text = 'ID Session'
        elif self.session_type == 1:
            session_type_text = 'Credential Session'

        return '{user} - {sim_type}, {session_type}'.format(
            user=self.user_id,
            sim_type=sim_type_text,
            session_type=session_type_text
            )
