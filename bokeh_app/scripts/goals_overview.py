# -*- coding: utf-8 -*-
"""
Created on Thu May  7 07:28:17 2020

@author: Ciaran
"""

def goals_overview_tab(events_df, match_list, bokeh_attack, bokeh_defence, shirt_mapping):
    
    import metrica_to_bokeh as mtb
    from bokeh.models import ColumnDataSource, Select, TextInput, Panel, Paragraph   
    from bokeh.layouts import row, column, WidgetBox
    
    def make_dataset(play, event_frame, tracking_attack, tracking_defence):
        if event_frame == "All":
            event = events_df.loc[[(play)]]
        else:
            event = events_df.loc[[(play, int(event_frame))]]

        tracking_frame = event['Start Frame'][0]

        att_frame = tracking_attack.loc[(play,tracking_frame)]
        att_player_frame = att_frame[att_frame['player'] != "ball"]
        att_player_frame['Shirt Number'] = att_player_frame['player'].map(int).map(shirt_mapping[play]).fillna("")

        def_frame = tracking_defence.loc[(play,tracking_frame)]
        def_player_frame = def_frame[def_frame['player'] != "ball"]
        def_player_frame['Shirt Number'] = def_player_frame['player'].map(int).map(shirt_mapping[play]).fillna("")

        ball_frame = att_frame[att_frame['player'] == "ball"]
           
        event_src = ColumnDataSource(event)
        att_src = ColumnDataSource(att_player_frame)
        def_src = ColumnDataSource(def_player_frame)
        ball_src = ColumnDataSource(ball_frame)
            
        return event_src, att_src, def_src, ball_src
    
    def make_plot(event_src, event_frame, att_src, def_src, ball_src):
                
        events = mtb.plot_bokeh_events(event_src)
        frame = mtb.plot_bokeh_frame(att_src, def_src, ball_src)
        frame = mtb.plot_bokeh_events(event_src, plot = frame)
            
        return events, frame

    def update(attr, old, new):
        match_selection = match_select.value
        event_selection = event_select.value
        
        new_event_src, new_att_src, new_def_src, new_ball_src = make_dataset(match_selection, event_selection, bokeh_attack, bokeh_defence)        
        event_src.data.update(new_event_src.data)
        att_src.data.update(new_att_src.data)
        def_src.data.update(new_def_src.data)
        ball_src.data.update(new_ball_src.data)
        
        
    match_select = Select(title="Select Match:", 
                    value=match_list[0], 
                    options=match_list)
    match_select.on_change('value', update)

    event_select = TextInput(value="1", title="Event:")
    event_select.on_change('value', update)


# Initial match to plot
    match = 'Liverpool [3] - 0 Bournemouth'
    event_frame = 1

    event_src, att_src, def_src, ball_src = make_dataset(match, event_frame, bokeh_attack, bokeh_defence)

    event, frame = make_plot(event_src, event_frame, att_src, def_src, ball_src)
    event.title.text = 'Events'
    event.title.text_font_size = "20px"
    frame.title.text = "Tracking"
    frame.title.text_font_size = "20px"
    
    
    # Paragraph for instructions and disclaimers
    instructions = Paragraph(text = "Select a match from the dropdown list below. Then enter an event number or 'All' to see all events.")
    
    # Layout setup
    control = WidgetBox(row(match_select, event_select))
    plot_layout = row(event, frame)
    layout = column(instructions, column(control, plot_layout))

    tab1 = Panel(child = layout, title = 'Liverpool Goals') 
   
    return tab1