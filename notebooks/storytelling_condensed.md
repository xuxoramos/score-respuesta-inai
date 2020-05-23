---
jupyter:
  jupytext:
    cell_metadata_filter: ExecuteTime,autoscroll,tags,-hide_output
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.3.3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python ExecuteTime={"end_time": "2019-08-25T17:52:59.317731Z", "start_time": "2019-08-25T17:52:59.311201Z"} tags=["to_remove"]
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
```


<!-- #region -->
# ¿Qué es y qué hace el INAI?

El INAI (Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales) es el organismo encargado de que tengamos acceso a la información pública y podamos proteger nuestros datos personales.


La idea del INAI (que en otras vidas se llamaba IFAI) surgió desde el primer sexenio de este milenio y ha ido transformándose poco a poco. Con este trabajo buscamos analizar las respuestas e información que brinda el INAI ante las preguntas de los ciudadanos. Comencemos.

<!-- #endregion -->

```python ExecuteTime={"end_time": "2019-08-25T17:51:48.613442Z", "start_time": "2019-08-25T17:51:32.621055Z"} tags=["to_remove"]
inai = pd.read_parquet('../data/inai.parquet')
```

```python ExecuteTime={"end_time": "2019-08-25T17:51:50.311131Z", "start_time": "2019-08-25T17:51:48.740118Z"} tags=["to_remove"]
for col in ['fecha_solicitud', 'fecha_respuesta', 'fecha_limite']:
    inai[col] = pd.to_datetime(inai[col]).dt.date

 #   , format='%d%b%Y:%H:%M:%S.%f'
```

```python tags=["to_remove"]
#inai['fecha_solicitud'] = pd.to_datetime(inai['fecha_solicitud'])


inai['year_solicitud'] =  pd.to_datetime(inai['fecha_solicitud']).dt.year
inai['year_respuesta'] =  pd.to_datetime(inai['fecha_respuesta']).dt.year

inai['mes_solicitud'] =  pd.to_datetime(inai['fecha_solicitud']).dt.month
inai['mes_respuesta'] =  pd.to_datetime(inai['fecha_respuesta']).dt.month
```

## Vista rápida de las solicitudes


Contamos con datos de solicitudes del 1 de enero del 2012 al 30 de junio del 2019. Esto equivale a un total **1'395,851** preguntas. Si asumimos que hay una pregunta por persona, es como si al 1.09% de nuestra población hubiera hecho solicitudes de información.

```python tags=["to_remove"]
# http://dof.gob.mx/nota_detalle.php?codigo=5436061&fecha=04/05/2016
```

Curiosamente, tenemos solicitudes desde las alcaldías de Ciudad de México hasta "COLEGIO HOGWARTS DE MAGIA Y HECHICERÍA" en el Reino Unido. Claramente, la creatividad de los mexicanos ante un campo de datos abierto no podía faltar.

Veamos cómo se ve el número de solicitudes por año y mes.


```python tags=["to_remove"]
pais_count = inai.groupby('pais')['folio'].count().reset_index()

pais_count = pais_count.sort_values(by = 'folio', ascending = False)

pais_count ['prop'] = (pais_count.folio / pais_count.folio.sum()) * 100
pais_count
```

```python
import plotly.graph_objects as go
import plotly.express as px
```

```python
import plotly.offline as py
```

```python tags=["to_remove"]
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
```

El número de solicitudes totales por año fue aumentando poco a poco del 2012 al 2017, año en que alcanzó su punto máximo, y después disminuyó. De hecho los 3 días en que más solicitudes hubo fueron el 8 de febrero 2017, 9 de febrero del 2017 y el 21 de febrero del 2017. Las solicitudes hechas en esos días son de diversos temas, pero un interés recurrente es conocer el sueldo de los funcionarios públicos.

Para conocer un poco más el detalle del número de solicitudes, ahora vemos cómo se ven las solicitudes por mes y año.

```python tags=["to_remove"]
fecha_count = inai.groupby('fecha_solicitud')['folio'].count().reset_index()
fecha_count = fecha_count.sort_values(by = 'folio', ascending = False)
```

```python tags=["to_remove"]
top_fechas = inai[inai.fecha_solicitud.isin(fecha_count.fecha_solicitud.head(3))]

# top_fechas.sector.value_counts()
```

```python tags=["to_remove"]
count = inai.groupby(['year_solicitud', 'mes_solicitud'])['folio'].count().reset_index()
# count.head()
```

```python tags=["to_remove"]
# esta es la paleta de colores
pal = sns.cubehelix_palette(8)
# pal.as_hex()
```

```python tags=["to_remove"]
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
```

Al analizar el número de solicitudes por mes y año podemos ver un patrón interesante: el número de preguntas baja en los meses finales del año y luego aumenta al inicio del año siguiente. Las combinaciones de mes-año con mayor número de preguntas fueron febrero 2017 y octubre 2018.

## Medios de Entrada de Solicitudes

Ya que vimos a grandes rasgos las solicitudes, vamos a analizar el medio de entrada.

```python tags=["to_remove"]
count_medio = inai.groupby('medio_entrada')['folio'].count().reset_index()
count_medio['prop'] = (count_medio.folio / count_medio.folio.sum()) * 100
# count_medio
```

```python tags=["to_remove"]
import plotly.express as px
#data = px.data.gapminder()

#data_canada = data[data.country == 'Canada']
fig = px.bar(count_medio, x='medio_entrada', y='prop', #orientation='h',
             color_continuous_scale=None,
             hover_data=['prop'], #color='prop',
             labels={'prop':'Proporción de solicitudes %',
                    'medio_entrada' : 'Medio de Entrada'}, width=900

            )
fig.update_layout(template="plotly_white")


fig.show()
```

Cerca del 96% de las solicitudes se realizaron por medio electrónico, mientras que 56 mil solicitudes se hicieron por medios manuales.

## Medios de entrega de respuesta

El medio de **entrega** también cambia según el medio de entrada.


```python tags=["to_remove"]
count_medio_entrega = inai.groupby(['medio_entrada','medio_entrega'])['folio'].count().reset_index()

count_medio.rename(columns = {'folio':'total'}, inplace = True)

