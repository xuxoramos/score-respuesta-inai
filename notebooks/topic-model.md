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
import multiprocessing as mp
```

```python
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (20,10)
import seaborn as sns
sns.set()
```

```python
import spacy
from spacy.lang.es import Spanish 
from spacy.lang.es.stop_words import STOP_WORDS 
nlp = spacy.load('es_core_news_md')

plt.rcParams['figure.figsize'] = (20,10)
```

```python
from gensim.models import LdaMulticore, Phrases
from gensim.corpora import Dictionary, MmCorpus
```

```python
STOP_WORDS = STOP_WORDS.union({
    'información', 'desear', 'informacion', 
    'solicitar', 'solicitud', 'querer',
    'solicito', 'informar', 'nombrar',
    '?', '¿', '!', '¡', r'\s', ',', '.', 
    'cordial', 'saludar'})
```

```python
def is_stopword(token):
    if (not token.is_alpha) or (not token.is_digit):
        return True
    return token.is_stop or token.lower_ in STOP_WORDS or token.lemma_ in STOP_WORDS 
```

## `descripción` 

```python
inai = (
    pd.read_parquet('../data/inai.parquet')
    .drop_duplicates('descripcion')
    .pipe(lambda df: df.assign(n_desc=df.descripcion.str.len()))
    .query('n_desc > 20')
)
```

```python
g = sns.distplot(inai.n_desc)
g.set_title('Longitud de cada pregunta')
```

```python
g = sns.distplot(np.log(inai.n_desc))
g.set_title('log Longitud de cada pregunta')
```

```python
g = sns.countplot(inai.sector)
g = g.set_xticklabels(g.get_xticklabels(), rotation=30, ha='right')
```

```python
def tokenize(text):
    tokens = nlp(text)
    ttokens = [t for t in tokens if not is_stopword(t)]
    return ttokens
```

```python
inai.descripcion.index
```

```python
tokenize(inai.descripcion.[5])
```

```python
res = map(tokenize, inai.descripcion)
```

```python
with open('../output/tokenized_desc.pkl', 'wb') as f:
    pkl.dump(res, f)
```

## Clasificador

```python
dictionary = Dictionary()
corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in res]
dictionary.save('../output/dict.dict')
MmCorpus.serialize('../output/corpus.mm', corpus)
```

```python
with open('../output/bigrams.pkl', 'wb') as f:
    pkl.dump(bigram, f)
```

```python
lda1 = LdaMulticore(corpus=corpus,
                    num_topics=50,
                    id2word=dictionary,
                    workers=3,
                    chunksize=2000,
                    passes=2,
                    eval_every=10
                   )
```

```python
lda1.save('../output/lda1.mm')
```

```python
for idx, topic in lda1.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic ))
    print("\n")
```

---

```python
bigram = Phrases(res, min_count=15)
for idx in range(len(res)):
    for token in bigram[res[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            res[idx].append(token)
```

```python
# Create a dictionary representation of the documents.
dictionary = Dictionary(res)

# Filter out words that occur less than 20 documents, or more than 50% of the documents.
dictionary.filter_extremes(no_below=20, no_above=0.5)
```

```python
corpus = [dictionary.doc2bow(r) for r in res]
dictionary.save('../output/dict2.dict')
MmCorpus.serialize('../output/corpus2.mm', corpus)
```

```python
lda2 = LdaMulticore(corpus=corpus,
                    num_topics=25,
                    id2word=dictionary,
                    workers=3,
                    chunksize=2000,
                    passes=2,
                    eval_every=10
                   )
lda2.save('../output/lda2.mm')
```

```python
for idx, topic in lda2.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic ))
    print("\n")
```

```python

```
