# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + {"tags": ["to_remove"]}
import numpy as np
import pandas as pd
np.set_printoptions(threshold=20000)
pd.options.display.max_columns = None

from itertools import product

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (30, 15)
import seaborn as sns
#sns.set()
sns.set_style("whitegrid")

import re

import warnings
warnings.filterwarnings('ignore')
# -


# # La importancia de la transparencia 
#
# Una frase que escuchamos mucho es que como ciudadanos tenemos derechos y obligaciones. Entre los derechos bien conocidos están el derecho a la libertad de pensamiento y expresión, derecho a la educación, salud, vivienda, y muchos más. Hoy hablaremos de un derecho que no todos ejercemos, pero cuya popularidad e importancia va al alza: derecho de acceso a la información. La Comisión Nacional de Derechos Humanos establece que "el Estado debe garantizar el derecho de las personas para acceder a la información pública, buscar, obtener y difundir libremente la información...". El acceso a la información es una herramienta para fomentar la transparencia en la gestión pública, y así poder mejorar la calidad de nuestra democracia. El INAI (Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales) es el organismo encargado de que tengamos acceso a la información pública y podamos proteger nuestros datos personales.
#
#
# La idea del INAI (que en otras vidas se llamaba IFAI) surgió desde el primer sexenio de este milenio y ha ido transformándose poco a poco. Con este trabajo buscamos analizar las respuestas e información que brinda el INAI ante las preguntas de los ciudadanos. Comencemos. 
#

# + {"tags": ["to_remove"]}
inai = pd.read_parquet('../data/inai.parquet')

# + {"tags": ["to_remove"]}
for col in ['fecha_solicitud', 'fecha_respuesta', 'fecha_limite']:
    inai[col] = pd.to_datetime(inai[col]).dt.date
    
 #   , format='%d%b%Y:%H:%M:%S.%f'

# + {"tags": ["to_remove"]}
#inai['fecha_solicitud'] = pd.to_datetime(inai['fecha_solicitud'])


inai['year_solicitud'] =  pd.to_datetime(inai['fecha_solicitud']).dt.year
inai['year_respuesta'] =  pd.to_datetime(inai['fecha_respuesta']).dt.year

inai['mes_solicitud'] =  pd.to_datetime(inai['fecha_solicitud']).dt.month
inai['mes_respuesta'] =  pd.to_datetime(inai['fecha_respuesta']).dt.month
# -

# ## Vista rápida de las solicitudes

# Contamos con datos de solicitudes del 1 de enero del 2012 al 30 de junio del 2019. Esto equivale a un total **1'395,851** preguntas. Si asumimos que hay una pregunta por persona, es como si al 1.09% de nuestra población hubiera hecho solicitudes de información.

# + {"tags": ["to_remove"]}
# http://dof.gob.mx/nota_detalle.php?codigo=5436061&fecha=04/05/2016
# -

# Curiosamente, no todas las preguntas fueron realizadas desde México, sino que el estado y municipio reportado por los solicitantes es muy variado. Por ejemplo, incluso hay una solicitud desde Zimbabwe y Mauricio.
#
# Naturalmente, México es el país de 99.44% de las solicitudes, pero también hay solicitudes de los siguientes países: 
#
# + El 0.24% viene de Estados Unidos
#
#
# + El 0.05% viene de Reino Unido 
#
#
# + El 0.05% viene de Canadá
#
#
# + El 0.03% viene de España
#
#
# + El 0.02% viene de Rusia 
#
# Dado que el estado y municipio son reportados por el usuario tenemos solicitudes desde las alcaldías de Ciudad de México hasta "COLEGIO HOGWARTS DE MAGIA Y HECHICERÍA" en el Reino Unido. Claramente, la creatividad de los mexicanos ante un campo de datos abierto no podía faltar. 
#
# Veamos cómo se ve el número de solicitudes por año y mes.
#

# + {"tags": ["to_remove"]}
pais_count = inai.groupby('pais')['folio'].count().reset_index()

pais_count = pais_count.sort_values(by = 'folio', ascending = False)

pais_count ['prop'] = (pais_count.folio / pais_count.folio.sum()) * 100
#pais_count

# + {"tags": ["to_remove"]}
#inai[inai.pais == 'México'].estado.value_counts()

# + {"tags": ["to_remove"]}
# inai[inai.pais != 'México']