count_medio_entrega = count_medio_entrega.merge(count_medio[['medio_entrada', 'total']])
count_medio_entrega['prop_medio'] = (count_medio_entrega.folio / count_medio_entrega.total) * 100
# count_medio_entrega
```

```python tags=["to_remove"]
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
```

Podemos ver que el medio de entrega más popular en el medio Eléctronico es Entrega por Internet en la "PNT" (Plataforma Nacional de Transparencia), mientras que las solicitudes manuales la entrega más común es "Otro Medio". Aunque no lo podemos apreciar, hubo 709 solicitudes (0.05% de las solicitudes Electrónicas) que se entregaron de forma "Verbal".

## Estatus de solicitudes

```python tags=["to_remove"]
count_est = inai.groupby('estatus')['folio'].count().reset_index()
count_est = count_est.sort_values(by = 'folio', ascending = False).reset_index()
count_est['prop'] = (count_est.folio / count_est.folio.sum()) * 100
count_est = count_est.drop(columns = ['index'])
# count_est
```

```python tags=["to_remove"]
fig = px.bar(count_est, x='prop', y='estatus', orientation='h',
             color_continuous_scale=None,
             hover_data=['folio'], #color='prop',
             labels={'prop':'Proporción de solicitudes %',
                    'folio' : 'Solicitudes totales'} , width=900

            )
fig.update_layout(template="plotly_white")

fig.update_yaxes(title_text = "Estatus")

fig.show()
```

<!-- #region -->
El 87% de las solicitudes se cuentan como terminadas. El resto de las solicitudes siguen en proceso, están esperando a un pago o respuesta del ciudadano, o fueron rechazadas. Como las claves identificadoras de las solicitudes son únicas, realmente no hay forma de saber si las solicitudes "en proceso" o "en espera" sí se concluyeron o no.

## Calidad de las respuestas

Como no hay una forma muy clara de conocer si al final todas las solicitudes sí se completaron o no al 100%, vamos a calificar las respuestas como  **satisfactoria** o **no satisfactoria**. Además, tomaremos en cuenta aquellas solicitudes cuya respuesta fue que hubo falta por parte del ciudadano. Así vamos a calificar las respuestas:

Satisfactoria:
+ Entrega de información en medio electrónico

+ Notificación de disponibilidad de información

+ Notificación lugar y fecha de entrega

+ Notificación de envío

+ La información está disponible públicamente


No satisfactoria:
+ No es de competencia de la unidad de enlace

+ La solicitud no corresponde al marco de la Ley

+ Inexistencia de la información solicitada

+ Negativa por ser reservada o confidencial

+ Información parcialmente reservada o confidencial

+ No se dará trámite a la solicitud

+ Sin respuesta

+ Notificación de cambio de tipo de solicitud

+ Notificación de prórroga


Falta del solicitante:

+ Requerimiento de información adicional

+ Respuesta del solicitante a la notificación de entrega de información sin costo

+ Respuesta a solicitud de información adicional

+ Respuesta del solicitante a la notificación de entrega de información con  costo

+ Notificación de pago

Vamos a ver cómo es la calidad de respuesta por sector.
<!-- #endregion -->

```python ExecuteTime={"end_time": "2019-08-25T18:36:31.278566Z", "start_time": "2019-08-25T18:36:31.140534Z"} tags=["to_remove"]
labels = inai.respuesta.unique().astype(str)
#labels
```

```python ExecuteTime={"end_time": "2019-08-25T18:46:16.887278Z", "start_time": "2019-08-25T18:46:16.883702Z"} tags=["to_remove"]
categorias = [0, 1, 0, 1, -1, 0, 0, 0, 0, -1, 0, 0, 0, -1, -1, 1, 1, 1, -1]
category_translation = dict(zip(labels, categorias))
```

```python ExecuteTime={"end_time": "2019-08-25T18:46:34.656737Z", "start_time": "2019-08-25T18:46:34.514717Z"} tags=["to_remove"]
inai['calidad_respuesta'] = inai.respuesta.map(category_translation)
```

```python tags=["to_remove"]
inai['trans'] = np.where(inai.calidad_respuesta == 1, "Satisfactoria",
                                      np.where(inai.calidad_respuesta == 0,"No satisfactoria",
                                               "Falta solicitante" ))

```

```python tags=["to_remove"]
# count_year_calidad.calidad_respuesta == 1, "Satisfactoria",
# count_year_calidad.calidad_respuesta == 0,"No satisfactoria",
# count_year_calidad.calidad_respuesta == -1, "Falta solicitante" ))
aa = inai.groupby(['trans', 'respuesta'])['folio'].count().reset_index()
aa.rename(columns = {'trans': 'Categoría asignada', 'respuesta' : 'Categoría reall',
                    'folio' : 'Solicitudes totales'}, inplace = True)
aa
```

### Calidad de respuesta por año

```python tags=["to_remove"]
count_year = inai.groupby('year_solicitud')['folio'].count().reset_index()
count_year.rename(columns = {'folio' : 'total'}, inplace = True)

count_year_calidad = inai.groupby(['year_solicitud', 'calidad_respuesta'])['folio'].count().reset_index()
count_year_calidad['trans'] = np.where(count_year_calidad.calidad_respuesta == 1, "Satisfactoria",
                                      np.where(count_year_calidad.calidad_respuesta == 0,"No satisfactoria",
                                               "Falta solicitante" ))

count_year_calidad = count_year_calidad.merge(count_year)
count_year_calidad['prop'] = np.round( (count_year_calidad.folio/count_year_calidad.total)*100  , 2)

```

```python tags=["to_remove"]
count_year_calidad_pv = count_year_calidad.pivot(index= 'year_solicitud',
                  columns = 'trans', values = 'prop')
# count_year_calidad_pv
```

```python tags=["to_remote"]
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

```

```python tags=["to_remove"]
## das ist alles
```

```python tags=["to_remove"]
sect = ['Ninguno', 'Energía', 'Aportaciones a Seguridad Social',
       'Comunicaciones y Transportes', 'Educación Pública',
       'Reforma Agraria', 'Economía', 'Desarrollo Social',
       'Función Pública', 'Gobernación', 'Hacienda y Crédito Público',
       'Medio Ambiente y Recursos Naturales', 'Salud',
       'Trabajo y Previsión Social', 'Turismo', 'Poder Legislativo',
       'Procuraduría General de la República',
       'Agricultura, Ganadería, Desarrollo Rural, Pesca y Alimentación',
       'Defensa Nacional', 'Seguridad Pública',
       'Presidencia de la República', 'Relaciones Exteriores', 'Marina',
       'Consejo Nacional de Ciencia y Tecnología',
       'Previsiones y Aportaciones para los Sistemas de Educación Básica, Normal, Tecnológica y de Adultos',
       'Consejería Jurídica del Ejecutivo Federal']
