# -*- coding: utf-8 -*-
"""
Created on Thu May  7 07:26:35 2020

@author: Ciaran
"""

# Pandas for data management
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import sys
import pathlib
# os methods for manipulating paths
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# Last Row data path
lastrow_DIR = pathlib.Path(os.path.join(dir_path, 'data'))

# extra_functions path
extra_functions_DIR = pathlib.Path(os.path.join(dir_path,'extra_functions'))

# Metrica Functions
laurie_metrica_DIR = os.path.join(extra_functions_DIR,'LaurieOnTracking-master')
sys.path.append(laurie_metrica_DIR)
import Metrica_IO as mio
import Metrica_Viz as mviz
import Metrica_Velocities as mvel
import Metrica_PitchControl as mpc

# Convert to Metrica
lastrow_to_metrica_DIR = os.path.join(extra_functions_DIR,'lastrow_to_friendsoftracking')
sys.path.append(lastrow_to_metrica_DIR)
import lastrow_to_friendsoftracking as lrfot
import pitch_value_model as pvm
import shirt_mappings as sm
import create_events as create

# Convert to Bokeh
convert_to_bokeh_DIR = os.path.join(extra_functions_DIR,'metrica_to_bokeh')
sys.path.append(convert_to_bokeh_DIR)
import metrica_to_bokeh as mtb

# Bokeh Football Pitch
danzn_pitch = os.path.join(extra_functions_DIR,'PyFootballPitch-master')
sys.path.append(danzn_pitch)
import Football_Pitch_Bokeh as fpbokeh

# Bokeh basics 
from bokeh.io import curdoc, output_notebook, show
from bokeh.models import ColumnDataSource, HoverTool, BooleanFilter, CDSView, LabelSet, PointDrawTool, Tabs
from bokeh.plotting import figure
from bokeh.colors import RGB
from matplotlib import cm

# Each tab is drawn by one script
from scripts.goals_overview import goals_overview_tab
from scripts.pitch_surfaces import pitch_surfaces_tab
from scripts.player_displacement_value import player_displacement_value_tab

# Read data into dataframes
last_row = pd.read_csv(os.path.join(lastrow_DIR/'liverpool_2019.csv'), index_col=('play', 'frame'))

# to Metrica Format
metrica_attack, metrica_defence = lrfot.lastrow_to_friendsoftracking(last_row)
metrica_attack = lrfot.lastrow_to_metric_coordinates(metrica_attack)
metrica_defence = lrfot.lastrow_to_metric_coordinates(metrica_defence)
metrica_attack, data_defence = lrfot.lastrow_to_single_playing_direction(metrica_attack, metrica_defence)

metrica_attack = pvm.lastrow_calc_player_velocities(metrica_attack,smoothing=True)
metrica_defence = pvm.lastrow_calc_player_velocities(data_defence,smoothing=True)

# Read in Events
events_dict, events_df = create.create_events(metrica_attack)

# Real Shirt Mapping
shirt_mapping = sm.create_consistent_shirt_mapping(last_row)
events_df = sm.real_shirt_mapping(events_df, shirt_mapping)

# to Bokeh Format
bokeh_attack = mtb.tracking_to_bokeh_format(metrica_attack)
bokeh_defence = mtb.tracking_to_bokeh_format(metrica_defence)

# List of available Matches
match_list = events_df.index.get_level_values(level=0).unique().tolist()

# Surface Colour Map
m_coolwarm_rgb = (255 * cm.coolwarm(range(256))).astype('int')
bokehpalette = [RGB(*tuple(rgb)).to_hex() for rgb in m_coolwarm_rgb]   

# Create each of the tabs
tab1 = goals_overview_tab(events_df, match_list, bokeh_attack, bokeh_defence, shirt_mapping)
tab2 = pitch_surfaces_tab(events_df, metrica_attack, metrica_defence, bokeh_attack, bokeh_defence, shirt_mapping, match_list)
tab3 = player_displacement_value_tab(events_df, metrica_attack, metrica_defence, bokeh_attack, bokeh_defence, shirt_mapping, match_list)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2, tab3])

# Put the tabs in the current document for display
curdoc().add_root(tabs)