# + {"tags": ["to_remove"]}
import plotly.graph_objects as go
import plotly.express as px

# + {"tags": ["to_remove"]}
import plotly.offline as py

# + {"tags": ["to_remove"]}
year_count = inai.groupby('year_solicitud')['folio'].count().reset_index()

fig = go.Figure(
    data=[go.Scatter(y=year_count.folio, line=dict())],
    layout=dict(title=dict(text="Número de solicitudes por año"))
)
fig.update_xaxes(title_text = "Año")

fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = [0, 1, 2, 3, 4, 5, 6, 7],
        ticktext = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
    )
)

fig.update_layout(template="plotly_white")

fig.update_yaxes(title_text = "Número de solicitudes")

fig.show()

#py.iplot([fig])
# -

# El número de solicitudes totales por año fue aumentando poco a poco del 2012 al 2017, año en que alcanzó su punto máximo, y después disminuyó. De hecho los 3 días en que más solicitudes hubo fueron el 8 de febrero 2017, 9 de febrero del 2017 y el 21 de febrero del 2017. Las solicitudes hechas en esos días son de diversos temas, pero un interés recurrente es conocer el sueldo de los funcionarios públicos. 
#
# Para conocer un poco más el detalle del número de solicitudes, ahora vemos cómo se ven las solicitudes por mes y año.

# + {"tags": ["to_remove"]}
fecha_count = inai.groupby('fecha_solicitud')['folio'].count().reset_index()
fecha_count = fecha_count.sort_values(by = 'folio', ascending = False)

# + {"tags": ["to_remove"]}
top_fechas = inai[inai.fecha_solicitud.isin(fecha_count.fecha_solicitud.head(3))]

# top_fechas.sector.value_counts()

# + {"tags": ["to_remove"]}
count = inai.groupby(['year_solicitud', 'mes_solicitud'])['folio'].count().reset_index()
# count.head()

# + {"tags": ["to_remove"]}
# esta es la paleta de colores 
pal = sns.cubehelix_palette(8)
# pal.as_hex()

# + {"tags": ["to_remove"]}
fig = go.Figure(
    data=[go.Scatter(y=count.folio, line=dict())],
    layout=dict(title=dict(text="Número de solicitudes por mes y año"))
)
fig.update_xaxes(title_text = "Mes / Año")

fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = [0,12,24,36,48,60,72, 84],
        ticktext = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
    )
)

fig.update_layout(template="plotly_white")

fig.update_yaxes(title_text = "Número de solicitudes")

fig.show()
# -

# Al analizar el número de solicitudes por mes y año podemos ver un patrón interesante: el número de preguntas baja en los meses finales del año y luego aumenta al inicio del año siguiente. Las combinaciones de mes-año con mayor número de preguntas fueron febrero 2017 y octubre 2018. 
#
# Ya que conocemos cómo ha cambiado el número de solicitudes por mes y año ahora vamos a conocer (a grandes rasgos) los sectores y las dependencias de las que preguntan los solicitantes.

# Una vez que las solicitudes son revisadas se les asigna un sector y una dependencia. En las solicitudes que aquí estudiamos hay 26 sectores distintos y 858 dependencias. El sector con el mayor número de solicitudes es "Aportaciones a Seguridad Social".  

# + {"tags": ["to_remove"]}
# juanito 1

# + {"tags": ["to_remove"]}
count_sector = inai.groupby('sector')['folio'].count().reset_index()
count_sector = count_sector.sort_values(by = 'folio', ascending = False).reset_index()
count_sector['prop'] = (count_sector.folio / count_sector.folio.sum()) * 100
count_sector = count_sector.drop(columns = ['index'])
#count_sector

# + {"tags": ["to_remove"]}
count_sector['sector'] = np.where(count_sector.sector == 'Previsiones y Aportaciones para los Sistemas de Educación Básica, Normal, Tecnológica y de Adultos',
                                 'Previsiones y Aportaciones para los Sistemas de Educación',
                                 count_sector.sector)

# + {"tags": ["to_remove"]}
count_sector.rename(columns = {'folio' : 'solicitudes totales' }, inplace = True)

# + {"tags": ["to_remove"]}
import plotly.express as px
#data = px.data.gapminder()

