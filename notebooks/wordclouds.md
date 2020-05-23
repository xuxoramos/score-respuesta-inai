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
texto_solicitudes.groupby(['descripcion','year_solicitud'])['sector']\
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
sector_remover = ['aportaciones a seguridad social',None,'reforma agraria','trabajo y prevision social','relaciones exteriores','previsiones y aportaciones para los sistemas de educacion basica, normal, tecnologica y de adultos','consejeria juridica del ejecutivo federal']
stop_words_sp = get_stop_words('spanish')
extra_stopwords = ['solicito','solicita','informacion','cordialmente','apego','constitucion','federal','mensual','anual','amable','relacion','encuentra','ley','copia','materia','acta','adjudicacion','quisiera', 'directa','escalafon','especifica','listado','obtener','adjunto','respe','conjunto','acceso','quiero','requiero','actualmente','conocer','siguiente','siguient','articulos','fundamento','solicitamos','entregar','referente','existente','toda','formato','presente','medio','nacional','respuesta','Length','dtype','saber','informen','documento','periodo','si','Name','object','documentacion','celebrados','siguie','format','buenas','gracias','quier','tardes','dias','noches','buenos','articulo','elabora','solic','solicitudes','favor','entr','base','Name','publicos','solicitud','frac','dia','atenta','manera']
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
            stopwords=aux,
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
    plt.savefig('img/' + title + '.png', bbox_inches='tight')
    plt.show()
```

```python
for elemento in texto_solicitudes_filtered.sector.unique():
    for ano in texto_solicitudes_filtered.year_solicitud.unique():
        if elemento not in sector_remover:
            df = texto_solicitudes_filtered[(texto_solicitudes_filtered.sector == elemento) & (texto_solicitudes_filtered.year_solicitud == ano)]
            show_word_cloud(df['descripcion'], elemento + ' ' + str(ano))
```

```python

```
