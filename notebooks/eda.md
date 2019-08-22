---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.1.7
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
import numpy as np
import pandas as pd
np.set_printoptions(threshold=20000)
pd.options.display.max_columns = None

from itertools import product

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (20, 10)
import seaborn as sns
sns.set()

import re
```


# Vista rápida

```python
inai = pd.read_parquet('../data/inai.parquet')
inai.sample(5)
```

```python
for col in ['fecha_solicitud', 'fecha_respuesta', 'fecha_limite']:
    inai[col] = pd.to_datetime(inai[col])
```

### `estatus`

```python
g = sns.countplot(inai.estatus)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

```python
g = sns.countplot(inai.estatus)
g.set_yscale('log')
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

### `medio_entrada`

```python
g = sns.countplot(inai.medio_entrada)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

### `tipo_solicitud`

```python
g = sns.countplot(inai.tipo_solicitud)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

```python
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
g = sns.countplot(inai.medio_entrega)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

### `respuesta`

```python
g = sns.countplot(inai.respuesta)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

```python
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
tseries = inai.groupby('fecha_solicitud').size()
sns.lineplot(tseries.index, tseries.values)
```

```python
tseries[tseries.values > 3000]
```

```python
inai['semana_solicitud'] = inai.fecha_solicitud.dt.week
inai['por_semana_sol'] = inai.año.astype(str) + '-' + inai.semana_solicitud.astype(str)
inai['mes_solicitud'] = inai.fecha_solicitud.dt.month
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

```python
iii = pd.DataFrame(product(todos_meses, inai.sector.unique()))
```

```python
iii.columns = ['todos-meses', 'sector']
```

```python
tseries = inai.groupby(['por_mes_sol', 'sector']).size().to_frame('n').reset_index()
tseries = iii.merge(tseries, how='left')
```

```python
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

```python
inai['tiempo_respuesta'] = (inai.fecha_respuesta - inai.fecha_solicitud).dt.days
inai['demora'] = (inai.fecha_respuesta - inai.fecha_limite).dt.days
```

```python
sns.distplot(inai.tiempo_respuesta, kde=False)
```

```python
inai.sort_values('demora', ascending=False)
```

```python
sns.distplot(inai.demora.dropna(), kde=False)
```

```python
tseries = inai.groupby(['por_mes_sol', 'sector']).agg({'demora':np.mean}).reset_index()
```

```python
iii.columns = ['por_mes_sol', 'sector']
```

```python
tseries = iii.merge(tseries, how='left')
```

```python
tseries['demora'] = tseries.demora.fillna(0)
```

```python
sns.relplot(x='por_mes_sol', y='demora', 
            row='sector', 
            kind='line',
            height = 3,
            aspect = 7,
            data=tseries)
```