#data_canada = data[data.country == 'Canada']
fig = px.bar(count_sector, x='prop', y='sector', orientation='h',
             color_continuous_scale=None,
             hover_data=['solicitudes totales'], #color='prop',
             labels={'prop':'Proporción de solicitudes',
                    'sector' : 'Sector'}, width=900
            
            )
fig.update_layout(template="plotly_white")


fig.show()
# -

# Ahora bien, como hay 858 dependencias distintas solo vamos a enseñar aquellas que acumulan el **50%** de las solicitudes. 

# + {"tags": ["to_remove"]}
count_dep = inai.groupby('dependencia')['folio'].count().reset_index()
count_dep = count_dep.sort_values(by = 'folio', ascending = False).reset_index()
count_dep = count_dep.drop(columns = ['index'])
count_dep['prop'] = (count_dep.folio /  count_dep.folio.sum())*100
count_dep['cum_prop'] = count_dep.prop.cumsum()

count_dep_filter = count_dep[count_dep.cum_prop < 51]

# + {"tags": ["to_remove"]}
# juanito 2

# + {"tags": ["to_remove"]}
count_dep_filter.rename(columns = {'folio' : 'solicitudes totales'}, inplace = True)

# + {"tags": ["to_remove"]}
import plotly.express as px
#data = px.data.gapminder()

#data_canada = data[data.country == 'Canada']
fig = px.bar(count_dep_filter, x='prop', y='dependencia', orientation='h',
             color_continuous_scale=None,
             hover_data=['solicitudes totales'], #color='prop',
             labels={'prop':'Proporción de solicitudes',
                    'dependencia' : 'Dependencia'}, width=900
            
            )
fig.update_layout(template="plotly_white")


fig.show()
# -

# Hay 15 dependencias que acumulan el 50% de todas las solicitudes. Las solicitudes de información al IMSS representan el 17.4% de todas las solicitudes. Podemos ver que hay congruencia entre el número de preguntas por sector y dependencia.
#
# Ya que vimos a grandes rasgos de qué sector vienen las solicitudes, vamos a analizar el medio de entrada. 

# + {"tags": ["to_remove"]}
count_medio = inai.groupby('medio_entrada')['folio'].count().reset_index()
count_medio['prop'] = (count_medio.folio / count_medio.folio.sum()) * 100
# count_medio

# + {"tags": ["to_remove"]}
import plotly.express as px
#data = px.data.gapminder()

#data_canada = data[data.country == 'Canada']
fig = px.bar(count_medio, x='medio_entrada', y='prop', #orientation='h',
             color_continuous_scale=None,
             hover_data=['folio'], #color='prop',
             labels={'prop':'Proporción de solicitudes %',
                    'medio_entrada' : 'Medio de Entrada'}, width=900
            
            )
fig.update_layout(template="plotly_white")


fig.show()
# -

# Cerca del 96% de las solicitudes se realizaron por medio electrónico. Aunque no es totalmente sorprendente (dada la burocracia que sigue presente en todos los trámites de gobierno), sí llama la atención que alrededor de 56 mil solicitudes se hicieron por medios manuales. Vamos a conocerlas un poco más. 

# + {"tags": ["to_remove"]}
manuales = inai[inai.medio_entrada == 'Manual']
 

# + {"tags": ["to_remove"]}
manual_dependencia = (
    manuales
    .groupby('dependencia')['folio']
    .count()
    .reset_index()
    .sort_values(by = 'folio', ascending = False) 
).reset_index()

manual_dependencia['prop'] = (manual_dependencia.folio / manual_dependencia.folio.sum()) * 100
manual_dependencia['prop_cum'] = manual_dependencia.prop.cumsum()
#manual_dependencia

# + {"tags": ["to_remove"]}
#manual_dependencia.head(7).dependencia.unique()
# -

# El 50% de las solicitudes manuales corresponden a 7 dependencias: 
#
# 1. Hospital Regional de Alta Especialidad de Ixtapaluca con 12.15% 
#
#
# 2. Instituto Mexicano del Seguro Social con 11.39% 
#
#
# 3. Instituto de Seguridad y Servicios Sociales de los Trabajadores del Estado con 7.32%
#
#
# 4. Instituto Nacional de Ciencias Médicas y Nutrición Salvador Zubirán con 5.34%
#
#
# 5. Procuraduría Federal de la Defensa del Trabajo coon 4.74%
#
#
# 6. Consejo de la Judicatura Federal con 3.91%
#
#
# 7. Suprema Corte de Justicia de la Nación con 3.58%
#
#

