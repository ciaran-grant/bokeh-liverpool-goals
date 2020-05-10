# -*- coding: utf-8 -*-
"""
Created on Sat May  9 15:28:22 2020

@author: Ciaran
"""

def player_displacement_value_tab(events_df, metrica_attack, metrica_defence, bokeh_attack, bokeh_defence, shirt_mapping, match_list):
    
    import metrica_to_bokeh as mtb
    import Metrica_PitchControl as mpc
    import pitch_value_model as pvm
    from bokeh.models import ColumnDataSource, Select, TextInput, Panel,Div, Button, DataTable, TableColumn, Paragraph
    from bokeh.events import ButtonClick
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
    
    def make_plot(event_src, att_src, def_src, ball_src, surface_src, bokeh_attack, bokeh_defence, xgrid, ygrid,field_dimen = (106.,68.,), new_grid_size = 500, point_click = False):

        surface = mtb.plot_bokeh_surface_at_event(event_src, att_src, def_src, ball_src, surface_src, bokeh_attack, bokeh_defence, xgrid, ygrid, point_click = True)
       
        return surface

    def update(attr, old, new):
        match_selection = match_select.value
        event_selection = event_select.value
        
        new_og_event_src, new_og_att_src, new_og_def_src, new_og_ball_src, new_og_PPCF_src, new_og_PT_src, new_og_PS_src, new_og_PPV_src, new_og_RPPV_src, xgrid, ygrid = make_dataset(match_selection, event_selection, metrica_attack, metrica_defence, bokeh_attack, bokeh_defence)
        og_att_src.data.update(new_og_att_src.data)
        og_def_src.data.update(new_og_def_src.data)
        og_ball_src.data.update(new_og_ball_src.data)
        og_PPCF_src.data.update(new_og_PPCF_src.data)
        og_PT_src.data.update(new_og_PT_src.data)
        og_PT_src.data.update(new_og_PS_src.data)
        og_PPV_src.data.update(new_og_PPV_src.data)
        og_RPPV_src.data.update(new_og_RPPV_src.data)
        
        new_event_src, new_att_src, new_def_src, new_ball_src, new_PPCF_src, new_PT_src, new_PS_src, new_PPV_src, new_RPPV_src, xgrid, ygrid = make_dataset(match_selection, event_selection, metrica_attack, metrica_defence, bokeh_attack, bokeh_defence)        
        event_src.data.update(new_event_src.data)
        att_src.data.update(new_att_src.data)
        def_src.data.update(new_def_src.data)
        ball_src.data.update(new_ball_src.data)
        PPCF_src.data.update(new_PPCF_src.data)
        PT_src.data.update(new_PT_src.data)
        PT_src.data.update(new_PS_src.data)
        PPV_src.data.update(new_PPV_src.data)
        RPPV_src.data.update(new_RPPV_src.data)

    match_select = Select(title="Select Match:", value=match_list[0], options=match_list)
    match_select.on_change('value', update)

    event_select = TextInput(title="Event:",value="0")
    event_select.on_change('value', update)
        
    player_select = TextInput(title="Index of Player Moved:",value="")
    
    team_select = Select(title="Team of Player Moved:", value="attack", options=["attack", "defence"])


    def recalculate(event):
        match_selection = match_select.value
        event_selection = event_select.value
        player_selection = int(player_select.value)
        team_selection = team_select.value
        
        if team_selection == 'attack':
            
            player = att_src.data['player'][player_selection]
            shirt = att_src.data['Shirt Number'][player_selection]
            # attack
            selected_att_x = att_src.data['x'][player_selection]
            selected_att_y = att_src.data['y'][player_selection]
            og_selected_att_x = og_att_src.data['x'][player_selection]
            og_selected_att_y = og_att_src.data['y'][player_selection]
            x_displacement = selected_att_x - og_selected_att_x
            y_displacement = selected_att_y - og_selected_att_y
        
            metrica_attack_new = mtb.player_displacement(match_selection, event_selection, events_df, metrica_attack, metrica_defence,'attack', player, x_displacement, y_displacement)
            bokeh_attack_new = mtb.tracking_to_bokeh_format(metrica_attack_new)
        
            new_event_src, new_att_src, new_def_src, new_ball_src, new_PPCF_src, new_PT_src, new_PS_src, new_PPV_src, new_RPPV_src, xgrid, ygrid = make_dataset(match_selection, event_selection, metrica_attack_new, metrica_defence, bokeh_attack_new, bokeh_defence)   
            
            event_src.data.update(new_event_src.data)
            att_src.data.update(new_att_src.data)
            def_src.data.update(new_def_src.data)
            ball_src.data.update(new_ball_src.data)
            PPCF_src.data.update(new_PPCF_src.data)
            PT_src.data.update(new_PT_src.data)
            PT_src.data.update(new_PS_src.data)
            PPV_src.data.update(new_PPV_src.data)
            RPPV_src.data.update(new_RPPV_src.data)
            
            pitch_value = make_plot(event_src, att_src, def_src, ball_src, PPV_src, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
            relative_pitch_value = make_plot(event_src, att_src, def_src, ball_src, RPPV_src, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
    
            
        elif team_selection == 'defence':
            
            player = def_src.data['player'][player_selection]
            shirt = def_src.data['Shirt Number'][player_selection]

            # defence
            selected_def_x = def_src.data['x'][player_selection]
            selected_def_y = def_src.data['y'][player_selection]
            og_selected_def_x = og_def_src.data['x'][player_selection]
            og_selected_def_y = og_def_src.data['y'][player_selection]
            x_displacement = selected_def_x - og_selected_def_x 
            y_displacement = selected_def_y - og_selected_def_y 
        
            metrica_defence_new = mtb.player_displacement(match_selection, event_selection, events_df, metrica_attack, metrica_defence,'defence', player, x_displacement, y_displacement)
            bokeh_defence_new = mtb.tracking_to_bokeh_format(metrica_defence_new)

            new_event_src, new_att_src, new_def_src, new_ball_src, new_PPCF_src, new_PT_src, new_PS_src, new_PPV_src, new_RPPV_src, xgrid, ygrid = make_dataset(match_selection, event_selection, metrica_attack, metrica_defence_new, bokeh_attack, bokeh_defence_new)   
            
            event_src.data.update(new_event_src.data)
            att_src.data.update(new_att_src.data)
            def_src.data.update(new_def_src.data)
            ball_src.data.update(new_ball_src.data)
            PPCF_src.data.update(new_PPCF_src.data)
            PT_src.data.update(new_PT_src.data)
            PT_src.data.update(new_PS_src.data)
            PPV_src.data.update(new_PPV_src.data)
            RPPV_src.data.update(new_RPPV_src.data)
            
            pitch_value = make_plot(event_src, att_src, def_src, ball_src, PPV_src, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
            relative_pitch_value = make_plot(event_src, att_src, def_src, ball_src, RPPV_src, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
    
   
    recalculate_button = Button(label="Re-Calculate Pitch Value")
    recalculate_button.on_event(ButtonClick, recalculate)
    
    # Initial match to plot
    play = 'Liverpool [3] - 0 Bournemouth'
    event_frame = 0

    og_event_src, og_att_src, og_def_src, og_ball_src, og_PPCF_src, og_PT_src, og_PS_src, og_PPV_src, og_RPPV_src, xgrid, ygrid = make_dataset(play, event_frame, metrica_attack, metrica_defence, bokeh_attack, bokeh_defence)
    event_src, att_src, def_src, ball_src, PPCF_src, PT_src, PS_src, PPV_src, RPPV_src, xgrid, ygrid = make_dataset(play, event_frame, metrica_attack, metrica_defence, bokeh_attack, bokeh_defence)
    
    pitch_value = make_plot(event_src, att_src, def_src, ball_src, PPV_src, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
    pitch_value.title.text = "Pitch Value"
    pitch_value.title.text_font_size = "20px"
    
    relative_pitch_value = make_plot(event_src, att_src, def_src, ball_src, RPPV_src, bokeh_attack, bokeh_defence, xgrid, ygrid, field_dimen = (106.,68.,), new_grid_size = 500)
    relative_pitch_value.title.text = "Relative Pitch Value"
    relative_pitch_value.title.text_font_size = "20px"
    
    # Create data tables for viewing movements
    columns = [
        TableColumn(field="Shirt Number", title = "Shirt Number"),
        TableColumn(field="player", title = "player"),
        TableColumn(field="x", title = "x"),
        TableColumn(field="y", title ="y"),
    ]
    att_table = DataTable(source=att_src, columns=columns, width=400, height=280, editable = True)
    att_title = Div(text="Red Team")
    def_table = DataTable(source=def_src, columns=columns, width=400, height=280, editable = True)
    def_title = Div(text="Blue Team")
    
    # Paragraph for instructions and disclaimers
    disclaimer = Paragraph(text = "*** Disclaimer - You can click the PointDrawTool in Pitch Value for each team to move a single player at a time. If you wish to re-calculate the Pitch Value based on the new location, you must add in a new player (click anywhere on the pitch with the PointDrawTool) and then remove them again (click on them to highlight only them, then press backspace). This is necessary to do for each team everytime you want to re-calculate Pitch Values. Any advice on correcting this would be appreciated! ***")
    instructions = Paragraph(text = "Select a match from the dropdown list below. Then enter an event number. If a player is moved, enter their Index to the respective table and select their team (Red = attack, Blue = defence). Pitch Value is the same as in 'Events - Pitch Value'. Relative Pitch Value highlights areas that will increase Pitch Value compared to the starting position. Again can turn off some HoverTools if necessary.")
    #notes = column(disclaimer, instructions)
                           
    # Layout setup
    control = WidgetBox(column(match_select, event_select, player_select, team_select, recalculate_button))
    plots = column(pitch_value, relative_pitch_value)
    tables = column(column(att_title, att_table), column(def_title, def_table))
    layout = column(disclaimer, instructions, row(plots, column(control, tables)))

    tab3 = Panel(child = layout, title = 'Player Displacement - Pitch Value') 
    
    return tab3