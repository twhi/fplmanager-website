from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.db.models import Q
from django.db import transaction
from django.template.loader import render_to_string

import json
import requests
from urllib.parse import urlparse, parse_qs
import operator

from .opt import Opt
from .models import Player, Team, Usage
from .forms import LoginCredsForm, LoginIdForm, WildcardForm, TransferForm, LineupForm
from .fpl import PlayerTable, TeamTable
from .lineup import Lineup
from .utils import OPT_PARAM_CHOICES


def prepare_team_for_template(lineup, param):
    SORT_ORDER = {'G': 0, 'D': 1, 'M': 2, 'F': 3}
    lineup['lineup'] = sorted(lineup['lineup'], key=lambda x: SORT_ORDER[x['position']])
    lineup['subs'] = sorted(lineup['subs'], key=lambda x: SORT_ORDER[x['position']])

    score_11 = sum(p[param] for p in lineup['lineup'])
    score_subs = sum(p[param] for p in lineup['subs'])
    score_tot = score_11 + score_subs

    captain = max(lineup['lineup'], key=lambda x:x[param])
    lineup.update({
        'captain': captain['name'],
        'param': param,
        'score_11': round(score_11, 1),
        'score_tot': round(score_tot, 1),
    })
    return lineup


def login_id_ajax(request):
    if request.POST.get('action') == 'post' and request.is_ajax():
        # extract data from ajax request
        account_id = request.POST.get('acc_id')

        if account_id:
            team_info = get_squad_from_id(request, account_id)

            if team_info:
                request.session['team_name'] = team_info['team_name']
                request.session['current_team'] = team_info['current_team']
                request.session['current_lineup'] = team_info['current_lineup']
                request.session['total_money_available'] = team_info['total_money_available']
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                response = JsonResponse({
                    'error': 'Unable to login with the provided credentials.'
                })
                response.status_code = 500
                return response


def login_creds_ajax(request):
    if request.POST.get('action') == 'post' and request.is_ajax():
        # extract data from ajax request
        creds = json.loads(request.POST.get('creds'))
        username = creds['user']
        password = creds['pass']
        team_info = get_team_info_from_creds(request, username, password)
        if team_info:
            # login success, save variables to session
            request.session['username'] = username
            request.session['password'] = password
            request.session['current_team'] = team_info['current_team']
            request.session['current_lineup'] = team_info['current_lineup']
            request.session['total_money_available'] = team_info['total_money_available']
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            response = JsonResponse({
                'error': 'Unable to login with the provided credentials.'
            })
            response.status_code = 500
            return response


def receive_sim_form(request):

    if not request.session.session_key:
        response = JsonResponse({
                'error': 'This function requires you to be logged in.'
            })
        response.status_code = 401
        return response

    if request.POST.get('action') == 'post' and request.is_ajax():
        # extract data from ajax request
        simulation_data = json.loads(request.POST.get('selected'))
        opt_param = simulation_data['opt_param']
        max_budget = float(simulation_data['max_budget'])
        num_subs = simulation_data['num_subs']
        if num_subs:
            num_subs = float(num_subs)
    
        include = simulation_data['include']
        exclude = simulation_data['exclude']

        # get current team and lineupp        
        current_team = request.session['current_team']
        current_lineup = request.session['current_lineup']
        current_lineup = prepare_team_for_template(current_lineup, opt_param)

        # run optimisation
        sim = Opt(opt_param, max_budget, current_team, num_subs, include, exclude)

        # check for optimisation error
        if sim.prob.status != 1:
            response = JsonResponse({
                'error': 'Unable to find a feasible solution with the provided parameters. Please check and try again.'
            })
            response.status_code = 500
            return response

        # save parameters of simulation for analytics
        u = Usage(
            session_type = 1 if 'username' in request.session else 0,
            user_id = request.session['unique_id'],
            sim_type = 0 if num_subs else 1,
            opt_param = opt_param,
            n_subs = num_subs if num_subs else None,
            include = ';'.join(str(i) for i in include) if include else None,
            exclude = ';'.join(str(i) for i in exclude) if exclude else None,
        )
        u.save()

        # extract results from optimisation and generate lineup
        optimal_team = sim.results
        l = Lineup(optimal_team, opt_param)
        lineup_opt = l.choose_optimal_lineup()

        # extract subs based on difference between current and opt squad
        outbound, inbound = extract_subs_from_lineups(current_team, l.team_serialized)

        # convert opt_param into something more readable
        opt_param_verbose = OPT_PARAM_CHOICES[[x[0] for x in OPT_PARAM_CHOICES].index(opt_param)][1]

        # prepare simulation results section
        context = {
                'current_team': current_lineup,
                'opt_param_verbose': opt_param_verbose,
                'max_budget': max_budget,
                'optimal_team': lineup_opt,
                'subs': zip(outbound, inbound),
            }
        results_section = render_to_string('simulation_results.html', context, request)

        # prepare optimal squad section
        context = {
                'type': 'new',
                'team': lineup_opt,
                'opt_param_verbose': opt_param_verbose,
                'inbound': [p['player_id'] for p in inbound],
                'outbound': [p['player_id'] for p in outbound],
            }
        optimal_squad_table = render_to_string('optimal_squad_table.html', context, request)

        # prepare current squad section
        context = {
                'type': 'current',
                'team': current_lineup,
                'opt_param_verbose': opt_param_verbose,
                'inbound': [p['player_id'] for p in inbound],
                'outbound': [p['player_id'] for p in outbound],
            }
        current_squad_table = render_to_string('optimal_squad_table.html', context, request)

        return JsonResponse({
            'results_section': results_section,
            'optimal_squad_table': optimal_squad_table,
            'current_squad_table': current_squad_table,
        })
        
    response = JsonResponse({
        'error': 'Something went very wrong D: \nLog out and back in again.'
        })
    response.status_code = 500
    return response


