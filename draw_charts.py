
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

import preprocess


def draw_scatter(dfScat, year1, year2):
    dfScat1 = dfScat.drop(dfScat[(dfScat.year == year1) | (dfScat.year == year2)].index)
    dfScat1["combineTaux"] = 100*dfScat1["combineTaux"].round(2)
    # dfScat1["combineTaux"] = dfScat1["combineTaux"].round(2)
    fig = px.scatter(dfScat1, 
                    x="year", 
                    y="combineRevenuMoinsAjuste", 
                    log_y = True,
                    range_y=[5000, 10000000],
                    title='Paliers d\'impots Québecois de 1929 à 2020 en dollars courant',
                    color_discrete_sequence=['black'],
                    height=800,
                    custom_data= ['combineTaux'])
    fig.update_traces(
        marker_symbol="line-ew-open",
        hovertemplate = '''Année: %{x}<br>Palier: %{y:,}$<br>Taux d'imposition: %{customdata}%<br><extra></extra>'''
        )
    fig.update_layout(
        yaxis_title="Revenus en échelle log ($)",
        xaxis_title="Année",
        
    )
    return fig

def highlight_scat(df, annee1, annee2):
    annee1 = int(annee1)
    annee2 = int(annee2)
    dfScatAnnee1 = df.loc[(df['year'] == annee1)].copy()
    dfScatAnnee1["combineTaux"] = 100*dfScatAnnee1["combineTaux"].round(2)
    figAnnee1 = px.scatter(
                    dfScatAnnee1,
                    x="year",
                    y="combineRevenuMoinsAjuste", 
                    color_discrete_sequence=['blue'],
                    custom_data= ['combineTaux'])
    figAnnee1.update_traces(
        marker_line_width=3, 
        hovertemplate = '''Année: %{x}<br>Palier: %{y:,}$<br>Taux d'imposition: %{customdata}%<br><extra></extra>'''
        )

    dfScatAnnee2 = df.loc[(df['year'] == annee2)].copy()
    dfScatAnnee2["combineTaux"] = 100*dfScatAnnee2["combineTaux"].round(2)
    figAnnee2 = px.scatter(
                    dfScatAnnee2,
                    x="year",
                    y="combineRevenuMoinsAjuste", 
                    color_discrete_sequence=['red'],
                    custom_data= ['combineTaux'])
    figAnnee2.update_traces(
        marker_line_width=3, 
        hovertemplate = '''Année: %{x}<br>Palier: %{y:,}$<br>Taux d'imposition: %{customdata}%<br><extra></extra>'''
        )

    fig = draw_scatter(df, annee1, annee2)
    fig.add_trace(figAnnee1.data[0])
    fig.add_trace(figAnnee2.data[0])
    fig.update_traces(marker_symbol="line-ew-open")
    fig.update_layout(
        font_family="georgia",
        title_font_size=30,
    )
    return fig
    

def draw_bar(data, annee1, annee2):
    fig = go.Figure()  # conversion back to Graph Object
    max1=max(data[0],data[4])
    max2=max(data[1],data[5])
    max3=max(data[2],data[6])
    max4=max(data[3],data[7])

    maximum10 = data[0]*100/max1 if max1!=0 else 0 
    maximum21 = data[1]*100/max2 if max2!=0 else 0 
    maximum32 = data[2]*100/max3 if max3!=0 else 0 
    maximum43 = data[3]*100/max4 if max4!=0 else 0 
    maximum14 = data[4]*100/max1 if max1!=0 else 0 
    maximum25 = data[5]*100/max2 if max2!=0 else 0 
    maximum36 = data[6]*100/max3 if max3!=0 else 0 
    maximum47 = data[7]*100/max4 if max4!=0 else 0 

    data1=[
        maximum10,
        maximum21,
        maximum32,
        maximum43,
        -maximum14,
        -maximum25,
        -maximum36,
        -maximum47]
    
    fig.add_trace(go.Bar(
        x = data1[0:4],
        y = ['Taux échangés*' ,'Impôts  ','Taux moyen  ','Revenu  '],
        orientation = 'h',
        base = 0,
        customdata = ["{:,}".format(data[0]).replace(",", " ").replace(".", ",")+'$',
                      "{:,}".format(data[1]).replace(",", " ").replace(".", ",")+'$',
                      str(data[2]).replace(".", ",")+'%',
                      "{:,}".format(data[3]).replace(",", " ").replace(".", ",")+'$'],
        texttemplate = "<b>%{customdata}</b>",
        textposition = "outside",
        name = str(annee1)
        ))
    fig.add_trace(go.Bar(
        x = data1[4:8],
        y = ['Taux échangés*','Impôts  ','Taux moyen  ','Revenu  '],
        orientation = 'h',
        base = 0,
        customdata = ["{:,}".format(data[4]).replace(",", " ").replace(".", ",")+'$',
                      "{:,}".format(data[5]).replace(",", " ").replace(".", ",")+'$',
                      str(data[6]).replace(".", ",")+'%',
                      "{:,}".format(data[7]).replace(",", " ").replace(".", ",")+'$'],
        texttemplate = '<span style="margin-left:auto; margin-right:auto"><b>%{customdata}</b>',
        textposition = "outside",
        hovertemplate = None,
        name = str(annee2)
        ))
    fig.update_layout(
        barmode = 'stack',
        title={'text': 'Comparaison de l\'année ' + str(annee2) +f" avec " + str(annee1),
        'x':0.5,
        'xanchor':'center'},
        title_font_size=30,
        font_size = 15,
        font_family="georgia",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[-150, 150])
    )
    fig.update_xaxes(
        visible = False
    )
    fig.update_traces(
        hovertemplate= '''<b>%{y}:</b> %{customdata}<br><extra></extra>'''
    )
    return fig