```

```python
for s in sect:
    print(s)
    # Ninguno
    i = inai[inai.sector == s]
    year_count = i.groupby('year_solicitud')['folio'].count().reset_index()
    year_count.rename(columns = {'folio' : 'total'}, inplace = True)
    count_year_calidad = i.groupby(['year_solicitud', 'calidad_respuesta'])['folio'].count().reset_index()

    count_year_calidad['trans'] = np.where(count_year_calidad.calidad_respuesta == 1, "Satisfactoria",
                                      np.where(count_year_calidad.calidad_respuesta == 0,"No satisfactoria",
                                               "Falta solicitante" ))

    count_year_calidad = count_year_calidad.merge(year_count)
    count_year_calidad['prop'] = np.round( (count_year_calidad.folio/count_year_calidad.total)*100  , 2)


    count_year_calidad_pv = count_year_calidad.pivot(index= 'year_solicitud',
                                                      columns = 'trans', values = 'prop')

    plt.figure(figsize=(14, 7))

    plt.plot(count_year_calidad_pv.iloc[:,0] , color = '#e1b1b4')
    plt.plot(count_year_calidad_pv.iloc[:,1] , color = '#b77495')
    plt.plot(count_year_calidad_pv.iloc[:,2] , color = '#52315f')
    #plt.plot(count_ent_year_pv.iloc[:,2] , color = '#cf91a3')
    #plt.plot(count_ent_year_pv.iloc[:,3] , color = '#b77495')
    #plt.plot(count_ent_year_pv.iloc[:,4] , color = '#9a5b88', marker= 'v')
    #plt.plot(count_ent_year_pv.iloc[:,5] , color = '#52315f', marker = '^')
    #plt.plot(count_ent_year_pv.iloc[:,6] , color = '#2d1e3e')


    #plt.legend(count_ent_year_pv.columns, loc=2, prop={'size': 7})
    plt.legend()
    plt.ylim([0,100])
    plt.title('Porcentaje de bateo de las solicitudes en sector ' + s )

    plt.xlabel('Año')
    plt.ylabel('Porcentaje de solicitudes %')

    plt.show()

```

## Porcentaje de bateo (general)

```python
count_year_month = inai.groupby(['year_solicitud', 'mes_solicitud'])['folio'].count().reset_index()
count_year_month.rename(columns = {'folio' : 'total'}, inplace = True)
count_year_month.head()
```

```python
count_year_calidad = inai.groupby(['year_solicitud', 'mes_solicitud', 'calidad_respuesta'])['folio'].count().reset_index()
count_year_calidad['trans'] = np.where(count_year_calidad.calidad_respuesta == 1, "Satisfactoria",
                                      np.where(count_year_calidad.calidad_respuesta == 0,"No satisfactoria",
                                               "Falta solicitante" ))

count_year_calidad = count_year_calidad.merge(count_year_month, on = ['year_solicitud', 'mes_solicitud'])
count_year_calidad['prop'] = np.round( (count_year_calidad.folio/count_year_calidad.total)  , 2)

count_year_calidad['mes_solicitud'] =  count_year_calidad.mes_solicitud.map("{:02}".format)

count_year_calidad['period'] = count_year_calidad.year_solicitud.map(str) + '-' + count_year_calidad.mes_solicitud.map(str)


count_year_calidad
```

### Número de solicitudes- calidad

```python
count_year_m_calidad_pv = count_year_calidad.pivot(index= 'period',
                  columns = 'trans', values = 'folio')

plt.figure(figsize=(14, 7))

plt.plot(count_year_m_calidad_pv.iloc[:,0] , color = '#e1b1b4')
plt.plot(count_year_m_calidad_pv.iloc[:,1] , color = '#b77495')
plt.plot(count_year_m_calidad_pv.iloc[:,2] , color = '#52315f')
#plt.plot(count_ent_year_pv.iloc[:,2] , color = '#cf91a3')
#plt.plot(count_ent_year_pv.iloc[:,3] , color = '#b77495')
#plt.plot(count_ent_year_pv.iloc[:,4] , color = '#9a5b88', marker= 'v')
#plt.plot(count_ent_year_pv.iloc[:,5] , color = '#52315f', marker = '^')
#plt.plot(count_ent_year_pv.iloc[:,6] , color = '#2d1e3e')


#plt.legend(count_ent_year_pv.columns, loc=2, prop={'size': 7})
plt.legend()
#plt.ylim([0,100])
#plt.xticks(rotation = 70, size = 7)
plt.xticks(range(0,87,3), rotation = 50)
plt.yticks([0, 5000, 10000, 15000, 20000, 25000], ["0", "5,000", "10,000", "15,000", "20,000", "25,000"])

plt.xlabel('Año / Mes')
plt.ylabel('Número de solicitudes')
plt.title('Calidad de respuesta por año mes')

plt.show()
```

```python
plt.rcParams['figure.figsize'] = (18, 9)
sns_ch = sns.cubehelix_palette(n_colors=3, as_cmap=True)
```

```python
plt.figure(figsize=(20, 10))

count_year_m_calidad_pv = count_year_calidad.pivot(index= 'period',
                  columns = 'trans', values = 'folio')

count_year_m_calidad_pv.plot.area(colormap=sns_ch,
                                  alpha=0.75,
                                 xticks = range(0,87,3))

plt.legend(loc=2, prop={'size': 26})

plt.xticks(range(0,87,3), rotation = 50, size = 20)
plt.yticks(size = 20)

plt.yticks([0, 5000, 10000, 15000, 20000, 25000,  30000],
           ["0", "5,000", "10,000", "15,000", "20,000", "25,000",
            "30,000"])

plt.xlabel('Año / Mes', size = 20)
plt.ylabel('Número de solicitudes', size = 20)
plt.title('Calidad de respuesta por año mes', size = 30)
#plt.savefig('bateo_general_trimestre_num.png', dpi = 300)
plt.show()
```

### Porcentaje de solicitudes

```python
plt.figure(figsize=(20, 10))

count_year_m_calidad_pv = count_year_calidad.pivot(index= 'period',
                  columns = 'trans', values = 'prop')


plt.plot(count_year_m_calidad_pv.iloc[:,0] , color = '#e1b1b4', linewidth=5.0)

plt.plot(count_year_m_calidad_pv.iloc[:,1] , color = '#b77495', linewidth=5.0)
plt.plot(count_year_m_calidad_pv.iloc[:,2] , color = '#52315f', linewidth=5.0)
#plt.plot(count_ent_year_pv.iloc[:,2] , color = '#cf91a3')
#plt.plot(count_ent_year_pv.iloc[:,3] , color = '#b77495')
#plt.plot(count_ent_year_pv.iloc[:,4] , color = '#9a5b88', marker= 'v')
#plt.plot(count_ent_year_pv.iloc[:,5] , color = '#52315f', marker = '^')
#plt.plot(count_ent_year_pv.iloc[:,6] , color = '#2d1e3e')


#plt.legend(count_ent_year_pv.columns, loc=2, prop={'size': 7})
plt.legend(loc=2, prop={'size': 22})
plt.ylim([-0.1,1.1])
plt.yticks(size = 16)
plt.xticks(range(0,87,3), rotation = 50, size = 16)

#plt.yticks([0, 5000, 10000, 15000, 20000, 25000], ["0", "5,000", "10,000", "15,000", "20,000", "25,000"])

