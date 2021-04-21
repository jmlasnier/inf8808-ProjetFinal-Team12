
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def prepScatterDf():
    df = pd.read_csv('Recension_bareme_finale2.csv')
    df = df[['year', 'combineRevenuMoins', 'combineTaux']]
    return df

def drawScatter(dfScat, year1, year2):
    print(dfScat)
    dfScat1 = dfScat.drop(dfScat[(dfScat.year == year1) | (dfScat.year == year2)].index)
    dfScat1["combineTaux"] = 100*dfScat1["combineTaux"].round(2)
    dfScat1["combineTaux"] = dfScat1["combineTaux"].round(2)
    fig = px.scatter(dfScat1, 
                    x="year", 
                    y="combineRevenuMoins", 
                    title='Paliers d\'impots Canadiens de 1928 à 2020 en dollars courant',
                    color_discrete_sequence=['grey'],
                    height=800,
                    custom_data= ['combineTaux'])
    fig.update_traces(
        marker_symbol="line-ew-open",
        hovertemplate = '''Année: %{x}<br>Palier: %{y}<br>Taux d'imposition: %{customdata}%<br><extra></extra>'''
        )
    fig.update_layout(
        yaxis_title="Revenus",
        xaxis_title="Année",
        
    )

    return fig

def highlightScat(df, annee1, annee2):
    dfScat = df.loc[(df['year'] == annee1) | (df['year'] == annee2)]
    fig2 = px.scatter(dfScat, x="year", y="combineRevenuMoins", 
                    color_discrete_sequence=['red'])
    fig2.update_traces(marker_line_width=3)
    fig = drawScatter(df, annee1, annee2)
    if len(fig2.data)!=0:
        fig.add_trace(fig2.data[0])
    fig.update_traces(marker_symbol="line-ew-open")
# else:
    fig = drawScatter(df, annee1, annee2)
    return fig
    

def drawBar(data, annee1, annee2):
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
        y = ['Impôts selon les paliers de lautre année  ' ,'Impôts  ','Taux moyen  ','Revenu  '],
        orientation = 'h',
        base = 0,
        customdata = [str(data[0])+'$',str(data[1])+'$',str(data[2])+'%',str(data[3])+'$'],
        texttemplate = "<b>%{customdata}</b>",
        textposition = "outside",
        name = str(annee1)
        ))
    fig.add_trace(go.Bar(
        x = data1[4:8],
        y = ['Impôts selon les paliers de lautre année  ','Impôts  ','Taux moyen  ','Revenu  '],
        orientation = 'h',
        base = 0,
        customdata = [str(data[4])+'$',str(data[5])+'$',str(data[6])+'%',str(data[7])+'$'],
        texttemplate = '<span style="margin-left:auto; margin-right:auto"><b>%{customdata}</b>',
        textposition = "outside",
        hovertemplate = None,
        name = str(annee2)
        ))
    fig.update_layout(
        barmode = 'stack',
        title={'text': str(annee2) +f" vs " + str(annee1),
        'x':0.5,
        'xanchor':'center'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[-150, 150])
    )
    fig.update_xaxes(
        visible = False
    )
    return fig

def prep_data(revenu,annee1,annee2):
    fileName = 'Recension_bareme_finale.csv'
    proc_data = convert_data(fileName)
    data = select_year(proc_data,annee1,annee2,revenu)
    return data
    
def select_year(df,year1,year2,revenu):
    # TODO : Replace players in each act not in the top 5 by a
    # new player 'OTHER' which sums their line count and percentage
    mask1 = df['year']==year1
    mask2 = df['year']==year2
    df1 = df.loc[mask1]
    df2 = df.loc[mask2]
    mask3 = (df1['combineRevenuPlus']<revenu)&(df1['combineRevenuMoins']>=revenu)
    mask4 = (df2['combineRevenuPlus']<revenu)&(df2['combineRevenuMoins']>=revenu)
    dff1 = df1.loc[mask3]
    dff2 = df2.loc[mask4]
    inflation2=dff2['inflation'].tolist()[0]
    inflation1=dff1['inflation'].tolist()[0]
    combineRevenuPlus2 = dff2['combineRevenuPlus'].tolist()[0]
    combineTaux2 = dff2['combineTaux'].tolist()[0]
    montantImpot2 = dff2['montantImpot'].tolist()[0]
    revenu2 = (revenu*inflation1)/inflation2
    dff3=df1.loc[(df1['combineRevenuPlus']<revenu2)&(df1['combineRevenuMoins']>=revenu2)]
    combineRevenuPlus1 = dff3['combineRevenuPlus'].tolist()[0]
    combineTaux1 = dff3['combineTaux'].tolist()[0]
    montantImpot1 = dff3['montantImpot'].tolist()[0]
    impot1 = (revenu2-combineRevenuPlus1)*combineTaux1+montantImpot1
    impot2 = (revenu-combineRevenuPlus2)*combineTaux2+montantImpot2
    d=[ revenu2*impot2/revenu, 
        impot1, 
        impot1*100/revenu2, 
        revenu2, 
        revenu*impot1/revenu2, 
        impot2, 
        impot2*100/revenu, 
        revenu, 
        year1, 
        year2]
    data=[round(num,2) for num in d]
    
    return data

def convert_data(fileName):
    df = pd.read_csv(fileName)
    df.replace(np.nan,np.inf,inplace=True)
    return df.drop(columns=['Unnamed: 6','Unnamed: 7'])

