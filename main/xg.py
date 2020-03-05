import asyncio
from datetime import datetime
import aiohttp
from understat import Understat
from .models import Player, XgLookup

CURRENT_SEASON = 2019

class XgStats:

    def __init__(self):
        loop = asyncio.get_event_loop()
        self.data = loop.run_until_complete(self.fetch_data())
        self.extract_xg_season()

        ender = True
    
    def extract_xg_season(self):
        for player in self.data:
            xg_season = 0
            for game in self.data[player]['games']:
                if int(game['season']) == CURRENT_SEASON:
                    xg_season += float(game['xG'])
            self.data[player]['xG'] = xg_season
            print(self.data[player]['name'], 'has a total xg of', xg_season)

    
    async def fetch_data(self):
        async with aiohttp.ClientSession() as session:
            understat = Understat(session)
            data = await understat.get_league_players('EPL', CURRENT_SEASON)
            player_ids = [int(player['id']) for player in data]
            player_names = [player['player_name'] for player in data]
            players = {k: {'name': v} for k, v in dict(zip(player_ids, player_names)).items()}
            count = 1
            for p_id, p_name in players.items():                             
                print('Getting data for player {current} out of {total}'.format(
                    current=count,
                    total=len(players)
                ))
                count += 1
                data = await understat.get_player_matches(p_id)
                players[p_id]['games'] = data

        return players
                    
                        

if __name__ == '__main__':

    XgStats()