plt.xlabel('Año / Mes', size = 20)
plt.ylabel('Proporción de solicitudes', size = 20)
plt.title('Calidad de respuesta por año mes', size = 20)
# plt.savefig('bateo_general_trimestre_porcentaje.png', dpi = 300)


plt.show()
```

```python
count_year_m_calidad_pv_prop = count_year_calidad.pivot(index= 'period',
                  columns = 'trans', values = 'prop')


count_year_m_calidad_pv_prop.plot.area(colormap=sns_ch,
                                  alpha=0.5,
                                 xticks = range(0,87,3),
                                      stacked = False)

#plt.legend(loc=2, prop={'size': 26})

#plt.xticks(range(0,87,3), rotation = 50, size = 20)
#plt.yticks(size = 20)

#plt.yticks([0, 5000, 10000, 15000, 20000, 25000,  30000],
#           ["0", "5,000", "10,000", "15,000", "20,000", "25,000",
#            "30,000"])

#plt.xlabel('Año / Mes', size = 20)
#plt.ylabel('Porcentaje de solicitudes %', size = 20)
#plt.title('Calidad de respuesta por año mes', size = 30)

plt.show()
```

## Porcentaje de bateo (por sector)


### Número de solicitudes

```python
for s in sect:
    print(s)
    i = inai[inai.sector == s]

    count_year_month = i.groupby(['year_solicitud', 'mes_solicitud'])['folio'].count().reset_index()
    count_year_month.rename(columns = {'folio' : 'total'}, inplace = True)

    count_year_calidad = i.groupby(['year_solicitud', 'mes_solicitud', 'calidad_respuesta'])['folio'].count().reset_index()
    count_year_calidad['trans'] = np.where(count_year_calidad.calidad_respuesta == 1, "Satisfactoria",
                                          np.where(count_year_calidad.calidad_respuesta == 0,"No satisfactoria",
                                                   "Falta solicitante" ))

    count_year_calidad = count_year_calidad.merge(count_year_month, on = ['year_solicitud', 'mes_solicitud'])
    count_year_calidad['prop'] = np.round( (count_year_calidad.folio/count_year_calidad.total)*100  , 2)

    count_year_calidad['mes_solicitud'] =  count_year_calidad.mes_solicitud.map("{:02}".format)

    count_year_calidad['period'] = count_year_calidad.year_solicitud.map(str) + '-' + count_year_calidad.mes_solicitud.map(str)

    count_year_m_calidad_pv = count_year_calidad.pivot(index= 'period',
                  columns = 'trans', values = 'folio')

    plt.figure(figsize=(14, 7))

    plt.plot(count_year_m_calidad_pv.iloc[:,0] , color = '#e1b1b4')

    plt.plot(count_year_m_calidad_pv.iloc[:,1] , color = '#b77495')
    plt.plot(count_year_m_calidad_pv.iloc[:,2] , color = '#52315f')
    #plt.plot(count_ent_year_pv.iloc[:,2] , color = '#cf91a3')
    #plt.plot(count_ent_year_pv.iloc[:,3] , color = '#b77495')
    #plt.plot(count_ent_year_pv.iloc[:,4] , color = '#9a5b88', marker= 'v')
    #plt.plot(count_ent_year_pv.iloc[:,5] , color = '#52315f', marker = '^')
    #plt.plot(count_ent_year_pv.iloc[:,6] , color = '#2d1e3e')


    #plt.legend(count_ent_year_pv.columns, loc=2, prop={'size': 7})
    plt.legend()
    #plt.ylim([0,100])
    plt.xticks(rotation = 70, size = 7)
    #plt.yticks([0, 5000, 10000, 15000, 20000, 25000], ["0", "5,000", "10,000", "15,000", "20,000", "25,000"])

    plt.xlabel('Año / Mes')
    plt.ylabel('Número de solicitudes')
    plt.title('Calidad de respuesta por año mes en sector ' + s)

    name = 'bateo_num_año_mes_'+s+'.png'
    # plt.savefig(name)

    plt.show()

```

```python
sect
```

### Número de solicitudes bateadas: sectores más interesantes

```python
sect_ref = ['Salud', 'Energía','Hacienda y Crédito Público' ,'Función Pública', 'Gobernación',
           'Previsiones y Aportaciones para los Sistemas de Educación Básica, Normal, Tecnológica y de Adultos',
           'Consejería Jurídica del Ejecutivo Federal']
```

```python
# salud, energia/pemex, hacienda y función pública
```

```python
for s in sect:
    print(s)
    i = inai[inai.sector == s]

    count_year_month = i.groupby(['year_solicitud', 'mes_solicitud'])['folio'].count().reset_index()
    count_year_month.rename(columns = {'folio' : 'total'}, inplace = True)

    count_year_calidad = i.groupby(['year_solicitud', 'mes_solicitud', 'calidad_respuesta'])['folio'].count().reset_index()
    count_year_calidad['trans'] = np.where(count_year_calidad.calidad_respuesta == 1, "Satisfactoria",
                                          np.where(count_year_calidad.calidad_respuesta == 0,"No satisfactoria",
                                                   "Falta solicitante" ))

    count_year_calidad = count_year_calidad.merge(count_year_month, on = ['year_solicitud', 'mes_solicitud'])
    count_year_calidad['prop'] = np.round( (count_year_calidad.folio/count_year_calidad.total)*100  , 2)

    count_year_calidad['mes_solicitud'] =  count_year_calidad.mes_solicitud.map("{:02}".format)

    count_year_calidad['period'] = count_year_calidad.year_solicitud.map(str) + '-' + count_year_calidad.mes_solicitud.map(str)

    count_year_m_calidad_pv = count_year_calidad.pivot(index= 'period',
                  columns = 'trans', values = 'folio')

    plt.figure(figsize=(14, 7))

    count_year_m_calidad_pv.plot.area(colormap=sns_ch,
                                  alpha=0.75,
                                 xticks = range(0,87,3))


    plt.legend(loc=2, prop={'size': 26})

    #plt.ylim([0,100])
    plt.xticks(range(0,87,3), rotation = 50, size = 20)
    plt.yticks(size = 20)
    #plt.yticks([0, 5000, 10000, 15000, 20000, 25000,  30000],
    #       ["0", "5,000", "10,000", "15,000", "20,000", "25,000",
    #        "30,000"])

    plt.xlabel('Año / Mes', size = 20)
    plt.ylabel('Número de solicitudes', size = 20)
    plt.title('Calidad de respuesta por año mes en sector ' + s, size = 30)

    name = 'bateo_conteo_año_mes_sector_'+s+'.png'
    # plt.savefig(name, dpi = 300)

    plt.show()

