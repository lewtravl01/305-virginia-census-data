import dash
from dash import dcc, html
import plotly as py
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import os

# Read in the USA counties shape files
from urllib.request import urlopen
#import json
#with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#    counties = json.load(response)

########### Define a few variables ######

tabtitle = 'Virginia Counties'
sourceurl = 'https://www.kaggle.com/muonneutrino/us-census-demographic-data'
githublink = 'https://github.com/austinlasseter/dash-virginia-counties'
varlist=['AK', 'AR', 'AZ', 'CA']

counties = pd.read_csv('https://raw.githubusercontent.com/austinlasseter/dash-virginia-counties/master/resources/acs2017_county_data.csv')
usda=pd.read_excel('https://github.com/austinlasseter/dash-virginia-counties/raw/master/resources/ruralurbancodes2013.xls')

fulldf=pd.merge(counties, usda, left_on='CountyId', right_on='FIPS', how='left')
statedf = fulldf.groupby(['State_y', 'State_x'])[['TotalPop']].mean().reset_index()

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
    html.H1('Virginia Census Data 2017'),
    # Dropdowns
    html.Div(children=[
        # left side
        html.Div([
                html.H6('Select a state:'),
                dcc.Dropdown(
                    id='stats-drop',
                    options=[{'label': i, 'value': i} for i in varlist],
                    value='CA'
                ),
        ], className='three columns'),
        # right side
        html.Div([
            dcc.Graph(id='va-map')
        ], className='nine columns'),
    ], className='twelve columns'),

    # Footer
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

############ Callbacks
@app.callback(Output('va-map', 'figure'),
              [Input('stats-drop', 'value')])
def display_results(statecode):
    #valmin=df[selected_value].min()
    #valmax=df[selected_value].max()
    
    singlestatedf = statedf[statedf['State_y'] == statecode]

    data = [dict(type='choropleth', 
        colorscale='Blues', 
        z=singlestatedf['TotalPop'], 
        locations=singlestatedf['State_y'], 
        locationmode='USA-states', 
        text = singlestatedf['State_y'], 
        colorbar=dict(title="Millions"))]
    
    layout = dict(title='Total Population', 
                  geo = dict(scope='usa', projection=dict(type='albers usa'), showlakes = True, lakecolor = 'rgb(66,165,245)'))
    
    fig = go.Figure(data=data, layout=layout)
    
    # fig = go.Figure(go.Choroplethmapbox(geojson=counties,
    #                                 locations=df['FIPS'],
    #                                 z=df[selected_value],
    #                                 colorscale='Blues',
    #                                 text=df['County'],
    #                                 zmin=valmin,
    #                                 zmax=valmax,
    #                                 marker_line_width=0))
    
    # fig.update_layout(mapbox_style="carto-positron",
    #                   mapbox_zoom=5.8,
    #                   mapbox_center = {"lat": 38.0293, "lon": -79.4428})
    
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# https://community.plot.ly/t/what-colorscales-are-available-in-plotly-and-which-are-the-default/2079
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
