# -*- coding: utf-8 -*-
"""
Created on Tue May  5 07:53:26 2020

@author: Ciaran
"""

import numpy as np


def create_consistent_shirt_mapping(last_row_data):
    consistent_to_player_mapping = {}
    player_to_shirt_mapping = {}
    consistent_to_shirt_mapping = {}
    for play in last_row_data.index.get_level_values('play').unique():
    
        # consistent to player map
        players = last_row_data.loc[play]['player'].unique()
        num_players = len(players)
        consistent_players = np.array(range(0,num_players))
        player_map = dict(zip(consistent_players, players))
        consistent_to_player_mapping[play] = player_map
        
        # player to shirt map
        match = last_row_data.loc[play]
        players = match['player'].unique()
        player_shirt_map = {}
        for player in players:
            shirt_to_player = match[match['player'] == player]['player_num'].unique()
            player_shirt_map[player] = shirt_to_player[0]
        player_to_shirt_mapping[play] = player_shirt_map
    
        # combine both to get consistent to shirt map
        cons_to_player = consistent_to_player_mapping[play]
        player_to_shirt = player_to_shirt_mapping[play]
        play_mapping = {}
        for key,value in cons_to_player.items():
            play_mapping[key] = player_to_shirt[value]
    
        consistent_to_shirt_mapping[play] = play_mapping
    
    return consistent_to_shirt_mapping


def real_shirt_mapping(events, shirt_mapping, old_id = 'From'):
    shirt_numbers = []
    for play, frame in events.index:
        fake_scorer = events.loc[play][old_id][frame]
        real_scorer = shirt_mapping[play][int(fake_scorer)]
        shirt_numbers.append(real_scorer)

    events['Shirt Number'] = shirt_numbers
    return events