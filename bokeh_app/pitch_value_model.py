# -*- coding: utf-8 -*-
"""
Created on Tue May  5 07:24:33 2020

@author: Ciaran
"""
import numpy as np
import Metrica_Viz as mviz
import scipy
import scipy.signal as signal

def remove_player_velocities(team):
    # remove player velocoties and acceleeration measures that are already in the 'team' dataframe
    columns = [c for c in team.columns if c.split('_')[-1] in ['vx','vy','ax','ay','speed','acceleration']] # Get the player ids
    team = team.drop(columns=columns)
    return team

def lastrow_calc_player_velocities(team, smoothing=True, filter_='Savitzky-Golay', window=7, polyorder=1, maxspeed = 12):
    """ calc_player_velocities( tracking_data )
    
    Calculate player velocities in x & y direciton, and total player speed at each timestamp of the tracking data
    
    Parameters
    -----------
        team: the tracking DataFrame for home or away team
        smoothing: boolean variable that determines whether velocity measures are smoothed. Default is True.
        filter: type of filter to use when smoothing the velocities. Default is Savitzky-Golay, which fits a polynomial of order 'polyorder' to the data within each window
        window: smoothing window size in # of frames
        polyorder: order of the polynomial for the Savitzky-Golay filter. Default is 1 - a linear fit to the velcoity, so gradient is the acceleration
        maxspeed: the maximum speed that a player can realisitically achieve (in meters/second). Speed measures that exceed maxspeed are tagged as outliers and set to NaN. 
        
    Returrns
    -----------
       team : the tracking DataFrame with columns for speed in the x & y direction and total speed added

    """
    # remove any velocity data already in the dataframe
    team = remove_player_velocities(team)
    
    # Get the player ids
    player_ids = np.unique( [ c[:-2] for c in team.columns if c[:3] in ['att','def'] ] )

    # Calculate the timestep from one frame to the next. Should always be 0.05 within the same half
    dt = team['Time [s]'].diff()

    # estimate velocities for players in team
    maxspeed = 12
    smoothing=True
    filter_='Savitzky-Golay'
    for player in player_ids: # cycle through players individually
        # difference player positions in timestep dt to get unsmoothed estimate of velicity
        vx = team[player+"_x"].diff() / dt
        vy = team[player+"_y"].diff() / dt

        if maxspeed>0:
            # remove unsmoothed data points that exceed the maximum speed (these are most likely position errors)
            raw_speed = np.sqrt( vx**2 + vy**2 )
            vx[ raw_speed>maxspeed ] = np.nan
            vy[ raw_speed>maxspeed ] = np.nan

        if smoothing:
            if filter_=='Savitzky-Golay':
                # calculate velocity
                vx = signal.savgol_filter(vx,window_length=7,polyorder=1)
                vy = signal.savgol_filter(vy,window_length=7,polyorder=1)        

            elif filter_=='moving average':
                ma_window = np.ones( window ) / window 
                # calculate velocity
                vx = np.convolve( vx , ma_window, mode='same' ) 
                vy = np.convolve( vy , ma_window, mode='same' )      


        # put player speed in x,y direction, and total speed back in the data frame
        team[player + "_vx"] = vx
        team[player + "_vy"] = vy
        team[player + "_speed"] = np.sqrt( vx**2 + vy**2 )

    return team