```

### Proporción de solicitudes bateadas: sectores más interesantes

```python
for s in sect_ref:
    print(s)
    i = inai[inai.sector == s]

    count_year_month = i.groupby(['year_solicitud', 'mes_solicitud'])['folio'].count().reset_index()
    count_year_month.rename(columns = {'folio' : 'total'}, inplace = True)

    count_year_calidad = i.groupby(['year_solicitud', 'mes_solicitud', 'calidad_respuesta'])['folio'].count().reset_index()
    count_year_calidad['trans'] = np.where(count_year_calidad.calidad_respuesta == 1, "Satisfactoria",
                                          np.where(count_year_calidad.calidad_respuesta == 0,"No satisfactoria",
                                                   "Falta solicitante" ))

    count_year_calidad = count_year_calidad.merge(count_year_month, on = ['year_solicitud', 'mes_solicitud'])
    count_year_calidad['prop'] = np.round( (count_year_calidad.folio/count_year_calidad.total)  , 2)

    count_year_calidad['mes_solicitud'] =  count_year_calidad.mes_solicitud.map("{:02}".format)

    count_year_calidad['period'] = count_year_calidad.year_solicitud.map(str) + '-' + count_year_calidad.mes_solicitud.map(str)

    count_year_m_calidad_pv = count_year_calidad.pivot(index= 'period',
                  columns = 'trans', values = 'prop')

    plt.plot(count_year_m_calidad_pv.iloc[:,0] , color = '#e1b1b4', linewidth=5.0)

    plt.plot(count_year_m_calidad_pv.iloc[:,1] , color = '#b77495', linewidth=5.0)
    plt.plot(count_year_m_calidad_pv.iloc[:,2] , color = '#52315f', linewidth=5.0)

    plt.legend(loc=2, prop={'size': 22})
    plt.ylim([-0.1,1.1])
    plt.yticks(size = 16)
    plt.xticks(range(0,87,3), rotation = 50, size = 16)

    plt.xlabel('Año / Mes', size = 20)
    plt.ylabel('Proporción de solicitudes', size = 20)
    plt.title('Calidad de respuesta por año mes sector ' + s, size = 20)

    name = 'bateo_prop_año_mes_sector_'+s+'.png'
    #plt.savefig(name, dpi = 300)

    #plt.savefig('bateo_general_trimestre_porcentaje.png', dpi = 300)

    plt.show()
```

```python
count_year_m_calidad_pv = count_year_calidad.pivot(index= 'period',
                  columns = 'trans', values = 'prop')


plt.plot(count_year_m_calidad_pv.iloc[:,0] , color = '#e1b1b4', linewidth=5.0)

plt.plot(count_year_m_calidad_pv.iloc[:,1] , color = '#b77495', linewidth=5.0)
plt.plot(count_year_m_calidad_pv.iloc[:,2] , color = '#52315f', linewidth=5.0)
#plt.plot(count_ent_year_pv.iloc[:,2] , color = '#cf91a3')
#plt.plot(count_ent_year_pv.iloc[:,3] , color = '#b77495')
#plt.plot(count_ent_year_pv.iloc[:,4] , color = '#9a5b88', marker= 'v')
#plt.plot(count_ent_year_pv.iloc[:,5] , color = '#52315f', marker = '^')
#plt.plot(count_ent_year_pv.iloc[:,6] , color = '#2d1e3e')


#plt.legend(count_ent_year_pv.columns, loc=2, prop={'size': 7})
plt.legend(loc=2, prop={'size': 22})
plt.ylim([-0.1,1.1])
plt.yticks(size = 16)
plt.xticks(range(0,87,3), rotation = 50, size = 16)

#plt.yticks([0, 5000, 10000, 15000, 20000, 25000], ["0", "5,000", "10,000", "15,000", "20,000", "25,000"])

plt.xlabel('Año / Mes', size = 20)
plt.ylabel('Proporción de solicitudes', size = 20)
plt.title('Calidad de respuesta por año mes', size = 20)
# plt.savefig('bateo_general_trimestre_porcentaje.png', dpi = 300)
```

### Porcentaje de solicitudes

```python
for s in sect_ref:
    print(s)
    i = inai[inai.sector == s]

    count_year_month = i.groupby(['year_solicitud', 'mes_solicitud'])['folio'].count().reset_index()
    count_year_month.rename(columns = {'folio' : 'total'}, inplace = True)

    count_year_calidad = i.groupby(['year_solicitud', 'mes_solicitud', 'calidad_respuesta'])['folio'].count().reset_index()
    count_year_calidad['trans'] = np.where(count_year_calidad.calidad_respuesta == 1, "Satisfactoria",
                                          np.where(count_year_calidad.calidad_respuesta == 0,"No satisfactoria",
                                                   "Falta solicitante" ))

    count_year_calidad = count_year_calidad.merge(count_year_month, on = ['year_solicitud', 'mes_solicitud'])
    count_year_calidad['prop'] = np.round( (count_year_calidad.folio/count_year_calidad.total)*100  , 2)

    count_year_calidad['mes_solicitud'] =  count_year_calidad.mes_solicitud.map("{:02}".format)

    count_year_calidad['period'] = count_year_calidad.year_solicitud.map(str) + '-' + count_year_calidad.mes_solicitud.map(str)

    count_year_m_calidad_pv = count_year_calidad.pivot(index= 'period',
                  columns = 'trans', values = 'prop')

    plt.figure(figsize=(14, 7))

    plt.plot(count_year_m_calidad_pv.iloc[:,0] , color = '#e1b1b4')

    plt.plot(count_year_m_calidad_pv.iloc[:,1] , color = '#b77495')
    plt.plot(count_year_m_calidad_pv.iloc[:,2] , color = '#52315f')
    #plt.plot(count_ent_year_pv.iloc[:,2] , color = '#cf91a3')
    #plt.plot(count_ent_year_pv.iloc[:,3] , color = '#b77495')
    #plt.plot(count_ent_year_pv.iloc[:,4] , color = '#9a5b88', marker= 'v')
    #plt.plot(count_ent_year_pv.iloc[:,5] , color = '#52315f', marker = '^')
    #plt.plot(count_ent_year_pv.iloc[:,6] , color = '#2d1e3e')


    #plt.legend(count_ent_year_pv.columns, loc=2, prop={'size': 7})
    plt.legend()
    plt.ylim([-10,110])
    plt.xticks(rotation = 70, size = 7)
    #plt.yticks([0, 5000, 10000, 15000, 20000, 25000], ["0", "5,000", "10,000", "15,000", "20,000", "25,000"])

    plt.xlabel('Año / Mes')
    plt.ylabel('Porcentaje de solicitudes %')
    plt.title('Calidad de respuesta por año mes en sector ' + s)

    name = 'bateo_porc_año_mes_'+s+'.png'
    #plt.savefig(name)

    plt.show()
```

```python

```

```python

