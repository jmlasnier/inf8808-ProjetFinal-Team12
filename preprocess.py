import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def prep_scatter_df():
    df = pd.read_csv('Recension_bareme_finale2.csv')
    df = df[['year', 'combineRevenuMoinsAjuste', 'combineTaux']]
    return df

def prep_data_bar(revenu,annee1,annee2):
    fileName = 'Recension_bareme_finale2.csv'
    proc_data = convert_data_bar(fileName)
    data = select_year_bar(proc_data,annee1,annee2,revenu)
    return data

  
def select_year_bar(df,year1,year2,revenu):
    print('revenus')
    print(revenu)
    mask1 = df['year']==year1
    mask2 = df['year']==year2
    df1 = df.loc[mask1]
    df2 = df.loc[mask2]
    mask3 = (df1['combineRevenuMoins']<revenu)&(df1['combineRevenuPlus']>=revenu)
    mask4 = (df2['combineRevenuMoins']<revenu)&(df2['combineRevenuPlus']>=revenu)
    dff1 = df1.loc[mask3]
    dff2 = df2.loc[mask4]
    inflation2=dff2['inflation'].tolist()[0]
    inflation1=dff1['inflation'].tolist()[0]
    combineRevenuPlus2 = dff2['combineRevenuMoins'].tolist()[0]
    combineTaux2 = dff2['combineTaux'].tolist()[0]
    montantImpot2 = dff2['montantImpot'].tolist()[0]
    revenu2 = (revenu*inflation1)/inflation2
    dff3=df1.loc[(df1['combineRevenuMoins']<revenu2)&(df1['combineRevenuPlus']>=revenu2)]
    combineRevenuPlus1 = dff3['combineRevenuMoins'].tolist()[0]
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

def convert_data_bar(fileName):
    df = pd.read_csv(fileName)
    df.replace(np.nan,np.inf,inplace=True)
    return df.drop(columns=['combineRevenuMoinsAjuste','combineRevenuPlusAjuste'])