class player(object):
    """
    player() class
    
    Class defining a player object that stores position, velocity, time-to-intercept and pitch control contributions for a player
    
    __init__ Parameters
    -----------
    pid: id (jersey number) of player
    team: row of tracking data for team
    teamname: team name "Home" or "Away"
    params: Dictionary of model parameters (default model parameters can be generated using default_model_params() )
    
    methods include:
    -----------
    simple_time_to_intercept(r_final): time take for player to get to target position (r_final) given current position
    probability_intercept_ball(T): probability player will have controlled ball at time T given their expected time_to_intercept
    
    """
    # player object holds position, velocity, time-to-intercept and pitch control contributions for each player
    def __init__(self,pid,team,teamname,params):
        self.id = pid
        self.teamname = teamname
        self.playername = "%s_%s_" % (teamname,pid)
        self.vmax = params['max_player_speed'] # player max speed in m/s. Could be individualised
        self.reaction_time = params['reaction_time'] # player reaction time in 's'. Could be individualised
        self.tti_sigma = params['tti_sigma'] # standard deviation of sigmoid function (see Eq 4 in Spearman, 2018)
        self.get_position(team)
        self.get_velocity(team)
        self.PPCF = 0. # initialise this for later
        
    def get_position(self,team):
        self.position = np.array( [ team[self.playername+'x'], team[self.playername+'y'] ] )
        self.inframe = not np.any( np.isnan(self.position) )
        
    def get_velocity(self,team):
        self.velocity = np.array( [ team[self.playername+'vx'], team[self.playername+'vy'] ] )
        if np.any( np.isnan(self.velocity) ):
            self.velocity = np.array([0.,0.])
    
    def simple_time_to_intercept(self, r_final):
        self.PPCF = 0. # initialise this for later
        # Time to intercept assumes that the player continues moving at current velocity for 'reaction_time' seconds
        # and then runs at full speed to the target position.
        r_reaction = self.position + self.velocity*self.reaction_time
        self.time_to_intercept = self.reaction_time + np.linalg.norm(r_final-r_reaction)/self.vmax
        return self.time_to_intercept

    def probability_intercept_ball(self,T):
        # probability of a player arriving at target location at time 'T' given their expected time_to_intercept (time of arrival), as described in Spearman 2018
        f = 1/(1. + np.exp( -np.pi/np.sqrt(3.0)/self.tti_sigma * (T-self.time_to_intercept) ) )
        return f

def lastrow_initialise_players(team,teamname,params):
    """
    initialise_players(team,teamname,params)
    
    create a list of player objects that holds their positions and velocities from the tracking data dataframe 
    
    Parameters
    -----------
    
    team: row (i.e. instant) of either the home or away team tracking Dataframe
    teamname: team name "Home" or "Away"
    params: Dictionary of model parameters (default model parameters can be generated using default_model_params() )
        
    Returns
    -----------
    
    team_players: list of player objects for the team at at given instant
    
    """    
    # get player  ids
    player_ids = np.unique( [ c.split('_')[1] for c in team.keys() if c[:3] == teamname[:3] ] )
    # create list
    team_players = []
    for p in player_ids:
        # create a player object for player_id 'p'
        team_player = player(p,team,teamname,params)
        if team_player.inframe:
            team_players.append(team_player)
    return team_players






def plot_surface_for_event( event_id, events,  data_attack, data_defence, surface, xgrid, ygrid, alpha = 0.7, include_player_velocities=True, annotate=False, field_dimen = (106.0,68),cmap='bwr'):
    """ plot_pitchcontrol_for_event( event_id, events,  tracking_home, tracking_away, PPCF, xgrid, ygrid )
    
    Plots the pitch control surface at the instant of the event given by the event_id. Player and ball positions are overlaid.
    
    Parameters
    -----------
        event_id: Index (not row) of the event that describes the instant at which the pitch control surface should be calculated
        events: Dataframe containing the event data
        tracking_home: (entire) tracking DataFrame for the Home team
        tracking_away: (entire) tracking DataFrame for the Away team
        surface: Pitch surface (dimen (n_grid_cells_x,n_grid_cells_y) ) containing probability for the attcking team (as returned by the generate_xxx_for_event)
        xgrid: Positions of the pixels in the x-direction (field length) as returned by the generate_pitch_control_for_event in Metrica_PitchControl
        ygrid: Positions of the pixels in the y-direction (field width) as returned by the generate_pitch_control_for_event in Metrica_PitchControl
        alpha: alpha (transparency) of player markers. Default is 0.7
        include_player_velocities: Boolean variable that determines whether player velocities are also plotted (as quivers). Default is False
        annotate: Boolean variable that determines with player jersey numbers are added to the plot (default is False)
        field_dimen: tuple containing the length and width of the pitch in meters. Default is (106,68)
        
    Returrns
    -----------
       fig,ax : figure and aixs objects (so that other data can be plotted onto the pitch)

    """    

    play = event_id[0]
    frame = event_id[1]
    
    # pick a pass at which to generate the pitch control surface
    pass_frame = events.loc[event_id]['Start Frame']
    
    # plot frame and event
    fig,ax = mviz.plot_pitch(field_color='white', field_dimen = field_dimen)
    mviz.plot_frame( data_attack.loc[(play,pass_frame)], data_defence.loc[(play,pass_frame)], figax=(fig,ax), PlayerAlpha=alpha, include_player_velocities=True, annotate=annotate)
    mviz.plot_events( events.loc[[(play,frame)]], figax = (fig,ax), indicators = ['Marker','Arrow'], annotate=annotate, color= 'k', alpha=1 )

    # plot pitch control surface
    cmap = cmap
    vmax = surface.max()
    ax.imshow(np.flipud(surface), extent=(np.amin(xgrid), np.amax(xgrid), np.amin(ygrid), np.amax(ygrid)),interpolation='hanning',vmin=0.0,vmax=vmax,cmap=cmap,alpha=0.5)
    
    return fig,ax


