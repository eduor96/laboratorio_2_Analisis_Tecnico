# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""


import pandas as pd
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import plotly as py
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
#%%
def date_range(start_date, end_date, increment, period):
    result = []
    nxt = start_date
    delta = relativedelta(**{period:increment})
    while nxt <= end_date:
        result.append(nxt)
        nxt += delta
    return result
start_date = datetime(2016, 4, 1)
end_date = datetime(2019, 4, 1)
fechas = date_range(start_date, end_date, 5, 'minutes')
def ag_car(cadena):
    nueva=cadena[0:10]+"T"+cadena[11:-1]+"Z"
    return nueva
def rsi_fun(prices,ind,n):
    gains=[]
    losses=[]
    ind=ind-(n)
    for i in range(n) :
        dife=prices[ind+1]-prices[ind]
        if dife>=0:
            gains.append(dife)
        else:
            losses.append(dife*-1)
        ind=ind+1
    gains=np.array(gains)
    losses=np.array(losses)
    rsi=100-(100/(1+((gains.sum()/14)/(losses.sum()/14))))
    return rsi


#%%
A1_OA_Da = 17                     # Day Align
A1_OA_Ta = "America/Mexico_City"  # Time Align

A1_OA_Ai = "101-004-2221697-001"  # Id de cuenta
A1_OA_At = "practice"             # Tipo de cuenta

A1_OA_In = "USD_MXN"              # Instrumento
A1_OA_Gn = "M5"                   # Granularidad de velas

A1_OA_Ak = "a1a2738e43e01183e07cbb8dec8e2ca4-771e2b55a25bd1f6cb73b42ca4b1f432"


F1=ag_car(str(fechas[0]))
F2=ag_car(str(fechas[5000]))

# =============================================================================
# Inicializar API de Oanda
# =============================================================================


api = API(access_token=A1_OA_Ak)
lista = []
n=5000
while pd.to_datetime(F2)<fechas[-1]:
    params = {"granularity": A1_OA_Gn, "price": "M", "dailyAlignment": A1_OA_Da,
              "alignmentTimezone": A1_OA_Ta, "from": F1, "to": F2}
    A1_Req1 = instruments.InstrumentsCandles(instrument=A1_OA_In, params=params)
    A1_Hist = api.request(A1_Req1)
    
    for i in range(len(A1_Hist['candles'])-1):

            lista.append({'TimeStamp': A1_Hist['candles'][i]['time'],
                          'Open': A1_Hist['candles'][i]['mid']['o'],
                          'High': A1_Hist['candles'][i]['mid']['h'],
                          'Low': A1_Hist['candles'][i]['mid']['l'],
                          'Close': A1_Hist['candles'][i]['mid']['c']})
            
    F1=ag_car(str(fechas[n+1]))
    n=n+5000
    try:F2=ag_car(str(fechas[n]))
    except IndexError:
        break
    
df1_precios = pd.DataFrame(lista)
df1_precios = df1_precios[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
df1_precios['TimeStamp'] = pd.to_datetime(df1_precios['TimeStamp'])
#%%
n=len(df1_precios)
data=np.empty((n,8))
df2_operaciones=pd.DataFrame(data,columns=['Fecha','Folio','Operacion',
                             'Unidades','Margen','Comentario','Precio_Apertura',
                             'Precio_Cierre']).replace(0,"")
df2_operaciones['Fecha']=df1_precios.iloc[:,0]

data=np.empty((n,6))
df3_cuenta=pd.DataFrame(data,columns=['Fecha','Capital','Flotante',
                             'Balance','Rendimiento','Comentario']).replace(0,"")
df3_cuenta['Fecha']=df1_precios.iloc[:,0]
capital=100000
cambios