# El 99% de las solicitudes tuvieron origen en México, en especial en la Ciudad de México. Analicemos el tipo de solicitud de las consultas hechas a mano: 

# + {"tags": ["to_remove"]}
manual_tipo_sol = (
    manuales
    .groupby('tipo_solicitud')['folio']
    .count()
    .reset_index()
    .sort_values(by = 'folio', ascending = False) 
).reset_index()

manual_tipo_sol['prop'] = (manual_tipo_sol.folio / manual_tipo_sol.folio.sum()) * 100
manual_tipo_sol['prop_cum'] = manual_tipo_sol.prop.cumsum()
# manual_tipo_sol

# + {"tags": ["to_remove"]}
s = inai[inai.dependencia == 'Instituto Mexicano del Seguro Social'].tipo_solicitud.value_counts() / inai[inai.dependencia == 'Instituto Mexicano del Seguro Social'].shape[0]
# s

# + {"tags": ["to_remove"]}
import plotly.express as px

fig = px.bar(manual_tipo_sol, x='tipo_solicitud', y='prop', #orientation='h',
             color_continuous_scale=None,
             hover_data=['folio'], #color='prop',
             labels={'prop':'Proporción de solicitudes manuales %',
                    'tipo_solicitud' : 'Tipo solicitud',
                    'folio' : 'Solicitudes totales'}, width=900
            
            )
fig.update_layout(template="plotly_white")


fig.show()
# -

# De las solicitudes manuales el 51.42% son para solicitar información pública, 45.25% es de datos personales y 3.32% es de corrección de dato personales. Vamos a contrastar esto con las solicitudes realizadas de manera electrónica. 

# + {"tags": ["to_remove"]}
ts = (
    inai[inai.medio_entrada != 'Manual']
    .groupby('tipo_solicitud')['folio']
    .count()
    .reset_index()
    .sort_values(by = 'folio', ascending = False) 
).reset_index()

ts['prop'] = (ts.folio / ts.folio.sum()) * 100
ts['prop_cum'] = ts.prop.cumsum()
#ts

# + {"tags": ["to_remove"]}
import plotly.express as px

fig = px.bar(ts, x='tipo_solicitud', y='prop', #orientation='h',
             color_continuous_scale=None,
             hover_data=['folio'], #color='prop',
             labels={'prop':'Proporción de solicitudes Electrónicas %',
                    'tipo_solicitud' : 'Tipo solicitud',
                    'folio' : 'Solicitudes totales'}, width=900
            
            )
fig.update_layout(template="plotly_white")


fig.show()
# -

# Diferente a lo observado en las solicitudes manuales, el 80.90% de las solicitudes electrónicas son para solicitar información pública, 18.99% son sobre datos personales y 0.09% son para la corrección de datos personales. 
#
# El tipo de solicitud sí cambia según el medio de entrada pues en las consultas manuales hay un mayor balance entre solicitudes de información pública y de datos personales. Además, hay un mayor porcentaje de corrección de datos personales en las solicitudes manuales. 
#
# El medio de **entrega** también cambia según el medio de entrada. 
#

# + {"tags": ["to_remove"]}
count_medio_entrega = inai.groupby(['medio_entrada','medio_entrega'])['folio'].count().reset_index()

count_medio.rename(columns = {'folio':'total'}, inplace = True)

count_medio_entrega = count_medio_entrega.merge(count_medio[['medio_entrada', 'total']])
count_medio_entrega['prop_medio'] = (count_medio_entrega.folio / count_medio_entrega.total) * 100
# count_medio_entrega

# + {"tags": ["to_remove"]}
import plotly.express as px

fig = px.bar(count_medio_entrega, x='medio_entrega', y='prop_medio', facet_col="medio_entrada",
             color_continuous_scale=None,
             hover_data=['folio'], #color='prop',
             labels={'medio_entrada' : 'Medio entrada', 
                 'prop_medio':'Proporción de solicitudes %',
                    'medio_entrega' : 'Medio de entrega',
                    'folio' : 'Solicitudes totales'}, width=900
            
            )
fig.update_layout(template="plotly_white")


fig.show()
# -

