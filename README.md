# Upepo

Video demo: https://youtu.be/Fk0NxxyzBb4

## Disctinctiveness and Complexity
Upepo is a custom web application that can fetch wind data about any location and perform calculations to produce a 10-minute mean wind speed. Meteorological data is usually scarce and not of robust quality in my country Kenya. As a civil engineer, this poses a challenge since you require reliable data particularly on wind speeds to peform calculations on lateral forces your structure might encounter during its design working life.

The wind speed data that is available in Kenya only covers a few locations and is a maximum 3-second wind gust. The maximum 3-second wind gust was applicable for design according to the obsolete standard CP3-Chapter V-2:1972. The new design standards in Kenya are an adaptation of the newer Eurocodes, KS EN 1991-1-4:2005. However, the new design standards utilise a 10-minute mean wind speed for obtaining wind loads hence this poses a challenge.

A number of scientific procedures are used to convert wind speeds across different duration periods. For this project, the Durst Curve was used to convert a maximum 3-second wind gust to a 10-minute mean wind speed which can then be used to determine wind loads on a structure. The Durst Curve is a statistical correlation between wind speeds over different wind speed durations.
  
The application queries a weather API for maximum wind gusts of a particular location each month for the last 10 years from the time of query. A maximum value is obtained from this dataset and a cumulative probability function ran on the dataset to obtain the risk of annual exceedence. The designer can thus obtain a reliable 10-minute mean wind speed after computation as well as the risk of annual exceedence to ensure that the wind load obtained would not be exceeded within the design working life of the structure.

The web application also includes functionality for commenting and liking comments so as to gauge feedback from users.

## Description
Upepo is a web application that obtains wind speeds for any location on a map and produces a basic 10-minute wind speed for use in structural design.

[Maps JavaScript API](https://developers.google.com/maps/documentation/javascript) from Google is used to build an interactive, dynamic map for the user to interact with. [Places API](https://developers.google.com/maps/documentation/javascript/places) from Google is used to enable search, provide autocomplete and geocoding functionality that transforms the location to latitude and longitude coordinates which are then posted to the server for processing. 

The server queries [Open-Meteo API](https://open-meteo.com/) for maximum wind gust data over the last 10 years which is then processed to a basic 10-minute mean wind speed for the user. Annual risk of exceedence is also calculated from this data and presented to the user.
The application contains the following:
- views.py - Contains view functions that render various html pages, perform registration, login and logout, perform analysis on data, process user comments, and provides an API for performing dynamic like functionality on comments.
- models.py - Contains models for user, likes and comments.
-  urls.py - Contains urls for the different view functions in views.py.
- static folder
    - images - Folder containing background image for the website.
    - map.js - JavaScript file containing code used to render the map, provide autocomplete and geocoding functionality through APIs, and functionality for performing likes, clearing input fields and commenting.
    - styles.css - Contains styling for the application's HTML pages.
- templates folder
    - login.html - Contains a form for logging an existing user in and a link to perform registration.
    - register.html - Contains a form for registering a new user.
    - layout.html - Contains the base layout for multiple templates.
    - index.html - Contains the default landing page that directs a user to either log in or perform analysis.
    - docs.html - Contains some technical documentation on the analysis.
    - contacts.html - Contains contact information.
    - map.html - Contains the map provided by Google to enable location search.
    - analyze.html - Contains analysis output and comments section for user feedback.


## Getting Started
Upepo is a web application that is accessed through its URL.


