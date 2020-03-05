import asyncio
from datetime import datetime
import aiohttp
from understat import Understat
from .models import XgLookup
import requests
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

CURRENT_SEASON = 2019
PLAYER_TABLE_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'

class XgStats:

    PLAYER_TABLE_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    
    def __init__(self):
        self.xg_lookup = XgLookup.objects.all()
        if len(self.xg_lookup) > 0:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.data = loop.run_until_complete(self.fetch_data())
            self.extract_xg_season()
            self.add_data_to_db()
    
    def _get_fpl_player_table(self):
        master_table_s = self._session.get(self.PLAYER_TABLE_URL).text
        master_table = json.loads(master_table_s)
        return master_table['elements']

    def _find_new_xg_player_id(self, name):
        fpl_player_table = self._get_fpl_player_table()
        remove_list = [x.player_id for x in self.xg_lookup]
        fpl_player_table_trim = [p for p in fpl_player_table if p['id'] not in remove_list]
        
        found_player = next((item for item in fpl_player_table_trim if item["web_name"] == name), None)

        if not found_player:
            found_player = next((item for item in fpl_player_table_trim if ' '.join(item["first_name"], item['second_name']) == name), None)

        choice_one = process.extractOne(name, f_plus_s_dict.keys())
        choice_two = process.extractOne(name, web_dict.keys())
        if choice_one[1] > choice_two[1]:
            return f_plus_s_dict[choice_one[0]], choice_one[1]
        else:
            return web_dict[choice_two[0]], choice_two[1]
        p = 0
    
    @property
    def _session(self):
        if hasattr(self, 'session'):
            return self.session
        else:
            return requests.Session()
    
    def add_data_to_db(self):
        for player in self.data:
            try:
                p = XgLookup.objects.get(xg_name=self.data[player]['name'])
                p.xg_season = self.data[player]['xg_season']
                p.save()
            except:
                print('unable to find player, finding...', self.data[player]['name'])
                new_player_id = self._find_new_xg_player_id(self.data[player]['name'])
                pass

    def extract_xg_season(self):
        for player in self.data:
            xg_season = 0
            for game in self.data[player]['games']:
                if int(game['season']) == CURRENT_SEASON:
                    xg_season += float(game['xG'])
            self.data[player]['xg_season'] = xg_season

    
    async def fetch_data(self):
        async with aiohttp.ClientSession() as session:
            
            understat = Understat(session)
            data = await understat.get_league_players('EPL', CURRENT_SEASON)
            
            player_ids = [int(player['id']) for player in data]
            player_names = [player['player_name'].replace('&#039;', '\'') for player in data]
            players = {k: {'name': v} for k, v in dict(zip(player_ids, player_names)).items()}

            for p_id, p_name in players.items():                             
                data = await understat.get_player_matches(p_id)
                players[p_id]['games'] = data

        return players
                    
                        

if __name__ == '__main__':

    XgStats()