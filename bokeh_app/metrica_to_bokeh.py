# -*- coding: utf-8 -*-
"""
Created on Thu May  7 07:45:33 2020

@author: Ciaran
"""

def tracking_to_bokeh_format(metrica_data):
    
    import pandas as pd
    
    bokeh_data = metrica_data.copy()
    bokeh_data = bokeh_data.reset_index()
    bokeh_data = bokeh_data.set_index(['play', 'frame', 'Time [s]'])
    bokeh_data.columns = pd.MultiIndex.from_tuples([col.split("_")[-2:] for col in bokeh_data.columns])
    bokeh_data = bokeh_data.stack(level=0).reset_index()
    bokeh_data = bokeh_data.rename(columns={'level_3':'player'})
    bokeh_data = bokeh_data.set_index(['play', 'frame'])
    
    return bokeh_data

def plot_bokeh_frame(att_src, def_src, ball_src, plot=None, pitch_colour = 'green', edit = False, tracking_hover = True):
    
    from bokeh.plotting import figure 
    from bokeh.models import ColumnDataSource, HoverTool, BooleanFilter, CDSView, LabelSet, PointDrawTool
    from bokeh.io import output_notebook, show
    
    import Football_Pitch_Bokeh as fpbokeh
    
    line_colour = 'white'
    if pitch_colour == 'white':
        line_colour = 'black'
   
    if plot is None:
        p = fpbokeh.draw_pitch(hspan=[-53,53],vspan=[-34,34], fill_color = pitch_colour, line_color = line_colour)
    else:
        p = plot
    
    #attack
    patt = p.circle(x='x', y='y', source = att_src, color = 'red', alpha=0.7,size=10)
    #defence
    pdef = p.circle(x='x', y='y', source = def_src, color = 'blue', alpha=0.7,size=10)
    # ball
    pball = p.circle(x='x', y='y', source = ball_src, color = 'black', alpha=0.7,size=5)
    
    att_labels = LabelSet(x='x', y='y', x_offset=5,y_offset=5,
                      text='Shirt Number', text_font_size ="10pt",text_color='red',
                      source = att_src)   
    p.add_layout(att_labels)
    def_labels = LabelSet(x='x', y='y', x_offset=5,y_offset=5,
                      text='Shirt Number', text_font_size ="10pt",text_color='blue',
                      source = def_src)   
    p.add_layout(def_labels)
    
    if tracking_hover == True:
        hover = HoverTool()
        hover.mode = 'mouse'
        hover.tooltips = [
            #("Player", "@{Shirt Number}"),
            ("(x,y)", "($x, $y)")
        ]
        hover.renderers = [patt,pdef,pball]
        p.add_tools(hover)

    if edit == True:
        point_draw_att = PointDrawTool()
        point_draw_att.renderers = [patt]
        point_draw_att.num_objects = 12
        p.add_tools(point_draw_att)
        
        point_draw_def = PointDrawTool()
        point_draw_def.renderers = [pdef]
        point_draw_def.num_objects = 12
        p.add_tools(point_draw_def)
        
    return p


def plot_bokeh_events(src, plot=None, pitch_colour = 'green', event_hover = True):
    
    from bokeh.models import Arrow, OpenHead,LabelSet, HoverTool, Segment
    
    import Football_Pitch_Bokeh as fpbokeh
    
    line_colour = 'white'
    if pitch_colour == 'white':
        line_colour = 'black'
    
    if plot is None:
        p = fpbokeh.draw_pitch(hspan=[-53,53],vspan=[-34,34], fill_color = pitch_colour, line_color = line_colour)
    else:
        p = plot
    
    players = p.circle(source = src,
             x='Start X',
             y='Start Y',
             color = 'red',
             size=10,
             alpha=0.7)

    glyph = Segment(x0="Start X", 
                    y0="Start Y", 
                    x1="End X", 
                    y1="End Y", 
                    line_color="black", line_width=1)
    p.add_glyph(src, glyph)


    p.add_layout(LabelSet(x='Start X',
                          y='Start Y',
                          x_offset=3,
                          y_offset=3,
                          text='Shirt Number',
                          text_font_size='10pt',
                          text_color = 'red',
                          source = src,
                          level='glyph'))
    if event_hover == True:
        hover = HoverTool()
        hover.mode = 'mouse'
        hover.tooltips = [
                ("Event", "@play_frame"),            
                ("Player", "@{Shirt Number}"),
                ("Type", "@Type"),
                ("SubType", "@SubType"), 
                ("(Start X,Start Y)", "($x, $y)")
        ]
        hover.renderers = [players]
        p.add_tools(hover)
    
    return p


def plot_bokeh_surface_at_event(event_src, att_src, def_src, ball_src, surface_src, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500, point_click = False):
    
    import matplotlib as plt
    import matplotlib.cm as cm
    import numpy as np
    from bokeh.models import ColumnDataSource, HoverTool, BooleanFilter, CDSView, LabelSet, PointDrawTool, Tabs
    
    colormap =cm.get_cmap("bwr")
    bokehpalette = [plt.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))] 
    
    p = plot_bokeh_frame(att_src, def_src, ball_src, pitch_colour = 'white', edit = point_click, tracking_hover = False)
    p = plot_bokeh_events(event_src, p, pitch_colour = 'white')

    surface = p.image(source = surface_src, image='image',x='x',y='y',dw='dw',dh='dh', palette=bokehpalette, level="image"  )

    hover = HoverTool()
    hover.mode = 'mouse'
    hover.tooltips = [
        ("Value", "@image"),
        ("(x,y)", "($x, $y)")
    ]
    hover.renderers = [surface]
    p.add_tools(hover)
    
    return p