# Podemos ver que el medio de entrega más popular en el medio Eléctronico es Entrega por Internet en la "PNT" (Plataforma Nacional de Transparencia), mientras que las solicitudes manuales la entrega más común es "Otro Medio". Aunque no lo podemos apreciar, hubo 709 solicitudes (0.05% de las solicitudes Electrónicas) que se entregaron de forma "Verbal". 
#
# Ya que conocemos la forma en que se entregan las respuestas, hay que conocer cuáles son las respuestas otorgadas por el INAI. 

# ### Medios de entrega a través de los años

# + {"tags": ["to_remove"]}
count_ent_year = (inai
                  .groupby(['year_solicitud', 'medio_entrega'])
                  ['folio']
                  .count()
                  .reset_index()
                 
                 )
#count_ent_year

# + {"tags": ["to_remove"]}
a = inai.groupby('medio_entrega')['folio'].count().reset_index()

b = a.copy() #2012
b['year_solicitud'] = 2012

c = a.copy() #2013
c['year_solicitud'] = 2013

d = a.copy() #2014
d['year_solicitud'] = 2014

e = a.copy() #2015
e['year_solicitud'] = 2015

f = a.copy() #2016
f['year_solicitud'] = 2016

g = a.copy() #2017
g['year_solicitud'] = 2017

h = a.copy() #2018
h['year_solicitud'] = 2018

i = a.copy() #2019
i['year_solicitud'] = 2019

year_entrega = pd.concat([b,c,d,e,f,g,h,i], axis = 0).reset_index()
year_entrega = year_entrega.drop(columns = ['index', 'folio'])
#year_entrega

# + {"tags": ["to_remove"]}
cc = count_ent_year.merge(year_entrega, 
                          on = ['year_solicitud', 'medio_entrega'],
                          how = 'right')
# cc.shape

# + {"tags": ["to_remove"]}
cc = cc.fillna(0)
cc = cc.sort_values(by = ['year_solicitud', 'medio_entrega']).reset_index()
#cc = cc.drop(columns = ['index', 'level_0'])
# cc

# + {"tags": ["to_remove"]}
count_year = inai.groupby('year_solicitud')['folio'].count().reset_index()
count_year.rename(columns = {'folio' : 'total'}, inplace = True)
# count_year

# + {"tags": ["to_remove"]}
count_ent_year = cc.copy()
# count_ent_year.shape

# + {"tags": ["to_remove"]}
count_ent_year = count_ent_year.merge(count_year)
count_ent_year['prop'] = np.round((count_ent_year.folio / count_ent_year.total) * 100, 2)
# count_ent_year

# + {"tags": ["to_remove"]}
count_ent_year.rename(columns = {'year_solicitud' : 'Año',
                                 'medio_entrega' : 'Medio Entrega' }
                     , inplace = True)

# + {"tags": ["to_remove"]}
#count_resp_pivot = count_resp.pivot(index= 'period', 
#                  columns = 'respuesta', values = 'folio')

#count_resp_pivot

# + {"tags": ["to_remove"]}
count_ent_year_pv = count_ent_year.pivot(index = 'Año', columns = 'Medio Entrega',
                                        values = 'prop')
#count_ent_year_pv

# + {"tags": ["to_remove"]}
# juanito 3.1

# + {"tags": ["to_remove"]}
import plotly.express as px
fig = px.line(count_ent_year, x="Año", y="folio", 
              
                 facet_row="Medio Entrega", width=900
            )

fig.update_xaxes(title_text = "Mes - Año")

fig.update_layout(
    yaxis = dict(
        tickmode = 'array',
        tickvals = [0, 50000, 100000, 150000],
        ticktext = ["0", "50,000", "100,000", "150,000"]
    ),
    xaxis = dict(
        tickmode = 'array',
        tickvals = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019] #,
        #ticktext = ["0", "50,000", "100,000", "150,000"]
    ),
    font=dict(
        #family="Courier New, monospace",
        size=7,
        color="#7f7f7f"
    )#,
      #  title={
      #  'text': "Plot Title",
        #'y':0.9,
        #'x':0.5,
      #  'xanchor': 'center',
      #  'yanchor': 'top'}

)

# 0
fig.update_layout(template="plotly_white")

fig.update_yaxes(title_text = "# Solicitudes")

# this works 1 
for annotation in fig.layout.annotations:
    annotation.text = annotation.text.split("=")[1]
    annotation.textangle =  0
    annotation.font=dict(color="black", size=5)
    #annotation.text = ["hi", 'alo']
    #annotation.title_font_size = 1
   


    
    
    