```

```python

```

```python

```

```python ExecuteTime={"end_time": "2019-08-25T21:34:46.293434Z", "start_time": "2019-08-25T21:34:25.187570Z"} tags=["to_remove"]
g = (
    inai.assign(mes=lambda df: df.fecha_solicitud.astype(str).apply(lambda s: s[0:7]))
    .groupby(['mes', 'calidad_respuesta', 'sector'])
    .size()
    .to_frame('n')
    .reset_index(drop=False)
)
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:01.911377Z", "start_time": "2019-08-25T21:35:01.900649Z"} tags=["to_remove"]
g = g.sort_values(['mes', 'sector', 'calidad_respuesta'])
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:04.341080Z", "start_time": "2019-08-25T21:35:04.333591Z"} tags=["to_remove"]
g_todas_fechas = []
for year in range(2012, 2019):
    for month in range(1, 13):
        if month < 10:
            strm = '0'+str(month)
        else:
            strm = str(month)
        g_todas_fechas.append(str(year)+'-'+strm)
for month in range(1, 7):
    if month < 10:
        strm = '0'+str(month)
    else:
        strm = str(month)
    g_todas_fechas.append('2019-'+strm)

```

```python ExecuteTime={"end_time": "2019-08-25T21:35:05.742163Z", "start_time": "2019-08-25T21:35:05.738657Z"} tags=["to_remove"]
sectores = g.sector.unique()
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:08.526495Z", "start_time": "2019-08-25T21:35:08.491422Z"} tags=["to_remove"]
ii = pd.DataFrame(list(product(g_todas_fechas, [-1, 0, 1], sectores)))
ii.columns = ['mes', 'calidad_respuesta', 'sector']
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:11.333873Z", "start_time": "2019-08-25T21:35:11.307945Z"} tags=["to_remove"]
g = ii.merge(g, how='left').fillna(0).sort_values(['mes', 'sector', 'calidad_respuesta'])
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:12.686899Z", "start_time": "2019-08-25T21:35:12.666502Z"} tags=["to_remove"]
gg = g.groupby(['mes', 'sector']).agg({'n':'sum'}).reset_index()
gg.columns = ['mes', 'sector', 'n']
gg['calidad_respuesta'] = 2
#gg.head()
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:17.225157Z", "start_time": "2019-08-25T21:35:17.210574Z"} tags=["to_remove"]
gg = pd.concat((g, gg), sort=False).sort_values(['mes', 'sector', 'calidad_respuesta'])
```

```python ExecuteTime={"end_time": "2019-08-25T21:38:12.069023Z", "start_time": "2019-08-25T21:38:12.065760Z"} tags=["to_remove"]
plt.rcParams['figure.figsize'] = (18, 9)
sns_ch = sns.cubehelix_palette(n_colors=3, as_cmap=True)
```

```python tags=["to_remove"]
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
```

```python tags=["to_remove"]
# sectores
```

```python tags=["to_remove"]
#sectores
#Comunicaciones y Transportes

#df = gg[gg.sector== 'Gobernación'].drop('sector', axis=1)
#df = df.pivot(index='mes', columns='calidad_respuesta', values='n')


#df.columns = ['Falta del solicitante', 'No satisfactoria', 'Satisfactoria', 'total']
#df.drop('total', axis=1, inplace=True)
#df
```

```python tags=["to_remove"]
#inai[(inai.sector == "Gobernación") &
#    (inai.year_solicitud.isin([2015]) ) &
#     (inai.mes_solicitud.isin([7]) )].descripcion.unique()
```

```python ExecuteTime={"end_time": "2019-08-25T21:39:29.824401Z", "start_time": "2019-08-25T21:39:18.019434Z"} tags=["to_remove"]
for i, s in enumerate(sectores):
    plt.figure(i)
    df = gg[gg.sector==s].drop('sector', axis=1)
    df = df.pivot(index='mes', columns='calidad_respuesta', values='n')
    df.columns = ['Falta del solicitante', 'No satisfactoria', 'Satisfactoria', 'total']
    df.drop('total', axis=1, inplace=True)
    df.plot.area(colormap=sns_ch, alpha=0.75)
    plt.title(s)
    plt.xlabel('Mes/Año')
    plt.ylabel('Número de solicitudes')
    #plt.show()
