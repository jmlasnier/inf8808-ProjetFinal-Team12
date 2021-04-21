# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

import testCallback as test

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
colors = {
    'background': '#111111',
    'text': '#000000'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


dfScat = test.prepScatterDf()
figScat = test.drawScatter(dfScat, 1940, 1940)

# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )
dfBar = test.prep_data(50000, 1990, 2000)
figBar = test.drawBar(dfBar, 1990, 2000)

# barChart = test.draw1(0)

app.layout = html.Div(style={'font-family':'georgia'}, children=[
    html.H1(
        children='Les impots au Canada',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-family':'georgia'
        }
    ),

    html.Div(children='Projet Final pour le cours de Visualisation de Données Inf8808', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div([
            html.Center(html.Div([
                html.H3('Inputs', style={'textAlign': 'center','color': colors['text']}),
                html.Div([
                    html.Label('Revenus'),
                    dcc.Input(id='revenus', placeholder='Revenus', type='number', value=50000 ,min=192, required=True)]),
                html.Br(),
                html.Center(),
                html.Div([
                    html.Label('Année initiale'),
                    dcc.Input(id='annee1', placeholder='Entre 1929 et 2020', type='number',
                                   value='', max=2020, min=1929, required=True)]),
                html.Br(),
                html.Div([
                    html.Label('Année de comparaison'),
                    dcc.Input(id='annee2', placeholder='Entre 1929 et 2020', type='number', 
                                   value='', required=True, max=2020, min=1929)]),
                html.Br(),
                html.Br(),
                html.Button('Submit', id='button', n_clicks=0),
            ],style={'width':'20%','float':'left'}, className="six columns")),
            html.Div([
                html.H3('', id='vis1', style={ 'textAlign': 'center', 'color': colors['text'] }),
                dcc.Graph(id='barChart', figure=figBar)
            ],style={'width':'75%','float':'left'}, className="six columns"),
        ],style={'width':'80%','margin':'auto', 'padding':'10px'}, className="row"),
    dcc.Graph(
        id='scatterChart',
        figure=figScat
    )
])


@app.callback(
    Output(component_id='vis1',   component_property='children'),
    Output(component_id='barChart',     component_property='figure'),
    Output(component_id='scatterChart',     component_property='figure'),
    Input( component_id='button', component_property='n_clicks'),
    State( component_id='revenus',component_property='value'),
    State( component_id='annee1', component_property='value'),
    State( component_id='annee2', component_property='value'),
    State( component_id='barChart',component_property='figure'),
    State( component_id='scatterChart',component_property='figure')
    )
def update_year(n_clicks, revenus, annee1, annee2, barFig, scatterFig):
    y1 = annee1
    annee1 = annee2
    annee2 = y1

    ctx = dash.callback_context
    

    figScatter = scatterFig

    if ctx.triggered:
        figScatter = test.highlightScat(dfScat, annee1, annee2)
        dfBar = test.prep_data(revenus, annee1, annee2)
        figBar = test.drawBar(dfBar, annee1, annee2)

        return 'Revenus: {}'.format(revenus),figBar, figScatter
    
    figBar = barFig
    return 'Revenus: {}'.format(revenus),figBar, figScatter

if __name__ == '__main__':
    app.run_server(debug=True)