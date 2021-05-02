# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

import preprocess
import draw_charts as draw

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#To run server
#From same folder as server.py
# 1: py -m virtualenv -p python3.8 venv
# 2: source venv/Scripts/activate
# 3: py -m pip install -r requirements.txt
# 4: py server.py

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Projet Team12 INF8808'
server = app.server
colors = {
    'background': '#111111',
    'text': '#000000'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )

dfScat = preprocess.prep_scatter_df()
figScat = draw.highlight_scat(dfScat, 2020, 2000)

dfBar = preprocess.prep_data_bar(50000, 2020, 2000)
figBar = draw.draw_bar(dfBar, 2020, 2000)

app.layout = html.Div(style={'font-family':'georgia'}, children=[
    html.H1(
        children='Les impôts au Québec',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-family':'georgia'
        }
    ),

    html.Div(children=[
        html.P('''Nous vous présentons un calculateur d’impôt historique permettant de comprendre et comparer l’évolution de l’impôt Québécois dans le temps. 
                        Entrer dans la 1ère boîte le revenu que vous voulez comparer, dans la 2e l’année où vous avez gagné ce revenu et dans la 3e l’année de comparaison. 
                        Le taux d’inflation de la deuxième année sera appliqué au revenu afin de pouvoir comparer les sommes entre elles. '''),
        html.P('''Le deuxième tableau affiche toutes les années d’impositions. Vous pouvez glisser votre souris sur les petites barres horizontales 
                    afin de connaître le revenu de chaque paliers et le taux d’imposition marginal pour chaque année.'''),
        html.P('''Vous pouvez entrer n'importequelle année entre 1929 et 2020''')
    ], style={
        'textAlign': 'center',
        'color': colors['text'],
        'width':'80%','margin':'auto', 'padding':'10px', 'text-align':'justify',
        'border': '4px solid grey', 'border-radius':'15px'
    }),

    html.Div([
            html.Center(html.Div([
                html.H3('Inputs', style={'textAlign': 'center','color': colors['text']}),
                html.Div([
                    html.Label('Vous avez gagné un revenus de :'),
                    dcc.Input(id='revenus', placeholder='Revenus', type='number', value=50000 ,min=192, required=True, style={'width':'90%'})
                    ]),
                html.Br(),
                html.Center(),
                html.Div([
                    html.Label('à l\'année : '),
                    dcc.Input(id='annee1', placeholder='1929 à 2020', type='number',
                                   value='', max=2020, min=1929, required=True, style={'width':'90%'})]),
                html.Br(),
                html.Div([
                    html.Label('Combien auriez vous payé d\'impôt à l\'année: '),
                    dcc.Input(id='annee2', placeholder='1929 à 2020', type='number', 
                                   value='', required=True, max=2020, min=1929, style={'width':'90%'})]),
                html.Br(),
                html.Button('Calculer', id='button', n_clicks=0),
            ],style={'width':'15%', 'height':'470px','float':'left', 'border': '4px solid grey', 'border-radius':'15px'}, className="six columns")),
            html.Div([
                html.H3('', id='vis1', style={ 'textAlign': 'center', 'color': colors['text'] }),
                dcc.Graph(id='barChart', figure=figBar)
            ],style={'width':'80%', 'height':'470px','float':'left', 'border': '4px solid grey', 'border-radius':'15px'}, className="six columns"),
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
    print(revenus)
    if revenus == None:
        revenus = 0
    if (annee1 == '') or (annee2==''):
        annee1 = 2000
        annee2 = 2020
        return None,barFig, scatterFig
    y1 = int(annee1)
    annee1 = int(annee2)
    annee2 = y1

    ctx = dash.callback_context
    

    figScatter = scatterFig

    if ctx.triggered:
        
        figScatter = draw.highlight_scat(dfScat,annee1, annee2)
        dfBar = preprocess.prep_data_bar(revenus, annee1, annee2)
        figBar = draw.draw_bar(dfBar, annee1, annee2)

        return 'Revenus: {}$'.format(revenus),figBar, figScatter
    
    figBar = barFig
    return 'Revenus: {}$'.format(revenus),figBar, figScatter

if __name__ == '__main__':
    app.run_server(debug=True)