```

```python ExecuteTime={"end_time": "2019-08-25T21:12:43.421449Z", "start_time": "2019-08-25T21:12:10.121030Z"} tags=["to_remove"]
#sns.relplot(x='mes',  y='n',
#            row='sector', hue='calidad_respuesta',
#            kind='line',
#            aspect=3,
#            facet_kws={'sharey':False},
#            data=g)
```

<!-- #region -->
**Sector de agricultur. ganadería, desarrollo rural, pesca y alimentación**:
+ El número de solicitudes va al alza y la mayoria de solicitudes tuvieron una respuesta satisfactoria.

**Aportaciones a seguridad social (sector con la mayor proporción de solicitudes)**:
+ Las preguntas por mes/año se concentran alrededor de las tres mil preguntas, claro que hay meses con más o menos preguntas. La mayoría tuvo una respuesta satisfactori, pero es el sector con mayor número de solicitudes donde hubo fallas por parte del solicitante.

**Comunicaciones y transportes**:
+ El patrón de solicitudes en este sector es interesante pues el número de solicitudes gira alrededor de las 500-700 solicitudes por mes. Sin embargo, se observa un disparo importante donde las solicitudes llegan a más de tres mil. Esta fecha fue febrero 2017, que es muy cercana a la fecha en que se anunció el famoso "Gasolinazo".

**Consejería jurídica del Ejecutivo Federal:**
+ Observamos que en este sector la mayoría de solicitudes tuvieron una respuesta no satisfactoria. Uno de los principales picos en solicitudes se dio en febrero 2013. Muchas de estas preguntas giran alrededor de bienes o cuentas decomisadas (o aseguradas ministerialmente) de personas detenidas, los hermanos Arellano Félix fueron especialmente populares en estas solicitudes.

**Consejo Nacional de Ciencia y Tecnología**:
+ Las preguntas a este sector por mes giran alrededor de las 150 por mes aproximadamente. En este sector vemos un pico muy importante en febrero 2017. Muchas preguntas buscaban conocer el organigrama de este sector y sueldos de los funcionarios.

+ Curioso: hubo una persona que querían que le hicieran la tarea, pues esta fue su peticion: 'Solicito todo documento  investigación  trabajo  bibliografía  tesis  y en general cualquier información relacionada con el derecho al olvido. '

**Defensa nacional:**
+ La mayoría de las respuestas a solicitudes en este sector han sido satisfactorias y vemos una tendencia a la alza.


**Desarrollo social:**
+ La mayoría de las solicitudes de este sector tuvieron una respuesta satisfactoria. De febrero a mayo del 2019 observamos un pico en las solicitudes. Las preguntas son diversas pero muy enfocadas a la distribución de recursos a los programas sociales y apoyos del estado, y a conocer la lista de los beneficiarios de estos programas.

+ Curioso: Hubo una pregunta sobre la "leche radiactiva" durante el gobierno de Carlos Salinas.


**Economía:**
+ En este sector la mayoría de preguntas recibieron una respuesta satisfactoria. Hay dos picos importantes en el número de preguntas: enero 2017 y agosto 2018. Como hemos mencionados a inicios del 2017 se dio el gasolinazo, por lo que hace sentido que muchas preguntas sean sobre el petróleo. Muchas peticiones son para conocer contratos.

**Educación pública:**
+ En este sector la mayoría de preguntas también ha recibido un respuesta satisfactoria. Vemos un pico en marzo 2017: muchas preguntas en este periodo giran alrededor de la difusión de cultura, los requisitos de becas y presupuestos designados.

+ Curioso: hay una pregunta que se repitió muchísimas veces, "Solicito de la Escuela de Diseño  perteneciente a la Subdirección General de Educación e Investigación Artística  del Instituto Nacional de Bellas Artes  adscrita a la Secretaría de Cultura  lo siguiente:  El plan de estudios de educación a distancia  del año 2002"

**Energía:**
+ El número de preguntas va al alza y hay un porcentaje importante de preguntas cuya respuesta no fue satisfactoria. Vemos picos en el número de preguntas del 2019. Naturalmente, las preguntas son sobre hidrocarburos, gasolina, petróleo y PEMEX.

**Función pública:**
+ Muchas de las preguntas de este sector tuvieron una respuesta no satisfactoria. El mes con mayor preguntas fue octubre 2017. Muchas preguntas buscan conocer los salarios de servidores públicos y casos sobre enriquecimiento ilícito.

+ Curioso: hubo una solicitud que se repitió varias veces y que buscaba conocer las funciones del titular del organo interno del Hospital Regional de Alta Especialidad de Ciudad Victoria.

**Gobernación:**
+ En este sector también hay una proporción importante de solicitudes cuya respuesta fue poco satisfactoria. Los picos en las preguntas fueron en julio 2015, y los meses de marzo, abril, mayo de 2019.



<!-- #endregion -->

## Tiempo de respuesta

```python ExecuteTime={"end_time": "2019-08-25T17:52:52.241735Z", "start_time": "2019-08-25T17:52:46.096401Z"}
inai['tiempo_respuesta'] = (inai.fecha_respuesta - inai.fecha_solicitud).dt.days
```

```python ExecuteTime={"end_time": "2019-08-25T17:53:04.386949Z", "start_time": "2019-08-25T17:53:03.734656Z"}
plt.figure(figsize=(24,12))

sns.distplot(inai.tiempo_respuesta, kde=False)
```

```python ExecuteTime={"end_time": "2019-08-25T17:53:06.825904Z", "start_time": "2019-08-25T17:53:06.118368Z"}
plt.figure(figsize=(24,12))


sns.distplot(inai.tiempo_respuesta,
             kde=False,
             hist_kws={'cumulative':True})
```

```python ExecuteTime={"end_time": "2019-08-25T17:53:09.099271Z", "start_time": "2019-08-25T17:53:09.059564Z"}
inai.tiempo_respuesta.quantile(q=[0.95, 0.975, 0.99, 0.999])
```

```python ExecuteTime={"end_time": "2019-08-25T17:53:11.374781Z", "start_time": "2019-08-25T17:53:10.676332Z"}
plt.figure(figsize=(24,12))

sns.distplot(inai.tiempo_respuesta[inai.tiempo_respuesta < 141],
             kde=False, norm_hist=True)
```

```python ExecuteTime={"end_time": "2019-08-25T17:53:37.717203Z", "start_time": "2019-08-25T17:53:17.573833Z"}
plt.figure(figsize=(24,12))

g = sns.catplot(y='tiempo_respuesta', x='sector',
            kind='boxen',
            aspect=5,
            data=inai[inai.tiempo_respuesta<141].sort_values('tiempo_respuesta'))
g = g.set_xticklabels(rotation=90)
```

```python ExecuteTime={"end_time": "2019-08-25T18:11:23.462925Z", "start_time": "2019-08-25T18:10:57.863200Z"}
plt.figure(figsize=(24,12))


sns.relplot(x='fecha_solicitud', y='tiempo_respuesta',
            row='sector',
            estimator='mean',
            ci='sd',
            kind='line',
            facet_kws={'sharey': False, 'sharex': True},
            aspect=3,
            data=inai)
```

En casi todos los sectores, el tiempo medio de respuesta va a la baja con respecto al inicio del año. En el último mes de 2018 hay muchos ceros. A ver qué dice calidad.


# hasta aquí :))

```python
#############################################################################
```

# Word clouds de respuestas!


## Read-in

```python
texto_solicitudes = inai[['descripcion','sector','dependencia','year_solicitud']]
```

## Cleansing

```python
texto_solicitudes['sector'] = texto_solicitudes.sector.str.lower()
texto_solicitudes['sector'] = texto_solicitudes.sector.str.normalize('NFKD')\
.str.encode('ascii', errors = 'ignore')\
.str.decode('utf-8')
texto_solicitudes['sector'] = texto_solicitudes.sector.str.strip()
```

```python
texto_solicitudes['descripcion'] = texto_solicitudes.descripcion.str.lower()
texto_solicitudes['descripcion'] = texto_solicitudes.descripcion.str.normalize('NFKD')\
.str.encode('ascii', errors = 'ignore')\
.str.decode('utf-8')
texto_solicitudes['descripcion'] = texto_solicitudes.descripcion.str.strip()
```

```python
texto_solicitudes.head()
```

```python
texto_solicitudes.shape
```

```python
texto_solicitudes.groupby(['descripcion'])['sector']\
.count()\
.reset_index()\
.sort_values(by = 'sector', ascending = False)
```

```python
texto_solicitudes_filtered = texto_solicitudes[(texto_solicitudes.sector != 'ninguno')]
texto_solicitudes_filtered = texto_solicitudes_filtered[(texto_solicitudes_filtered\
                                                         .descripcion != 'descripcion solicitud')]
```

```python
texto_solicitudes_filtered.sector.unique()
```

```python
from wordcloud import WordCloud, STOPWORDS
from stop_words import get_stop_words
```

```python
stop_words_sp = get_stop_words('spanish')
extra_stopwords = ['solicito','solicita','informacion']
```

```python
aux = stop_words_sp + extra_stopwords
```

```python
aux
```

```python
def show_word_cloud(data, title):
    wordcloud = WordCloud(
            background_color='white',
            stopwords=stopwords,
            max_words=200,
            max_font_size=40, 
            normalize_plurals=False,
            scale=3,
            #random_state=1 # chosen at random by flipping a coin; it was heads
        ).generate(str(data))

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()
```

```python
for elemento in texto_solicitudes_filtered.sector.unique():
    df = texto_solicitudes_filtered[texto_solicitudes_filtered.sector == elemento]
    show_word_cloud(df['descripcion'], elemento)
