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

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (20, 10)
import seaborn as sns
sns.set()

import re
```


# Profiling

```python
sol = pd.read_feather('../data/inai.feather')
sol['clave_dependencia'] = sol.folio.astype(str).apply(lambda x: x[:5])
sol.sample(5)
```

### `estatus`

```python
g = sns.countplot(sol.estatus)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

```python
g = sns.countplot(sol.estatus)
g.set_yscale('log')
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')

```

### `medio_entrada`

```python
g = sns.countplot(sol.medio_entrada)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

### `tipo_solicitud`

```python
g = sns.countplot(sol.tipo_solicitud)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

### `descripción`

```python
sol.descripcion.sample(5)
```

Es la solicitud. Textimnear.


### `otros`

```python
sol.otros.sample(10)
```

No vale la pena, muy *ad hoc*.


### `archivo_adjunto`

```python
sol.loc[sol.archivo_adjunto!='nan', 'mo'].sample(10)
```

Adjuntos por el gobierno. En cualquier caso, si no son `nan` pueden ayudar a encontrar respuesta positiva o lo que signifique ADJUNTO SOLICITUD.


### `medio_entrega`

```python
g = sns.countplot(sol.medio_entrega)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

### `respuesta`

```python
g = sns.countplot(sol.respuesta)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

```python
g = sns.countplot(sol.respuesta)
g.set_yscale('log')
g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

requerimiento de información adicional: la ciudadana no dio suficiente información para satisfacer el query.

respuesta del solic... : estos están en el proceso entre "ah, necesitamos esto de ti" y que se los de. Seguramente si no lo contesta, se va a deshechado por falta de pago en estatus.


###  `archivo_respuesta`

```python
sol.loc[sol.archivo_respuesta=='nan', 'medio_entrega'].sample(10)
```

## Un poquillo de tiempo

```python
sol.iloc[0].fecha_solicitud.date()
```

```python
sol['fecha_solicitud'] = sol.fecha_solicitud.apply(lambda x: x.date())
```

```python
sol.groupby('fecha_solicitud').size()
```

```python
tseries = sol.groupby('fecha_solicitud').size()
sns.lineplot(tseries.index, tseries.values)
```

> Hacer análisis de punto de cambio.
