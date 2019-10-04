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
sol = [pd.concat(pd.read_excel(f, sheet_name=None, dtypes={'FOLIO':str}).values()) for f in files]
```

```python
sol = map(
    lambda y, df: df.assign(anio=int(y)),
    years, sol
)
```



```python
sol = pd.concat(list(sol)).reset_index(drop=True)
```

```python
df = pd.read_excel(files[0], dtypes={'FOLIO': object})
df.head()
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
sol.respuesta.nunique()
```

```python
sol.loc[sol.codigo_postal=='680O0', 'codigo_postal'] = '68000'
```

```python
# Fechas 
for c in ['fecha_solicitud', 'fecha_limite', 'fecha_respuesta']:
    sol[c] = pd.to_datetime(sol[c], errors='coerce')

# Categorías 
for c in ['dependencia', 'estatus', 'medio_entrada', 'tipo_solicitud', 
          'medio_entrega', 'pais', 'estado', 'municipio', 'sector',
          'respuesta']:
    sol[c] = sol[c].astype("category")
    
# Textos
for c in ['descripcion', 'otros', 'archivo_adjunto', 'texto_respuesta',
         'archivo_respuesta']:
    sol[c] = sol[c].astype(str)
    
# double
sol['codigo_postal'] = pd.to_numeric(
                        sol.codigo_postal.replace(
                            to_replace=r'[Oo]', 
                            value='0', 
                            regex=True),
                        errors='coerce')
    
sol.dtypes
```

```python
sol.describe(include="all")
```

```python
<<<<<<< HEAD
 sol.reset_index(drop=True).to_feather('../data/inai.feather')
```

```python

=======
sol.reset_index(drop=True).to_parquet('../data/inai.parquet', engine='pyarrow')
>>>>>>> exploratorio
```