```

# Un poquillo de tiempo (todavía no)

```python ExecuteTime={"end_time": "2019-08-22T04:29:06.689370Z", "start_time": "2019-08-22T04:29:05.689563Z"}
plt.figure(figsize=(18, 9))

tseries = inai.groupby('fecha_solicitud').size()
sns.lineplot(tseries.index, tseries.values)
```

```python ExecuteTime={"end_time": "2019-08-22T04:29:10.070971Z", "start_time": "2019-08-22T04:29:10.064338Z"}
tseries[tseries.values > 3000]
```

```python
#inai['year_solicitud'] =  pd.to_datetime(inai['fecha_solicitud']).dt.year

```

```python ExecuteTime={"end_time": "2019-08-22T10:54:06.839654Z", "start_time": "2019-08-22T10:54:02.184090Z"}
inai['semana_solicitud'] = pd.to_datetime(inai['fecha_solicitud']).dt.week
inai['por_semana_sol'] = inai.año.astype(str) + '-' + inai.semana_solicitud.astype(str)
inai['mes_solicitud'] = pd.to_datetime(inai['fecha_solicitud']).dt.month
inai['por_mes_sol'] = inai.año.astype(str) + '-' + inai.mes_solicitud.astype(str)
```

```python ExecuteTime={"end_time": "2019-08-22T10:59:26.263381Z", "start_time": "2019-08-22T10:59:26.259391Z"}
todos_meses = []
for year in range(2012, 2020):
    y = str(year)
    for month in range(1, 13):
        m = str(month)
        todos_meses.append(y+'-'+m)
```

### Respuestas por año-mes

```python ExecuteTime={"end_time": "2019-08-22T10:58:53.993957Z", "start_time": "2019-08-22T10:58:53.859830Z"}
respuestas = inai.respuesta.unique()
```

```python ExecuteTime={"end_time": "2019-08-22T10:58:54.574251Z", "start_time": "2019-08-22T10:58:54.571499Z"}
from itertools import product
```

```python ExecuteTime={"end_time": "2019-08-22T10:59:29.342988Z", "start_time": "2019-08-22T10:59:29.338391Z"}
ii = pd.DataFrame(list(product(respuestas, todos_meses)))
```

```python ExecuteTime={"end_time": "2019-08-22T10:59:41.485775Z", "start_time": "2019-08-22T10:59:41.482379Z"}
ii.columns = ['respuesta', 'por_mes_sol']
```

```python ExecuteTime={"end_time": "2019-08-22T11:05:45.436715Z", "start_time": "2019-08-22T11:05:40.941523Z"}
plt.figure(figsize=(22, 11))


tseries = inai.groupby(['por_mes_sol', 'respuesta']).size().to_frame('n').reset_index()
tseries = ii.merge(tseries, how='left').fillna(0)
sns.lineplot(tseries.por_mes_sol, tseries.n, hue=tseries.respuesta)


```

```python ExecuteTime={"end_time": "2019-08-22T11:06:20.422830Z", "start_time": "2019-08-22T11:06:00.013853Z"}
sns.relplot(x='por_mes_sol', y='n',
            row='respuesta',
            kind='line',
            height = 3,
            aspect = 7,
            data=tseries)
```

### Número de solicitudes año-mes-respuesta

```python
count_resp =  inai.groupby(['year_solicitud', 'mes_solicitud','respuesta'])['folio'].count().reset_index()
count_resp['mes_solicitud'] =  count_resp.mes_solicitud.map("{:02}".format)
count_resp['period'] = count_resp.year_solicitud.map(str) + '-' + count_resp.mes_solicitud.map(str)

count_resp
```

```python
count_resp_pivot = count_resp.pivot(index= 'period',
                  columns = 'respuesta', values = 'folio')

count_resp_pivot
```

```python
plt.figure(figsize=(18, 9))

plt.plot(count_resp_pivot)
plt.legend(count_resp_pivot.columns, loc=2, prop={'size': 7})
plt.xticks(rotation = 70, size = 6.5)
#plot.legend()
plt.figure(figsize=(24,12))
plt.show()
```

```python

```

### Número de solicitudes por año-mes-sector

```python
count_sector =  inai.groupby(['year_solicitud', 'mes_solicitud','sector'])['folio'].count().reset_index()
count_sector['mes_solicitud'] =  count_sector.mes_solicitud.map("{:02}".format)
count_sector['period'] = count_sector.year_solicitud.map(str) + '-' + count_sector.mes_solicitud.map(str)

count_sector
```

```python
count_sect_pivot = count_sector.pivot(index= 'period',
                  columns = 'sector', values = 'folio')

count_sect_pivot
```

```python
plt.figure(figsize=(24,12))

plt.plot(count_sect_pivot)
plt.legend(count_sect_pivot.columns, loc=2, prop={'size': 7})
plt.xticks(rotation = 70, size = 6.5)
#plot.legend()

plt.show()
```

```python
from itertools import product
```

```python ExecuteTime={"end_time": "2019-08-22T11:11:37.384799Z", "start_time": "2019-08-22T11:11:37.289222Z"}
#iii = pd.DataFrame(product(todos_meses, inai.sector.unique()))

iii = pd.DataFrame(list(product(todos_meses, inai.sector.unique())))
```

```python ExecuteTime={"end_time": "2019-08-22T11:11:56.356519Z", "start_time": "2019-08-22T11:11:56.353180Z"}
iii.columns = ['todos-meses', 'sector']
```

```python ExecuteTime={"end_time": "2019-08-22T11:17:54.548719Z", "start_time": "2019-08-22T11:17:54.283847Z"}
tseries = inai.groupby(['por_mes_sol', 'sector']).size().to_frame('n').reset_index()
tseries = iii.merge(tseries, how='left')
```

```python ExecuteTime={"end_time": "2019-08-22T11:18:31.399815Z", "start_time": "2019-08-22T11:17:54.950985Z"}
plt.figure(figsize=(24,12))

sns.lineplot(tseries.por_mes_sol, tseries.n, hue=tseries.sector)
```

```python ExecuteTime={"end_time": "2019-08-22T11:19:30.428894Z", "start_time": "2019-08-22T11:18:35.155661Z"}
sns.relplot(x='por_mes_sol', y='n',
            row='sector',
            kind='line',
            height = 3,
            aspect = 7,
            data=tseries)
```

> Hacer análisis de punto de cambio.