#fig.update_xaxes(title_font=dict(size=18, family='Courier', color='crimson'))

fig.show()

# + {"tags": ["to_remove"]}
# juanito 3.2

# + {"tags": ["to_remove"]}
# juanito 3.3

# + {"tags": ["to_remove"]}
count_resp = inai.groupby('respuesta')['folio'].count().reset_index()
count_resp = count_resp.sort_values(by = 'folio', ascending = False).reset_index()
count_resp['prop'] = (count_resp.folio / count_resp.folio.sum()) * 100
count_resp = count_resp.drop(columns = ['index'])
# count_resp

# + {"tags": ["to_remove"]}
fig = px.bar(count_resp, x='prop', y='respuesta', orientation='h',
             color_continuous_scale=None,
             hover_data=['folio'], #color='prop',
             labels={'prop':'Proporción de solicitudes %',
                    'folio' : 'Solicitudes totales'} , width=900
            
            )
fig.update_layout(template="plotly_white")

fig.update_yaxes(title_text = "Respuesta")

fig.show()
# -

# Podemos observar que las respuestas registradas no son específicas a las solicitudes, sino que más bien reflejan el estatus de la solicitud o la forma en que fue entregada. La respuesta más común es que la entrega se dio por medio de un archivo electrónico, que es muy congruente con lo que vimos en el medio de entrega. 
#
# Hay respuestas que indican que al solicitante le faltó un paso extra: 
#
# + Requerimiento de información adicional
#
#
# + Notificación de pago
#
#
# + No es de competencia de la unidad de enlace
#
#
#
# Hay respuestas que nos intrigan: 
#
# + La solicitud no corresponde al marco de la Ley
#
#
# + Inexistencia de la información solicitada
#
#
# + Negativa por ser reservada o confidencial
#
#
# + Información parcialmente reservada o confidencial
#
#
# + No se dará trámite a la solicitud
#
#
# Más adelante haremos un análisis detallado sobre las preguntas que dieron lugar a las respuestas que nos intrigan. Con una vista muy rápida pudimos notar que los solicitantes hacían preguntas *muy específicas* (productos de madera, acceso a Internet, calentadores, minutas de reuniones, etc.), y es importante resaltar que muchas de estas preguntas buscaban conocer sobre contratos celebrados entre organismos o la marca de coche y renumeración de los servidores públicos. Pudimos ver también que una porción importante de estas preguntas eran sobre los candidatos presidenciales para las elecciones del 2018. 

# + {"tags": ["to_remove"]}
intriga = inai[inai.respuesta.isin(['La solicitud no corresponde al marco de la Ley ',
                          'Inexistencia de la información solicitada',
                         'Negativa por ser reservada o confidencial', 
                         'Información parcialmente reservada o confidencial', 
                         'No se dará trámite a la solicitud'])]

intriga = intriga[['tipo_solicitud', 'descripcion', 'respuesta', 'texto_respuesta']]

#intriga.to_csv('intriga.csv')
# -

# Ahora bien, regresando un poquito al tema de las respuestas, un campo que está muy relacionado con la respuesta a las solicitudes es el estatus de la solicitud. 

# + {"tags": ["to_remove"]}
count_est = inai.groupby('estatus')['folio'].count().reset_index()
count_est = count_est.sort_values(by = 'folio', ascending = False).reset_index()
count_est['prop'] = (count_est.folio / count_est.folio.sum()) * 100
count_est = count_est.drop(columns = ['index'])
# count_est

# + {"tags": ["to_remove"]}
fig = px.bar(count_est, x='prop', y='estatus', orientation='h',
             color_continuous_scale=None,
             hover_data=['folio'], #color='prop',
             labels={'prop':'Proporción de solicitudes %',
                    'folio' : 'Solicitudes totales'} , width=900
            
            )
fig.update_layout(template="plotly_white")

fig.update_yaxes(title_text = "Estatus")

fig.show()

# + {"tags": ["to_remove"]}
# juanito 4
# -