def get_autocomplete_players(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        players = Player.objects.filter(
            Q(name__icontains=q) | 
            Q(name_raw__icontains=q)
            )
        results = []
        for pl in players:
            label = pl.name + " (" + pl.team_name_short + ')'
            player_id = pl.player_id
            search_pos = pl.name_raw.lower().find(q)

            results.append({
                'label': label,
                'player_id': player_id,
                'search_pos': search_pos,
            })
        results.sort(key=operator.itemgetter('search_pos'))
        p = 0
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def wildcard(request):
    squad = None
    wildcard_form = WildcardForm()

    # if user is logged in then populate max budget field with user's max budget and get current squad
    if 'current_lineup' in request.session:
        if request.session['current_lineup']:
            wildcard_form.fields['max_budget'].initial = request.session['total_money_available']
            current_lineup = request.session['current_lineup']

    context = {
        'wildcard_form': wildcard_form,
        'wildcard': 'active',
        'squad': squad,
    }

    return render(request, 'wildcard.html', context)


def transfers(request):
    current_lineup = None
    transfer_form = TransferForm()

    # if user is logged in then populate max budget field with user's max budget and get current squad
    if 'current_lineup' in request.session:
        if request.session['current_lineup']:
            transfer_form.fields['max_budget'].initial = request.session['total_money_available']
            current_lineup = request.session['current_lineup']

    context = {
        'transfer_form': transfer_form,
        'transfers': 'active',
        'current_lineup': current_lineup,
    }

    return render(request, 'transfers.html', context)


def lineup(request):
    current_lineup = None
    lineup_form = LineupForm()

    # if user is logged in then get current squad
    if 'current_lineup' in request.session:
        if request.session['current_lineup']:
            current_lineup = request.session['current_lineup']

    context = {
        'lineup_form': lineup_form,
        'lineup': 'active',
        'current_lineup': current_lineup,
    }

    if 'lineup_simulation' in request.POST:
        lineup_form = LineupForm(request.POST)
        if lineup_form.is_valid():

            opt_param = lineup_form.cleaned_data['parameter']
            lineup_opt = Lineup(current_lineup['team_serialized'], opt_param)

            context.update({
                'optimal_squad': True,
                'type': 'optimised',
                'opt_param_verbose': OPT_PARAM_CHOICES[[x[0] for x in OPT_PARAM_CHOICES].index(opt_param)][1],
                'team': lineup_opt.choose_optimal_lineup(),
            })

            return render(request, 'lineup.html', context)

    return render(request, 'lineup.html', context)


def about(request):
    context = {
        'about': 'active'
    }
    return render(request, 'about.html', context)


def _get_is_sub_dict(t):
    # extract subs from team_info
    is_sub_dict = {}
    for p in t:
        if p['position'] >= 12:
            is_sub_dict[p['element']] = True
        else:
            is_sub_dict[p['element']] = False
    return is_sub_dict


def get_team_info_from_creds(request, username, password):
    session = requests.Session()
    login, session = log_into_fpl(session, username, password)

    if login.status_code == 200:

        # extract login status from URL
        try:
            login_status = parse_qs(urlparse(login.url).query)['state'][0]
        except KeyError as e:
            login_status = None

        if login_status == 'success':

            # get account specific info
            try:
                account_id = get_unique_account_id(session)
            except TypeError:
                # return some sort of error
                return None

            request.session['unique_id'] = account_id
            team_info = get_team(session, account_id)
            bank_balance = get_bank_balance(session, account_id)

            # extract subs from team_info
            is_sub_dict = _get_is_sub_dict(team_info)

            # construct a player_id list for database lookup
            lookup_ids = [p['element'] for p in team_info]
            request.session['current_team_ids'] = lookup_ids

            # perform database lookup
            team_qs = Player.objects.filter(player_id__in=lookup_ids)

            # look up player selling price by player_id and add to team list
            for player in team_qs:
                player.opt_cost = next(
                    (p['selling_price'] for p in team_info if p['element'] == player.player_id), None) / 10

            # get total money available based on squad and bank balance
            squad_value = round(sum(p.opt_cost for p in team_qs), 1)
            total_money_available = round(squad_value + bank_balance, 1)

            # sort team into a usable form
            l = Lineup(team_qs, 'ep_next')
            current_team = l.get_full_squad_sorted_by_position()
            current_lineup = l.lineup_from_serialized_team(is_sub_dict)

            return {
                'current_team': current_team,
                'current_lineup': current_lineup,
                'bank_balance': bank_balance,
                'squad_value': squad_value,
                'total_money_available': total_money_available,
                }
    

def _get_team_info(session, unique_id):
    url_template = 'https://fantasy.premierleague.com/api/entry/{}/'
    return json.loads(session.get(url_template.format(unique_id)).text)


def _get_last_event_info(session, unique_id, event):
    squad_url_template = 'https://fantasy.premierleague.com/api/entry/{u_id}/event/{ev}/picks/#/'
    return json.loads(session.get(squad_url_template.format(u_id=unique_id, ev=event)).text)


def get_squad_from_id(request, unique_id):
    # 475068

    request.session['unique_id'] = unique_id

    session = requests.Session()
    team_info = _get_team_info(session, unique_id)
    
    try:
        current_event = team_info['current_event']
    except TypeError:
        # GAME UPDATING ERROR CATCHING
        return None
    except KeyError:
        # ID NOT FOUND
        return None

    last_event_info = _get_last_event_info(session, unique_id, current_event)
    lookup_ids = [p['element'] for p in last_event_info['picks']]
    request.session['current_team_ids'] = lookup_ids

    is_sub_dict = _get_is_sub_dict(last_event_info['picks'])

    # perform database lookup
    team_qs = Player.objects.filter(player_id__in=lookup_ids)

    # look up player selling price by player_id and add to team list
    tot = 0
    for player in team_qs:
        player.opt_cost = player.now_cost
        tot += player.now_cost

    l = Lineup(team_qs, 'ep_next')
    current_team = l.get_full_squad_sorted_by_position()
    current_lineup = l.lineup_from_serialized_team(is_sub_dict)

    # serialize queryset so that it can be pass to template
    team = json.loads(serializers.serialize('json', team_qs))

    return {
        'team_name': team_info['name'],
        'current_team': current_team,
        'current_lineup': current_lineup,
        'total_money_available': tot if tot > 100 else 100,
    }


def extract_subs_from_lineups(lineup_old, lineup_new):
    outbound = []
    inbound = []
    for player_new, player_old in zip(lineup_new, lineup_old):
        if not any(p['player_id'] == player_new['player_id'] for p in lineup_old):
            inbound.append(player_new)
        if not any(p['player_id'] == player_old['player_id'] for p in lineup_new):
            outbound.append(player_old)

    # sort lists by position
    SORT_ORDER = {'G': 0, 'D': 1, 'M': 2, 'F': 3}
    inbound.sort(key=lambda x: SORT_ORDER[x['position']])
    outbound.sort(key=lambda x: SORT_ORDER[x['position']])

    return outbound, inbound


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def refresh_team(request):
    # request.session.username or request.session.team_name
    if 'username' in request.session:
        username = request.session['username']
        password = request.session['password']
        team_info = get_team_info_from_creds(request, username, password)
        if team_info:
            request.session['current_team'] = team_info['current_team']
            request.session['current_lineup'] = team_info['current_lineup']
            request.session['total_money_available'] = team_info['total_money_available']
    else:
        print('refresh team error')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@transaction.atomic
def update_players():
    player_table = PlayerTable()
    for p in player_table.table:
        Player.objects.update_or_create(
            player_id=p['id'],
            defaults={
                'name': p['web_name'],
                'name_raw': p['name_raw'],
                'team_id': p['team'],
                'team_code': p['team_code'],
                'position': p['position'],
                'assists': p['assists'],
                'bonus': p['bonus'],
                'bps': p['bps'],
                'clean_sheets': p['clean_sheets'],
                'cost_change_event': p['cost_change_event'],
                'dreamteam_count': p['dreamteam_count'],
                'event_points': p['event_points'],
                'goals_conceded': p['goals_conceded'],
                'goals_scored': p['goals_scored'],
                'minutes': p['minutes'],
                'own_goals': p['own_goals'],
                'penalties_missed': p['penalties_missed'],
                'penalties_saved': p['penalties_saved'],
                'red_cards': p['red_cards'],
                'saves': p['saves'],
                'total_points': p['total_points'],
                'transfers_in': p['transfers_in'],
                'transfers_in_event': p['transfers_in_event'],
                'transfers_out': p['transfers_out'],
                'transfers_out_event': p['transfers_out_event'],
                'yellow_cards': p['yellow_cards'],
                'creativity': float(p['creativity']),
                'ep_next': float(p['ep_next']),
                'ep_this': float(p['ep_this']),
                'form': float(p['form']),
                'ict_index': float(p['ict_index']),
                'influence': float(p['influence']),
                'now_cost': float(p['now_cost']),
                'points_per_game': float(p['points_per_game']),
                'selected_by_percent': float(p['selected_by_percent']),
                'threat': float(p['threat']),
                'value_form': float(p['value_form']),
                'value_season': float(p['value_season']),
                'kpi': float(p['kpi']),
                'top_50_count': int(p['top_50_count']),
                'price_change': float(p['price_change']),
            }
        )
        try:
            Player.objects.update_or_create(
                player_id=p['id'],
                defaults={
                    'team_name': p['team_name'],
                    'team_name_short': p['team_name_short'],
                }
            )
        except KeyError:
            pass


@transaction.atomic
def update_teams():
    team_table = TeamTable()
    for t in team_table.table:
        Team.objects.update_or_create(
            team_id=t['id'],
            defaults={
                'team_code': t['code'],
                'team_name': t['name'],
                'team_name_short': t['short_name'],
            }
        )
        try:
            Team.objects.update_or_create(
                team_id=t['id'],
                defaults={
                    'next_game_team_id': t['next_team_id'],
                    'next_game_team_name': t['next_team_name'],
                    'next_game_difficulty': t['next_team_diff'],
                }
            )
        except KeyError:
            pass


def landing(request):
    context = {
        'homepage': 'active',
        'wildcard_form': WildcardForm(),
        'substitution_form': TransferForm()
    }
    return render(request, 'index.html', context)


def get_bank_balance(session, account_id):
    # gets the player's remaining bank balance
    team_data_url = 'https://fantasy.premierleague.com/api/my-team/{0}/'.format(
        account_id)
    team_data_s = session.get(team_data_url).text
    return json.loads(team_data_s)['transfers']['bank'] / 10


def get_team(session, account_id):
    # gets the player's team based on the provided account ID
    team_data_url = 'https://fantasy.premierleague.com/api/my-team/{0}/'.format(
        account_id)
    team_data_s = session.get(team_data_url).text
    return json.loads(team_data_s)['picks']


def get_unique_account_id(session):
    data = json.loads(session.get('https://fantasy.premierleague.com/api/me/').text)
    return data['player']['entry']


def log_into_fpl(session, username, password):
    payload = {
        'login': username,
        'password': password,
        'app': 'plfpl-web',
        'redirect_uri': 'https://fantasy.premierleague.com/a/login'
    }

    login_url = 'https://users.premierleague.com/accounts/login/'
    login_status = session.post(login_url, data=payload)
    return login_status, session
