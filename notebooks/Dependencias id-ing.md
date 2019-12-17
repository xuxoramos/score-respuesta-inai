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
import re

import pandas as pd
```

Abrimos una versión simplificada del [Padrón de sujetos obligados](http://inicio.inai.org.mx/nuevo/Padron_Sujetos_Obligados.pdf) publicado por el INAI

```python
with open("../data/padron_simple.txt", "r") as infile: 
    text = infile.read()
```

```python
dpndencias = pd.DataFrame(columns=["Dependencia", "uID"])
splitted = re.findall("(\d{5}\s.*)", text)
for match in splitted: 
    match = match.split("\n")
    
    dpndencias = dpndencias.append({"Dependencia": match[1],
                      "uID": match[0]}, ignore_index=True)
    
dpndencias.set_index('uID', inplace=True)

dpndencias.head()
```

```python
dpndencias.reset_index(drop=True).to_feather('../data/ids_dependencias.feather')
```
