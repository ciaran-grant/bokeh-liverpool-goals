# bokeh-liverpool-goals

This is a bokeh dashboard using [@lastrowview](https://twitter.com/lastrowview)'s tracking data for several Liverpool goals.
The data can be found on their GitHub page here: 
[https://github.com/Friends-of-Tracking-Data-FoTD/Last-Row]

The Friends of Tracking tutorials and videos helped set up the majority of the functions and background.
Especially Laurie's [@EightyFivePoint](https://twitter.com/EightyFivePoint) Metrica data lessons: 
[https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking]

Initail plots for the pitch came in handy from [@danzn1](https://twitter.com/danzn1) here: 
[https://github.com/znstrider/PyFootballPitch]

The dashboard makes use of bokeh's server. To run the app, download the `bokeh-app` folder to your cd and using command line enter:
  ```
  bokeh serve --show bokeh-app
  ```
1. bokeh serve - this opens a server connection
2. --show - this opens the app in a browser
3. bokeh-app - this is the name of the folder which contains main.py (where the magic happens)

Have attempted to host this app on its own URL via binder and heroku, however just seem to get a white screen. If anyone has any advice please let me know!
Until then, downloading bokeh-app and running from your own command line is necessary to get the full benefits of the bokeh server.

Here's my binder attempt if interested:
[https://github.com/ciaran-grant/bokeh-binder]


## Preview:

### Tab1: Event and Tracking Overview

<img src="goals-overview.PNG" align="center">

### Tab2: Calculating Pitch Value

<img src="pitch-value.PNG" align="center">

### Tab3: Updating Pitch Value from Player Displacement

<img src="player-displacement.PNG" align="center">




