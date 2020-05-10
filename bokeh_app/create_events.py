# -*- coding: utf-8 -*-
"""
Created on Tue May  5 07:40:41 2020

@author: Ciaran
"""
import pandas as pd
import numpy as np

def create_events(tracking_data):
    
    # Liverpool v Bournemouth
    liv30bou = {
        'play' : 'Liverpool [3] - 0 Bournemouth',
        'team' : ['Liverpool','Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['GROUND PASS', 'THROUGH BALL','GROUND PASS','ON TARGET-GOAL'],
        'start_time' : [0, 2.1, 5.3, 6.6],
        'end_time' : [1.05, 3.55, 5.9, 7.3],
        'player_from' : ['3', '4', '1', '2'],
        'player_to' : ['4', '1', '2', np.NaN]
    }

    # Bayern v Liverpool
    bay01liv = {
        'play' : 'Bayern 0 - [1] Liverpool',
        'team' : ['Liverpool','Liverpool'],
        'event_type' : ['PASS', 'SHOT'],
        'event_subtype' : ['HIGH PASS','ON TARGET-GOAL'],
        'start_time' : [0.75, 6.45],
        'end_time' : [3.9, 7.85],
        'player_from' : ['2', '1'],
        'player_to' : ['1', np.NaN]
    }
    
    # Fulham v Liverpool
    ful01liv = {
        'play' : 'Fulham 0 - [1] Liverpool',
        'team' : ['Liverpool','Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['GROUND PASS', 'THROUGH BALL','PULL BACK','ON TARGET-GOAL'],
        'start_time' : [0.7,5.9,7.65,8.4],
        'end_time' : [2.05,6.45,8.4,8.75],
        'player_from' : ['5', '1', '4', '1'],
        'player_to' : ['1', '4', '1', np.NaN]
    }
    
    # 'Southampton 1 - [2] Liverpool'
    sou12liv = {
        'play' : 'Southampton 1 - [2] Liverpool',
        'team' : ['Liverpool','Liverpool'],
        'event_type' : ['PASS', 'SHOT'],
        'event_subtype' : ['HEADED PASS','ON TARGET-GOAL'],
        'start_time' : [3.5,11.6],
        'end_time' : [5.45,12.5],
        'player_from' : ['6', '1'],
        'player_to' : ['1', np.NaN]
    }
    
    # 'Liverpool [2] - 0 Porto'
    liv20por = {
        'play' : 'Liverpool [2] - 0 Porto',
        'team' : ['Liverpool','Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['GROUND PASS', 'THROUGH BALL','LOW CROSS','ON TARGET-GOAL'],
        'start_time' : [2.8,6.00,8.15,8.95],
        'end_time' : [4.45,7.3,8.95,9.45],
        'player_from' : ['1', '2', '3', '1'],
        'player_to' : ['2', '3', '1', np.NaN]
    }
    
    
    # 'Porto 0 - [2] Liverpool'
    por02liv = {
        'play' : 'Porto 0 - [2] Liverpool',
        'team' : ['Liverpool','Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['GROUND PASS', 'GROUND PASS', 'THROUGH BALL','ON TARGET-GOAL'],
        'start_time' : [1.7,4.25,8.65,11.6],
        'end_time' : [2.75,6.35,10.55,12.5],
        'player_from' : ['2', '4', '3', '1'],
        'player_to' : ['4', '3', '1', np.NaN]
    }
    
    
    # 'Liverpool [4] - 0 Barcelona'
    liv40bar = {
        'play' :'Liverpool [4] - 0 Barcelona',
        'team' : ['Liverpool','Liverpool'],
        'event_type' : ['PASS', 'SHOT'],
        'event_subtype' : ['CORNER', 'ON TARGET-GOAL'],
        'start_time' : [4.55,5.95],
        'end_time' : [5.95,6.5],
        'player_from' : ['2', '1'],
        'player_to' : ['1', np.NaN]
    }
    
    # 'Liverpool [1] - 0 Wolves'
    liv10wol = {
        'play' : 'Liverpool [1] - 0 Wolves',
        'team' : ['Liverpool','Liverpool','Liverpool','Liverpool', 'Liverpool'],
        'event_type' : ['PASS', 'PASS', 'PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['GROUND PASS', 'GROUND PASS','THROUGH BALL', 'LOW CROSS','ON TARGET-GOAL'],
        'start_time' : [0.0,2.15,3.55,5.35,6.75],
        'end_time' : [2.15,3.55,5.35,6.75,7.3],
        'player_from' : ['6', '1', '5', '1', '6'],
        'player_to' : ['1', '5', '1', '6', np.NaN]
    }
    
    # 'Liverpool [3] - 0 Norwich'
    liv30nor = {
        'play' : 'Liverpool [3] - 0 Norwich',
        'team' : ['Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['GROUND PASS', 'HIGH CROSS','HEADED ON TARGET-GOAL'],
        'start_time' : [1.4,4,5.8],
        'end_time' : [2.7,5.8,7.15],
        'player_from' : ['1', '3', '8'],
        'player_to' : ['3', '8', np.NaN]
    }
    
    # 'Liverpool [2] - 1 Chelsea'
    liv21che = {
        'play' : 'Liverpool [2] - 1 Chelsea',
        'team' : ['Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['THROUGH BALL','PULL BACK','ON TARGET-GOAL'],
        'start_time' : [4.05,7.1,8.05],
        'end_time' : [7.1,8.05,9.5],
        'player_from' : ['1', '2', '1'],
        'player_to' : ['2', '1', np.NaN]
    }
    
    # 'Liverpool [2] - 1 Newcastle'
    liv21new = {
        'play' : 'Liverpool [2] - 1 Newcastle',
        'team' : ['Liverpool','Liverpool'],
        'event_type' :['PASS', 'SHOT'],
        'event_subtype' : ['THROUGH BALL','ON TARGET-GOAL'],
        'start_time' : [2.4,6.25],
        'end_time' : [4.4,7.2],
        'player_from' : ['2', '1'],
        'player_to' : ['1', np.NaN]
    }
    
    # 'Liverpool [2] - 0 Salzburg'
    liv20sal = {
        'play' : 'Liverpool [2] - 0 Salzburg',
        'team' : ['Liverpool','Liverpool','Liverpool','Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['GROUND PASS', 'GROUND PASS', 'GROUND PASS', 'THROUGH BALL', 'LOW CROSS', 'ON TARGET-GOAL'],
        'start_time' : [1.3,2.85,3.7,4.85,7.4,8.2],
        'end_time' : [2.65,3.7,4.85,7.4,8.2,8.85],
        'player_from' : ['1', '7', '8', '7','5','1'],
        'player_to' : [ '7', '8', '7','5','1', np.NaN]
    }
    
    # 'Genk 0 - [3] Liverpool'
    gen03liv = {
        'play' : 'Genk 0 - [3] Liverpool',
        'team' : ['Liverpool','Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['GROUND PASS', 'GROUND PASS', 'THROUGH BALL','ON TARGET-GOAL'],
        'start_time' : [2.6,4.1,5.9,7.55],
        'end_time' : [4.1,5,7.55,8.9],
        'player_from' : ['4', '3', '1', '2'],
        'player_to' : ['3', '1', '2', np.NaN]
    }
    
    # 'Liverpool [2] - 0 Man City'
    liv20man = {
        'play' : 'Liverpool [2] - 0 Man City',
        'team' : ['Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['AERIAL PASS', 'HIGH CROSS','HEADED ON TARGET-GOAL'],
        'start_time' : [0.0,4.95,6.95],
        'end_time' : [3.8,6.95,8.1],
        'player_from' : ['6', '1', '5'],
        'player_to' : ['1', '5', np.NaN]
    }
    
    # 'Liverpool [1] - 0 Everton'
    liv10eve = {
        'play' : 'Liverpool [1] - 0 Everton',
        'team' : ['Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['GROUND PASS', 'THROUGH BALL','ON TARGET-GOAL'],
        'start_time' : [0.35,5.55,8.35],
        'end_time' : [1.75,7.35,9.65],
        'player_from' : ['7', '1', '2'],
        'player_to' : ['1', '2', np.NaN]
    }
    
    # 'Liverpool [2] - 0 Everton'
    liv20eve = {
        'play' : 'Liverpool [2] - 0 Everton',
        'team' : ['Liverpool','Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['GROUND PASS', 'AERIAL PASS', 'THROUGH BALL','ON TARGET-GOAL'],
        'start_time' : [0.0,3.1,10.70,12.1],
        'end_time' : [1.95,5.35,12.1,13],
        'player_from' : ['7', '6', '1', '8'],
        'player_to' : ['6', '1', '8', np.NaN]
    }
    
    # 'Bournemouth 0 - 3 Liverpool'
    bou03liv = {
        'play' : 'Bournemouth 0 - 3 Liverpool',
        'team' : ['Liverpool','Liverpool'],
        'event_type' : ['PASS', 'SHOT'],
        'event_subtype' : ['THROUGH BALL','ON TARGET-GOAL'],
        'start_time' : [4.05,6.25],
        'end_time' : [6.25,7.55],
        'player_from' : ['2', '1'],
        'player_to' : ['1', np.NaN]
    }
    
    # 'Liverpool [1] - 0 Watford'
    liv10wat = {
        'play' : 'Liverpool [1] - 0 Watford',
        'team' : ['Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['THROUGH BALL','THROUGH BALL','ON TARGET-GOAL'],
        'start_time' : [1.6,4.75,9.55],
        'end_time' : [4.75,7.65,10.6],
        'player_from' : ['8', '1', '3'],
        'player_to' :['1', '3', np.NaN]
    }
    
    # 'Leicester 0 - [3] Liverpool'
    lei03liv = {
        'play' : 'Leicester 0 - [3] Liverpool',
        'team' : ['Liverpool','Liverpool','Liverpool'],
        'event_type' : ['PASS', 'PASS', 'SHOT'],
        'event_subtype' : ['THROUGH BALL','LOW CROSS','ON TARGET-GOAL'],
        'start_time' : [1.2,2.95,4.8],
        'end_time' : [2.95,3.95,5.4],
        'player_from' : ['10', '2', '1'],
        'player_to' : ['2', '1', np.NaN]
    }
    
    matches_events = [liv30bou,bay01liv,ful01liv,sou12liv,liv20por,por02liv,liv40bar,liv10wol,liv30nor,liv21che,liv21new,liv20sal,gen03liv,liv20man,liv10eve,liv20eve,bou03liv,liv10wat,lei03liv]

    events_dict = {}
    for m in matches_events:
        
        mplay = m['play']
        mteam = m['team']
        mevent_type = m['event_type']
        mevent_subtype = m['event_subtype']
        mstart_time = m['start_time']
        mend_time = m['end_time']
        mplayer_from = m['player_from']
        mplayer_to = m['player_to']
        
    # Create dataframe
        match = tracking_data.loc[mplay]
        name = mplay.split(" ")[0][:3].lower() + mplay.split(" ")[1] + mplay.split(" ")[-2] + mplay.split(" ")[-1][:3].lower()
        ball_xy = match[['ball_x', 'ball_y']]
        num_events = len(mevent_type)
        mindex = [mplay] * num_events
        mstart_frame = [t * 20 for t in mstart_time]
        mend_frame = [t * 20 for t in mend_time]
        mstart_x = [ball_xy['ball_x'][mstart_frame[x]] for x in range(0,num_events)]
        mstart_y = [ball_xy['ball_y'][mstart_frame[y]] for y in range(0,num_events)]
        mend_x = [ball_xy['ball_x'][mend_frame[x]] for x in range(0,num_events)]
        mend_y = [ball_xy['ball_y'][mend_frame[y]] for y in range(0,num_events)]

        event = {
            'play' : mindex,
            'Team' : mteam,
            'Type' : mevent_type,
            'SubType' : mevent_subtype,
            'Start Frame' : mstart_frame,
            'Start Time [s]' : mstart_time,
            'End Frame' : mend_frame,
            'End Time [s]' : mend_time,
            'From' : mplayer_from,
            'To' : mplayer_to,
            'Start X' : mstart_x,
            'Start Y' : mstart_y,
            'End X' : mend_x,
            'End Y' : mend_y
        }
    
        event_df = pd.DataFrame(event)
        event_df['frame'] = event_df.index
        event_df.set_index(['play','frame'], inplace = True)
        events_dict[name] = event_df

    events_df = pd.DataFrame()
    for match in events_dict.keys():
        match_df = events_dict[match]
        match_df_reset = match_df.reset_index()
        events_df = events_df.append(match_df_reset)
    events_df = events_df.set_index(['play', 'frame'])
    
    return events_dict , events_df

