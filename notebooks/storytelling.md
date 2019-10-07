---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.2.4
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python tags=["to_remove"]
import numpy as np
import pandas as pd
np.set_printoptions(threshold=20000)
pd.options.display.max_columns = None

from itertools import product

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (30, 15)
import seaborn as sns
sns.set()

import re

import warnings
warnings.filterwarnings('ignore')
```


<!-- #region -->
# La importancia de la transparencia 

Una frase que escuchamos mucho es que como ciudadanos tenemos derechos y obligaciones. Entre los derechos bien conocidos están el derecho a la libertad de pensamiento y expresión, derecho a la educación, salud, vivienda, y muchos más. Hoy hablaremos de un derecho que no todos ejercemos, pero cuya popularidad e importancia va al alza: derecho de acceso a la información. La Comisión Nacional de Derechos Humanos establece que "el Estado debe garantizar el derecho de las personas para acceder a la información pública, buscar, obtener y difundir libremente la información...". El acceso a la información es una herramienta para fomentar la transparencia en la gestión pública, y así poder mejorar la calidad de nuestra democracia. El INAI (Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales) es el organismo encargado de que tengamos acceso a la información pública y podamos proteger nuestros datos personales.


La idea del INAI (que en otras vidas se llamaba IFAI) surgió desde el primer sexenio de este milenio y ha ido transformándose poco a poco. Con este trabajo buscamos analizar las respuestas e información que brinda el INAI ante las preguntas de los ciudadanos. Comencemos. 

<!-- #endregion -->

```python tags=["to_remove"]
inai = pd.read_parquet('../data/inai.parquet')
```

```python tags=["to_remove"]
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

```python
C
```

```python
inai.fecha_solicitud.min()
```

```python
inai.fecha_solicitud.max()
```

```python
year_count = inai.groupby('year_solicitud')['folio'].count().reset_index()
year_count

```

```python
fecha_count = inai.groupby('fecha_solicitud')['folio'].count().reset_index()
fecha_count = fecha_count.sort_values(by = 'folio', ascending = False)
fecha_count.head()
```

### `estatus`

```python
plt.figure(figsize=(18, 9))
g = sns.countplot(inai.estatus)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

```python
plt.figure(figsize=(18, 9))

g = sns.countplot(inai.estatus)
g.set_yscale('log')
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

### `medio_entrada`

```python
plt.figure(figsize=(18, 9))

g = sns.countplot(inai.medio_entrada)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

### `tipo_solicitud`

```python
plt.figure(figsize=(18, 9))

g = sns.countplot(inai.tipo_solicitud)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

```python
plt.figure(figsize=(18, 9))

g = sns.countplot(inai.sector)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

### `descripción`

```python
inai.descripcion.sample(5)
```

Es la solicitud. Textimnear.


### `otros`

```python
inai.otros.sample(10)
```

No vale la pena, muy *ad hoc*.


### `archivo_adjunto`

```python
inai.loc[inai.archivo_adjunto!='nan', 'archivo_adjunto'].sample(10)
```

Adjuntos por el gobierno. En cualquier caso, si no son `nan` pueden ayudar a encontrar respuesta positiva o lo que signifique ADJUNTO SOLICITUD.


### `medio_entrega`

```python
plt.figure(figsize=(18, 9))

g = sns.countplot(inai.medio_entrega)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

### `respuesta`

```python
plt.figure(figsize=(18, 9))

g = sns.countplot(inai.respuesta)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

```python
plt.figure(figsize=(18, 9))

g = sns.countplot(inai.respuesta)
g.set_yscale('log')
g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

requerimiento de información adicional: la ciudadana no dio suficiente información para satisfacer el query.

respuesta del solic... : estos están en el proceso entre "ah, necesitamos esto de ti" y que se los de. Seguramente si no lo contesta, se va a deshechado por falta de pago en estatus.


###  `archivo_respuesta`

```python
inai.loc[inai.archivo_respuesta=='nan', 'medio_entrega'].sample(10)
```

## Un poquillo de tiempo

```python
count = inai.groupby(['year_solicitud', 'mes_solicitud'])['folio'].count().reset_index()
count.head()
```

```python
count
```

```python
plt.figure(figsize=(18, 9))

plt.plot(count.folio)
plt.xticks([0,12,24,36,48,60,72, 84], ["2012", "2013", "2014","2015",
                                   "2016","2017", "2018", "2019"])
plt.xlabel('Solicitudes por mes y año')
plt.ylabel('Número de solicitudes')
```

```python
plt.figure(figsize=(18, 9))

tseries = inai.groupby('fecha_solicitud').size()
sns.lineplot(tseries.index, tseries.values)
```

```python
tseries[tseries.values > 3000]
```

```python
#inai['year_solicitud'] =  pd.to_datetime(inai['fecha_solicitud']).dt.year

```

```python
inai['semana_solicitud'] = pd.to_datetime(inai['fecha_solicitud']).dt.week
inai['por_semana_sol'] = inai.año.astype(str) + '-' + inai.semana_solicitud.astype(str)
inai['mes_solicitud'] = pd.to_datetime(inai['fecha_solicitud']).dt.month
inai['por_mes_sol'] = inai.año.astype(str) + '-' + inai.mes_solicitud.astype(str)
```

```python
todos_meses = []
for year in range(2012, 2020):
    y = str(year)
    for month in range(1, 13):
        m = str(month)
        todos_meses.append(y+'-'+m)
```

