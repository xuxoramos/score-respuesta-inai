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
from glob import glob

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (20, 10)
import seaborn as sns
sns.set()
```


# Análisis exploratorio

```python
sol = pd.read_feather('../data/inai.feather')
sol.head()
```

```python
g = sns.countplot(sol.estatus)
g.set_yscale('log')
g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

Cuando una persona hace una solicitud, queda en proceso. 

```python
sol.fecha_solicitud.max()
```

```python
sol.fecha_solicitud.max()
```

```python
sol.fecha_solicitud.apply(lambda x: x.month).max()
```

```python
sol.groupby('año').size()
```

```python

```

```python

```