# El 87% de las solicitudes se cuentan como terminadas. El resto de las solicitudes siguen en proceso, están esperando a un pago o respuesta del ciudadano, o fueron rechazadas. Como las claves identificadoras de las solicitudes son únicas, realmente no hay forma de saber si las solicitudes "en proceso" o "en espera" sí se concluyeron o no.
#
# Como no hay una forma muy clara de conocer si al final todas las solicitudes sí se completaron o no al 100%, vamos a calificar las respuestas como  **satisfactoria** o **no satisfactoria**. Además, tomaremos en cuenta aquellas solicitudes cuya respuesta fue que hubo falta por parte del ciudadano. Así vamos a calificar las respuestas: 
#
# Satisfactoria: 
# + Entrega de información en medio electrónico
#
# + Notificación de disponibilidad de información
#
# + Notificación lugar y fecha de entrega
#
# + Notificación de envío
#
# + La información está disponible públicamente
#
#  
# No satisfactoria:
# + No es de competencia de la unidad de enlace
#
# + La solicitud no corresponde al marco de la Ley
#
# + La solicitud no corresponde al marco de la Ley
#
# + Inexistencia de la información solicitada
#
# + Negativa por ser reservada o confidencial
#
# + Información parcialmente reservada o confidencial
#
# + No se dará trámite a la solicitud
#
# + Sin respuesta
#
# + Notificación de cambio de tipo de solicitud
#
# + Notificación de prórroga
#
#  
# Falta del solicitante: 
#
# + Requerimiento de información adicional
#
# + Respuesta del solicitante a la notificación de entrega de información sin costo
#
# + Respuesta a solicitud de información adicional
#
# + Respuesta del solicitante a la notificación de entrega de información con  costo
#
# + Notificación de pago
#
# Vamos a ver cómo es la calidad de respuesta por sector.

# + {"tags": ["to_remove"]}
labels = inai.respuesta.unique().astype(str)
#labels

# + {"tags": ["to_remove"]}
categorias = [0, 1, 0, 1, -1, 0, 0, 0, 0, -1, 0, 0, 0, -1, -1, 1, 1, 1, -1]
category_translation = dict(zip(labels, categorias))

# + {"tags": ["to_remove"]}
inai['calidad_respuesta'] = inai.respuesta.map(category_translation)

# + {"tags": ["to_remove"]}
inai['trans'] = np.where(inai.calidad_respuesta == 1, "Satisfactoria",
                                      np.where(inai.calidad_respuesta == 0,"No satisfactoria", 
                                               "Falta solicitante" ))


# + {"tags": ["to_remove"]}
# count_year_calidad.calidad_respuesta == 1, "Satisfactoria",
# count_year_calidad.calidad_respuesta == 0,"No satisfactoria", 
# count_year_calidad.calidad_respuesta == -1, "Falta solicitante" ))
aa = inai.groupby(['trans', 'respuesta'])['folio'].count().reset_index()
aa.rename(columns = {'trans': 'Categoría asignada', 'respuesta' : 'Categoría reall', 
                    'folio' : 'Solicitudes totales'}, inplace = True)
aa
# -

# ### Calidad de respuesta por año

# + {"tags": ["to_remove"]}
count_year_calidad = inai.groupby(['year_solicitud', 'calidad_respuesta'])['folio'].count().reset_index()
count_year_calidad['trans'] = np.where(count_year_calidad.calidad_respuesta == 1, "Satisfactoria",
                                      np.where(count_year_calidad.calidad_respuesta == 0,"No satisfactoria", 
                                               "Falta solicitante" ))

count_year_calidad = count_year_calidad.merge(count_year)
count_year_calidad['prop'] = np.round( (count_year_calidad.folio/count_year_calidad.total)*100  , 2)


# + {"tags": ["to_remove"]}
count_year_calidad_pv = count_year_calidad.pivot(index= 'year_solicitud', 
                  columns = 'trans', values = 'prop')
# count_year_calidad_pv

# + {"tags": ["to_remote"]}
fig = go.Figure(data=[
    go.Bar(name='Falta', y = count_year_calidad_pv.iloc[:,0])  ,
    go.Bar(name='No satisfactoria', y = count_year_calidad_pv.iloc[:,1])  ,
    go.Bar(name='Satisfactoria', y = count_year_calidad_pv.iloc[:,2])
    #go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
])

fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = [0,1,2,3,4,5,6,7],
        ticktext = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
    )
)
fig.update_yaxes(title_text = "Proporción de solicitudes")
fig.update_xaxes(title_text = "Año")
fig.update_layout(template="plotly_white")


fig.update_layout(barmode='stack')

fig.show()


# + {"tags": ["to_remove"]}
## das ist alles 
# -