def lastrow_generate_pitch_control_for_event(play, event_frame, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50):
    
    import Metrica_PitchControl as mpc
    
    """ generate_pitch_control_for_event
    
    Evaluates pitch control surface over the entire field at the moment of the given event (determined by the index of the event passed as an input)
    
    Parameters
    -----------
        event_id: Index (not row) of the event that describes the instant at which the pitch control surface should be calculated
        events: Dataframe containing the event data
        tracking_home: tracking DataFrame for the Home team
        tracking_away: tracking DataFrame for the Away team
        params: Dictionary of model parameters (default model parameters can be generated using default_model_params() )
        field_dimen: tuple containing the length and width of the pitch in meters. Default is (106,68)
        n_grid_cells_x: Number of pixels in the grid (in the x-direction) that covers the surface. Default is 50.
                        n_grid_cells_y will be calculated based on n_grid_cells_x and the field dimensions
        
    Returrns
    -----------
        PPCFa: Pitch control surface (dimen (n_grid_cells_x,n_grid_cells_y) ) containing pitch control probability for the attcking team.
               Surface for the defending team is just 1-PPCFa.
        xgrid: Positions of the pixels in the x-direction (field length)
        ygrid: Positions of the pixels in the y-direction (field width)
    """
    # get the details of the event (frame, team in possession, ball_start_position)
    #play = event_id[0]
    #event_frame = event_id[1]
    event_frame = int(event_frame)
    tracking_frame = events.loc[(play,int(event_frame))]['Start Frame']
    ball_start_pos = np.array([events.loc[(play,event_frame)]['Start X'],events.loc[(play,event_frame)]['Start Y']])
    # break the pitch down into a grid
    n_grid_cells_y = int(n_grid_cells_x*field_dimen[1]/field_dimen[0])
    xgrid = np.linspace( -field_dimen[0]/2., field_dimen[0]/2., n_grid_cells_x)
    ygrid = np.linspace( -field_dimen[1]/2., field_dimen[1]/2., n_grid_cells_y )
    # initialise pitch control grids for attacking and defending teams 
    PPCFa = np.zeros( shape = (len(ygrid), len(xgrid)) )
    PPCFd = np.zeros( shape = (len(ygrid), len(xgrid)) )
    
    # initialise player positions and velocities for pitch control calc (so that we're not repeating this at each grid cell position)
    attacking_players = lastrow_initialise_players(tracking_home.loc[(play,tracking_frame)],'attack',params)
    defending_players = lastrow_initialise_players(tracking_away.loc[(play,tracking_frame)],'defense',params)
    
    # calculate pitch pitch control model at each location on the pitch
    for i in range( len(ygrid) ):
        for j in range( len(xgrid) ):
            target_position = np.array( [xgrid[j], ygrid[i]] )
            PPCFa[i,j],PPCFd[i,j] = mpc.calculate_pitch_control_at_target(target_position, attacking_players, defending_players, ball_start_pos, params)
    # check probabilitiy sums within convergence
    checksum = np.sum( PPCFa + PPCFd ) / float(n_grid_cells_y*n_grid_cells_x ) 
    assert 1-checksum < params['model_converge_tol'], "Checksum failed: %1.3f" % (1-checksum)
    return PPCFa,xgrid,ygrid



