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
import pickle as pkl
np.set_printoptions(threshold=20000)
```

```python
sol = pd.read_parquet('../data/inai.parquet')
sol.head()
```

```python
sol['clave_dependencia'] = sol.folio.apply(lambda s: '0'*(13-len(str(s)))+str(s)).apply(lambda s: s[:5])
```

```python
dd = pd.read_csv('../data/diccionario_dependencias.csv').drop('Unnamed: 0', axis=1)
dd['clave_dependencia'] = dd.clave_dependencia.apply(lambda s: '0'*(5-len(str(s)))+str(s)).apply(lambda s: s[:5])
```

```python
sol = sol.drop('dependencia', axis=1).merge(dd)
```

```python
sol.to_parquet('../data/inai.parquet', engine='pyarrow')
```
