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

Limpiamos todos los datos 

```python
# Fechas 
sol["fecha_solicitud"] = pd.to_datetime(sol["fecha_solicitud"])
sol["fecha_limite"] = pd.to_datetime(sol["fecha_limite"])
sol["fecha_respuesta"] = pd.to_datetime(sol["fecha_respuesta"])

# Categorías 
sol["dependencia"] = sol["dependencia"].astype("category")
sol["estatus"] = sol["estatus"].astype("category")
sol["medio_entrada"] = sol["medio_entrada"].astype("category")
sol["tipo_solicitud"] = sol["tipo_solicitud"].astype("category")
sol["medio_entrega"] = sol["medio_entrega"].astype("category")
sol["pais"] = sol["pais"].astype("category")
sol["estado"] = sol["estado"].astype("category")
sol["municipio"] = sol["municipio"].astype("category")
sol["sector"] = sol["sector"].astype("category")

sol.dtypes
```

```python
sol.describe(include="all")
```

```python

```