def generate_relevance_at_event(play, event_frame, events, PPCF, params, lower_time_param = 0.3,upper_time_param=1.5, field_dimen = (106.,68.,),n_grid_cells_x = 50):
    
    event_frame = int(event_frame)
    n_grid_cells_y = int(n_grid_cells_x*field_dimen[1]/field_dimen[0])
    xgrid = np.linspace( -field_dimen[0]/2., field_dimen[0]/2., n_grid_cells_x)
    ygrid = np.linspace( -field_dimen[1]/2., field_dimen[1]/2., n_grid_cells_y )
    ball_start_pos = np.array([events.loc[(play,event_frame)]['Start X'],events.loc[(play,event_frame)]['Start Y']])
    
    # initialise relevance grid 
    relevance = np.zeros( shape = (len(ygrid), len(xgrid)) )

    # for each grid on pitch - add in how quickly the ball can get there
    for i in range( len(ygrid) ):
         for j in range( len(xgrid) ):
            target_position = np.array( [xgrid[j], ygrid[i]] )
            ball_travel_time = np.linalg.norm( target_position - ball_start_pos )/params['average_ball_speed']
            if (ball_travel_time < 2.5):
                # Normally distributed inverse ball travel time
                normal_transition_prob = scipy.stats.norm(0, 14).sf(ball_travel_time)
                relevance[i,j] = PPCF[i,j]*normal_transition_prob
            else:
                relevance[i,j] = 0
    
    # normalise between 0 and 1
    norm_relevance = (relevance-relevance.min())/(relevance.max() - relevance.min())

    return norm_relevance

def generate_scoring_opportunity(field_dimen = (106.,68.,), n_grid_cells_x = 50):
    
    import scipy
    
    field_dimen = (106.,68.,)
    n_grid_cells_x = 50
    n_grid_cells_y = int(n_grid_cells_x*field_dimen[1]/field_dimen[0])
    xgrid = np.linspace( -field_dimen[0]/2., field_dimen[0]/2., n_grid_cells_x)
    ygrid = np.linspace( -field_dimen[1]/2., field_dimen[1]/2., n_grid_cells_y )

    scoring_prob = np.zeros( shape = (len(ygrid), len(xgrid)) )
    
    # Use distance to goal as parameter
    goal_centre = np.array( [-53, 0] )

    # for each grid on pitch 
    for i in range( len(ygrid) ):
        for j in range( len(xgrid) ):
            target_position = np.array( [xgrid[j], ygrid[i]] )
            dist_to_goal = np.linalg.norm( target_position - goal_centre )
            scoring_prob[i,j] = (scipy.stats.norm(0, 1).cdf(1/dist_to_goal)-0.5)/0.5
    
    return scoring_prob

def generate_pitch_value(PPCF,PT,PS,field_dimen = (106.,68.,), n_grid_cells_x = 50):
    
    n_grid_cells_y = int(n_grid_cells_x*field_dimen[1]/field_dimen[0])
    xgrid = np.linspace( -field_dimen[0]/2., field_dimen[0]/2., n_grid_cells_x)
    ygrid = np.linspace( -field_dimen[1]/2., field_dimen[1]/2., n_grid_cells_y )

    # initialise relevant pitch control grid
    pitch_value = np.zeros( shape = (len(ygrid), len(xgrid)) )

    # for each grid on pitch - combine Pitch Control x Relevance
    for i in range( len(ygrid) ):
            for j in range( len(xgrid) ):
                pitch_value[i,j] = PPCF[i,j]*PT[i,j]*PS[i,j]

    # normalise
    #pitch_value = (pitch_value - pitch_value.min())/(pitch_value.max() - pitch_value.min())
    
    return pitch_value

def get_location(subject, play, play_frame, event_data, tracking_data, time = 'Start'):
    
    event_frame = event_data.loc[[(play,int(play_frame))]]
    tracking_frame = event_frame[time+' Frame'][0]
    tracking_freeze_frame = tracking_data.loc[(play,tracking_frame)]
    x, y = tracking_freeze_frame[subject+'_x'], tracking_freeze_frame[subject+'_y']
    return x, y

def tracking_to_grid(track_x, track_y, xgrid, ygrid):
    xloc = 0
    for x in range(0,len(xgrid)):
        if track_x < xgrid[x]:
            xloc = x-1
            #print(xloc)
            break
    yloc = 0
    for y in range(0,len(ygrid)):
        if track_y < ygrid[y]:
            yloc = y-1
            #print(yloc)
            break
    return yloc,xloc


def generate_relative_pitch_value(play, play_frame, event_data, tracking_data, pitch_value, xgrid, ygrid):
    
    # Get current location
    ball_start_x, ball_start_y = get_location('ball', play, int(play_frame), event_data, tracking_data, 'Start')
    
    # Convert from x,y metres to pitch value grid
    ystartloc,xstartloc = tracking_to_grid(ball_start_x,ball_start_y, xgrid, ygrid)
    
    # Get pitch value at current location
    start_pv = pitch_value[(ystartloc,xstartloc)]
    
    # Normalise by current pitch value
    relative_pitch_value = (pitch_value - start_pv) / start_pv
    
    return relative_pitch_value

