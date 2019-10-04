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

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
plt.rcParams['figure.figsize'] = (20, 10)

import spacy
from gensim.models import LdaMulticore
from gensim.corpora.dictionary import Dictionary

from os import mkdir
```

```python
inai = pd.read_parquet('../data/inai.parquet')[['fecha_solicitud', 'sector', 'descripcion']]
```

```python
sns.distplot(inai.descripcion.apply(len))
```

```python
inai = inai[inai.descripcion!='DESCRIPCIÓN SOLICITUD']
```

```python
sns.distplot(inai.descripcion.apply(len))
```

```python
sns.boxenplot(x='sector', y='y', 
              data=inai.assign(y=lambda df: df.descripcion.apply(len)))
```

```python
def trimestrisar(f):
    """
    trimestriza
    """
    año = f.year
    q = f.quarter
    return str(año)+'-Q'+str(q)
```

```python
inai['trimestre'] = inai.fecha_solicitud.apply(trimestrisar)
```

```python
inai.drop('fecha_solicitud', axis=1, inplace=True)
```

```python
nlp = spacy.load('es_core_news_sm')
nlp.Defaults.stop_words |= {'', 'solicito', 'atentamente', 'requiero', 'informacion',
                           'solicitamos', 'por', 'medio', 'del', 'presente', 'días',
                           'saber', 'conocer', 'proporcione', 'proporcionar', 'solicita',
                           'requiero', 'requereimos', 'quiero', 'quisiera', 'quisieramos',
                           'corresponda', 'tardes', 'noches', 
                            'a', 'e', 'i', 'o', 'u', 'y',
                           'solicitud'}
```

```python
def tokenizar(doc):
    ddoc = nlp(doc)
    tokens = [token.text.lower() for token in ddoc if not token.is_stop and token.is_alpha]
    return tokens
```

```python
inaigb = inai.groupby(['sector', 'trimestre'])
```

```python
for name, group in inaigb:
    print(name[0]+'..'+name[1])
    textos_tokenizados = [tokenizar(s) for s in group.descripcion]
    dicto = Dictionary(textos_tokenizados)
    corpus = [dicto.doc2bow(text) for text in textos_tokenizados]
    lda = LdaMulticore(corpus, id2word=dicto, num_topics=10)
    lda.show_topics()
    try:
        mkdir(f"./output/{name[1]+'..'+name[0]}")
    except FileExistsError:
        pass
    lda.save(f"./output/{name[1]+'..'+name[0]}/model")
```
