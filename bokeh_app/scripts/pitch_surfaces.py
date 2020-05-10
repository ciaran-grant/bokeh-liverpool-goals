# -*- coding: utf-8 -*-
"""
Created on Fri May  8 17:22:58 2020

@author: Ciaran
"""

def pitch_surfaces_tab(events_df, metrica_attack, metrica_defence, bokeh_attack, bokeh_defence, shirt_mapping, match_list):
    
    import metrica_to_bokeh as mtb
    import Metrica_PitchControl as mpc
    import pitch_value_model as pvm
    from bokeh.models import ColumnDataSource, Select, TextInput, Panel, Paragraph   
    from bokeh.layouts import row, column, WidgetBox
    import numpy as np
    from scipy import interpolate
    
    
    def make_dataset(play, event_frame, metrica_attack, metrica_defence, bokeh_attack, bokeh_defence, field_dimen = (106.,68.,), new_grid_size = 500):

        params = mpc.default_model_params(3) 

        event = events_df.loc[[(play, int(event_frame))]]
        tracking_frame = event['Start Frame'][0]

        att_frame = bokeh_attack.loc[(play,tracking_frame)]
        att_player_frame = att_frame[att_frame['player'] != "ball"]
        att_player_frame['Shirt Number'] = att_player_frame['player'].map(int).map(shirt_mapping[play]).fillna("")

        def_frame = bokeh_defence.loc[(play,tracking_frame)]
        def_player_frame = def_frame[def_frame['player'] != "ball"]
        def_player_frame['Shirt Number'] = def_player_frame['player'].map(int).map(shirt_mapping[play]).fillna("")

        ball_frame = att_frame[att_frame['player'] == "ball"]

        PPCF,xgrid,ygrid = pvm.lastrow_generate_pitch_control_for_event(play,event_frame, events_df, metrica_attack, metrica_defence, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
        PT = pvm.generate_relevance_at_event(play,event_frame, events_df, PPCF, params)
        PS = pvm.generate_scoring_opportunity(field_dimen = (106.,68.,),n_grid_cells_x = 50)
        PPV = pvm.generate_pitch_value(PPCF,PT,PS,field_dimen = (106.,68.,),n_grid_cells_x = 50)
        RPPV = pvm.generate_relative_pitch_value(play, event_frame, events_df, metrica_attack, PPV, xgrid, ygrid)

        xgrid_new = np.linspace( -field_dimen[0]/2., field_dimen[0]/2., new_grid_size)
        ygrid_new = np.linspace( -field_dimen[1]/2., field_dimen[1]/2., new_grid_size)

        PPCF_int = interpolate.interp2d(xgrid, ygrid, PPCF, kind = 'cubic')
        PPCF_new = PPCF_int(xgrid_new, ygrid_new)
        PPCF_dict = dict(image = [PPCF_new],x = [xgrid.min()],y = [ygrid.min()],dw = [field_dimen[0]], dh = [field_dimen[1]])
        PT_int = interpolate.interp2d(xgrid, ygrid, PT, kind = 'cubic')
        PT_new = PT_int(xgrid_new, ygrid_new)
        PT_dict = dict(image = [PT_new],x = [xgrid.min()],y = [ygrid.min()],dw = [field_dimen[0]], dh = [field_dimen[1]])
        PS_int = interpolate.interp2d(xgrid, ygrid, PS, kind = 'cubic')
        PS_new = PS_int(xgrid_new, ygrid_new)
        PS_dict = dict(image = [PS_new],x = [xgrid.min()],y = [ygrid.min()],dw = [field_dimen[0]], dh = [field_dimen[1]])
        PPV_int = interpolate.interp2d(xgrid, ygrid, PPV, kind = 'cubic')
        PPV_new = PPV_int(xgrid_new, ygrid_new)
        PPV_dict = dict(image = [PPV_new],x = [xgrid.min()],y = [ygrid.min()],dw = [field_dimen[0]], dh = [field_dimen[1]])
        RPPV_int = interpolate.interp2d(xgrid, ygrid, RPPV, kind = 'cubic')
        RPPV_new = RPPV_int(xgrid_new, ygrid_new)
        RPPV_dict = dict(image = [RPPV_new],x = [xgrid.min()],y = [ygrid.min()],dw = [field_dimen[0]], dh = [field_dimen[1]])


        event_src = ColumnDataSource(event)
        att_src = ColumnDataSource(att_player_frame)
        def_src = ColumnDataSource(def_player_frame)
        ball_src = ColumnDataSource(ball_frame)
        PPCF_src = ColumnDataSource(PPCF_dict)
        PT_src = ColumnDataSource(PT_dict)
        PS_src = ColumnDataSource(PS_dict)
        PPV_src = ColumnDataSource(PPV_dict)
        RPPV_src = ColumnDataSource(RPPV_dict)

        return event_src, att_src, def_src, ball_src, PPCF_src, PT_src, PS_src, PPV_src, RPPV_src, xgrid, ygrid
    
    def make_plot(event_src, att_src, def_src, ball_src, surface_src, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500):

        surface = mtb.plot_bokeh_surface_at_event(event_src, att_src, def_src, ball_src, surface_src, bokeh_attack, bokeh_defence, xgrid, ygrid)

        return surface

    def update(attr, old, new):
        
        match_selection = match_select.value
        event_selection = event_select.value

        new_event_src, new_att_src, new_def_src, new_ball_src, new_PPCF_src, new_PT_src, new_PS_src, new_PPV_src, new_RPPV_src, xgrid, ygrid = make_dataset(match_selection, event_selection, metrica_attack, metrica_defence, bokeh_attack, bokeh_defence)        

        event_src.data.update(new_event_src.data)
        att_src.data.update(new_att_src.data)
        def_src.data.update(new_def_src.data)
        ball_src.data.update(new_ball_src.data)
        PPCF_src.data.update(new_PPCF_src.data)
        PT_src.data.update(new_PT_src.data)
        PS_src.data.update(new_PS_src.data)
        PPV_src.data.update(new_PPV_src.data)
        RPPV_src.data.update(new_RPPV_src.data)
        

    match_select = Select(title="Select Match:", 
                          value=match_list[0], 
                          options=match_list)
    match_select.on_change('value', update)

    event_select = TextInput(title="Event:",
                            value="0")
    event_select.on_change('value', update)


        # Initial match to plot
    play = 'Liverpool [3] - 0 Bournemouth'
    event_frame = 0

    event_src, att_src, def_src, ball_src, PPCF_src, PT_src, PS_src, PPV_src, RPPV_src, xgrid, ygrid = make_dataset(play, event_frame, metrica_attack, metrica_defence, bokeh_attack, bokeh_defence)

    pitch_control = make_plot(event_src, att_src, def_src, ball_src, PPCF_src, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
    pitch_control.title.text = "Pitch Control"
    pitch_control.title.text_font_size = "20px"
    
    pitch_transition = make_plot(event_src, att_src, def_src, ball_src, PT_src, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
    pitch_transition.title.text = "Transition Likelihood"
    pitch_transition.title.text_font_size = "20px"
    
    probability_scoring = make_plot(event_src, att_src, def_src, ball_src, PS_src, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
    probability_scoring.title.text = "Scoring Likelihood"
    probability_scoring.title.text_font_size = "20px"
    
    pitch_value = make_plot(event_src, att_src, def_src, ball_src, PPV_src, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
    pitch_value.title.text = "Pitch Value"
    pitch_value.title.text_font_size = "20px"
    
    #relative_pitch_value = make_plot(event_src, att_src, def_src, ball_src, RPPV, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)

    # Paragraph for instructions and disclaimers
    instructions = Paragraph(text = "Select a match from the dropdown list below. Then enter an event number. Pitch Control shows which areas of the pitch a team is likely to maintain possession. Transision Likelihood is the region which the ball is likely to go to next based on ball travel time.. Scoring Likelihood is how likely you are to score based on purely distance to goal. Pitch Value combines each of these together to get a view of Pitch Control in the context of distance to ball and goal. If some of the HoverTools overlap, likely at events, then you can switch them off next to each plot.")
        
    # Layout setup
    control = WidgetBox(row(match_select, event_select))
    plot_layout = column(row(pitch_control, pitch_transition), row(probability_scoring, pitch_value))
    layout = column(instructions, column(control, plot_layout))

    tab2 = Panel(child = layout, title = 'Events - Pitch Value') 
   
    return tab2