### Respuestas por año-mes

```python
respuestas = inai.respuesta.unique()
```

```python
from itertools import product
```

```python
ii = pd.DataFrame(list(product(respuestas, todos_meses)))
```

```python
ii.columns = ['respuesta', 'por_mes_sol']
```

```python
plt.figure(figsize=(22, 11))


tseries = inai.groupby(['por_mes_sol', 'respuesta']).size().to_frame('n').reset_index()
tseries = ii.merge(tseries, how='left').fillna(0)
sns.lineplot(tseries.por_mes_sol, tseries.n, hue=tseries.respuesta)


```

```python
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

```python
#iii = pd.DataFrame(product(todos_meses, inai.sector.unique()))

iii = pd.DataFrame(list(product(todos_meses, inai.sector.unique())))
```

```python
iii.columns = ['todos-meses', 'sector']
```

```python
tseries = inai.groupby(['por_mes_sol', 'sector']).size().to_frame('n').reset_index()
tseries = iii.merge(tseries, how='left')
```

```python
plt.figure(figsize=(24,12))

sns.lineplot(tseries.por_mes_sol, tseries.n, hue=tseries.sector)
```

```python
sns.relplot(x='por_mes_sol', y='n', 
            row='sector', 
            kind='line',
            height = 3,
            aspect = 7,
            data=tseries)
```

> Hacer análisis de punto de cambio.


## Eficiencia

```python
inai.columns
```

## Tiempo de respuesta

```python
inai['tiempo_respuesta'] = (inai.fecha_respuesta - inai.fecha_solicitud).dt.days
```

```python
plt.figure(figsize=(24,12))

sns.distplot(inai.tiempo_respuesta, kde=False)
```

```python
plt.figure(figsize=(24,12))


sns.distplot(inai.tiempo_respuesta, 
             kde=False,
             hist_kws={'cumulative':True})
```

```python
inai.tiempo_respuesta.quantile(q=[0.95, 0.975, 0.99, 0.999])
```

```python
plt.figure(figsize=(24,12))

sns.distplot(inai.tiempo_respuesta[inai.tiempo_respuesta < 141], 
             kde=False, norm_hist=True)
```

```python
plt.figure(figsize=(24,12))

g = sns.catplot(y='tiempo_respuesta', x='sector',
            kind='boxen',
            aspect=5,
            data=inai[inai.tiempo_respuesta<141].sort_values('tiempo_respuesta'))
g = g.set_xticklabels(rotation=90)
```

```python
inai.dtypes
```

```python
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

```python
dic18 = inai[(pd.to_datetime(inai.fecha_solicitud).dt.year==2018) & (pd.to_datetime(inai.fecha_solicitud).dt.month==12)]
```

```python
plt.figure(figsize=(24,12))

g = sns.countplot(dic18.respuesta)
g.set_xticklabels(g.get_xticklabels(), rotation=70)
```

Intentemos generalizar.


## Calidad de respuesta

```python
inai.respuesta.unique().shape
```

```python
labels = inai.respuesta.unique().astype(str)
labels
```

```python
categorias = [0, 1, 0, 1, -1, 0, 0, 0, 0, -1, 0, 0, 0, -1, -1, 1, 1, 1, -1]
category_translation = dict(zip(labels, categorias))
```

```python
inai['calidad_respuesta'] = inai.respuesta.map(category_translation)
```

```python
inai.groupby(['sector', 'calidad_respuesta']).size().unstack().plot(kind='bar', stacked=True)
plt.figure(figsize=(24,12))

```

```python
g = (
    inai.assign(mes=lambda df: df.fecha_solicitud.astype(str).apply(lambda s: s[0:7]))
    .groupby(['mes', 'calidad_respuesta', 'sector'])
    .size()
    .to_frame('n')
    .reset_index(drop=False)
)
```

```python
g = g.sort_values(['mes', 'sector', 'calidad_respuesta'])
```

```python
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

```python
sectores = g.sector.unique()
```

```python
ii = pd.DataFrame(list(product(g_todas_fechas, [-1, 0, 1], sectores)))
ii.columns = ['mes', 'calidad_respuesta', 'sector']
```

```python
g = ii.merge(g, how='left').fillna(0).sort_values(['mes', 'sector', 'calidad_respuesta'])
```

```python
gg = g.groupby(['mes', 'sector']).agg({'n':'sum'}).reset_index()
gg.columns = ['mes', 'sector', 'n']
gg['calidad_respuesta'] = 2
gg.head()
```

```python
gg = pd.concat((g, gg), sort=False).sort_values(['mes', 'sector', 'calidad_respuesta'])
```

```python
plt.rcParams['figure.figsize'] = (15, 5)
sns_ch = sns.cubehelix_palette(n_colors=3, as_cmap=True)
```

```python
for i, s in enumerate(sectores):
    plt.figure(i)
    df = gg[gg.sector==s].drop('sector', axis=1)
    df = df.pivot(index='mes', columns='calidad_respuesta', values='n')
    df.columns = ['falta del solicitante', 'mala', 'buena', 'total']
    df.drop('total', axis=1, inplace=True)
    df.plot.area(colormap=sns_ch, alpha=0.75)
    plt.title(s)
```

```python
sns.relplot(x='mes',  y='n',
            row='sector', hue='calidad_respuesta',
            kind='line',
            aspect=3, 
            facet_kws={'sharey':False},
            data=g)
```

```python

```