def player_displacement(play, play_frame, events,data_attack,data_defence,team,player,x_disp, y_disp):

    event_frame = events.loc[[(play,int(play_frame))]]
    tracking_frame = event_frame['Start Frame'][0]
    
    if team.lower() == 'attack':
        data_temp = data_attack.copy()
        xcol = "attack_"+str(player)+"_x"
        ycol = "attack_"+str(player)+"_y"
    
    elif team.lower() == 'defence':
        data_temp = data_defence.copy()
        xcol = "defense_"+str(player)+"_x"
        ycol = "defense_"+str(player)+"_y"
    
    data_temp.loc[(play, tracking_frame)][xcol] += x_disp
    data_temp.loc[(play, tracking_frame)][ycol] += y_disp
    
    return data_temp
    
def generate_surfaces_at_event(play, event_frame, events, tracking_attack, tracking_defence, params, field_dimen = (106.,68.,), n_grid_cells_x = 50):
    
    import pitch_value_model as pvm
    
    PPCF,xgrid,ygrid = pvm.lastrow_generate_pitch_control_for_event((play,event_frame), events, tracking_attack, tracking_defence, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
    PT = pvm.generate_relevance_at_event((play,event_frame), events, PPCF, params)
    PS = pvm.generate_scoring_opportunity(field_dimen = field_dimen,n_grid_cells_x = n_grid_cells_x)
    PPV = pvm.generate_pitch_value(PPCF,PT,PS,field_dimen = field_dimen,n_grid_cells_x = n_grid_cells_x)
    RPPV = pvm.generate_relative_pitch_value(play, event_frame, events, tracking_attack, PPV, xgrid, ygrid)

    return PPCF, PT, PS, PPV, RPPV, xgrid, ygrid

def plot_player_displacement_surface(play, event_frame, player, team, x_disp, y_disp, events_df, data_attack, bokeh_attack, data_defence, bokeh_defence, params):
    
    tracking_temp = player_displacement(play, event_frame, events_df,data_attack,data_defence,team,player,x_disp, y_disp)
    bokeh_temp = tracking_to_bokeh_format(tracking_temp)
    
    if team == 'attack':
        PPCF_temp, PT_temp, PS_temp, PPV_temp, RPPV_temp, xgrid, ygrid = generate_surfaces_at_event(play, event_frame, events_df, tracking_temp, data_defence, params)
        p = plot_bokeh_surface_at_event(play, event_frame, events_df,PPV_temp , bokeh_temp, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
    elif team == 'defence':
        PPCF_temp, PT_temp, PS_temp, PPV_temp, RPPV_temp, xgrid, ygrid = generate_surfaces_at_event(play, event_frame, events_df, data_attack, tracking_temp, params)
        p = plot_bokeh_surface_at_event(play, event_frame, events_df,PPV_temp , bokeh_attack, bokeh_temp, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
        
    return p


def generate_displacement_surface(play, event_frame, player, team, x_disp, y_disp, gain, events_df, data_attack, bokeh_attack, data_defence, bokeh_defence, params):
    
    PPCF, PT, PS, PPV, RPPV, xgrid, ygrid = generate_surfaces_at_event(play, event_frame, events_df, data_attack, data_defence, params)
    
    tracking_temp = player_displacement(play, event_frame, events_df,data_attack,data_defence,team,player,x_disp, y_disp)
    bokeh_temp = tracking_to_bokeh_format(tracking_temp)
    
    if team == 'attack':
        PPCF_temp, PT_temp, PS_temp, PPV_temp, RPPV_temp, xgrid, ygrid = generate_surfaces_at_event(play, event_frame, events_df, tracking_temp, data_defence, params)
        p = plot_bokeh_surface_at_event(play, event_frame, events_df,PPV_temp , bokeh_temp, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
    elif team == 'defence':
        PPCF_temp, PT_temp, PS_temp, PPV_temp, RPPV_temp, xgrid, ygrid = generate_surfaces_at_event(play, event_frame, events_df, data_attack, tracking_temp, params)
        p = plot_bokeh_surface_at_event(play, event_frame, events_df,PPV_temp , bokeh_attack, bokeh_temp, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
        
    if gain == 'offensive':
        PPCF_gain = PPCF - PPCF_temp
        PT_gain = PT - PT_temp
        PPV_gain = PPV - PPV_temp
        RPPV_gain = RPPV - RPPV_temp
    elif gain == 'defensive':
        PPCF_gain = PPCF_temp - PPCF 
        PT_gain = PT_temp - PT
        PPV_gain = PPV_temp - PPV
        RPPV_gain = RPPV_temp - RPPV
        
    return PPCF_gain, PT_gain, PPV_gain, RPPV_gain, tracking_temp, bokeh_temp, p
    
    

