---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.0'
      jupytext_version: 0.8.6
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Profiling

```python
import numpy as np
import pandas as pd
from glob import glob
```

```python
files = [f for f in glob('../data/*.xls')]
years = [f[-8:-4] for f in files]
sol = [pd.read_excel(f) for f in files]
```

```python
sol = map(
    lambda y, df: df.assign(anio=int(y)),
    years, sol
)
sol = pd.concat(sol)
```

```python
sol.head()
```

```python
sol.columns = [
    'folio',
    'fecha_solicitud',
    'dependencia',
    'estatus',
    'medio_entrada',
    'tipo_solicitud',
    'descripcion',
    'otros',
    'archivo_adjunto',
    'medio_entrega',
    'fecha_limite',
    'respuesta',
    'texto_respuesta',
    'archivo_respuesta', 
    'fecha_respuesta',
    'pais',
    'estado',
    'municipio',
    'codigo_postal',
    'sector',
    'año'
]
```

```python
sol.describe(include='all')
```

```python
sol.dtypes
```

```python
sol['fecha_solicitud'] = pd.to_datetime(sol['fecha_solicitud'])
sol['dependencia'] = sol['dependencia'].astype(str)
sol['estatus'] = sol['estatus'].astype('category')
```

```python

```
