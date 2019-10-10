---
jupyter:
  jupytext:
    cell_metadata_filter: ExecuteTime,autoscroll,-hide_output
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.2.4
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
sns.set()

import re

import warnings
warnings.filterwarnings('ignore')
```


<!-- #region -->
# La importancia de la transparencia 

Una frase que escuchamos mucho es que como ciudadanos tenemos derechos y obligaciones. Entre los derechos bien conocidos están el derecho a la libertad de pensamiento y expresión, derecho a la educación, salud, vivienda, y muchos más. Hoy hablaremos de un derecho que no todos ejercemos, pero cuya popularidad e importancia va al alza: derecho de acceso a la información. La Comisión Nacional de Derechos Humanos establece que "el Estado debe garantizar el derecho de las personas para acceder a la información pública, buscar, obtener y difundir libremente la información...". El acceso a la información es una herramienta para fomentar la transparencia en la gestión pública, y así poder mejorar la calidad de nuestra democracia. El INAI (Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales) es el organismo encargado de que tengamos acceso a la información pública y podamos proteger nuestros datos personales.


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

## Vista rápida de las solicitudes


Contamos con datos de solicitudes del 1 de enero del 2012 al 30 de junio del 2019. Esto equivale a un total **1'395,851** preguntas. Si asumimos que hay una pregunta por persona, es como si toda la población de Trinidad y Tobago hubiera hecho solicitudes de información. O bien,  siguiendo la misma lógica, el número de solicitudes equivale al 1.09% de nuestra población. 

<!-- #region -->
Curiosamente, no todas las preguntas fueron realizadas desde México, sino que el estado y municipio reportado por los solicitantes es muy variado. Por ejemplo, incluso hay una solicitud desde Zimbabwe y Mauricio.

Naturalmente, México es el país de 99.44% de las solicitudes, pero también hay solicitudes de los siguientes países: 

+ El 0.24% viene de Estados Unidos


+ El 0.05% viene de Reino Unido 


+ El 0.05% viene de Canadá


+ El 0.03% viene de España


+ El 0.02% viene de Rusia 

Dado que el estado y municipio son reportados por el usuario tenemos solicitudes desde las alcaldías de Ciudad de México hasta "COLEGIO HOGWARTS DE MAGIA Y HECHICERÍA" en el Reino Unido. Claramente, la creatividad de los mexicanos ante un campo de datos abierto no podía faltar. 

Veamos cómo se ve el número de solicitudes por año y mes.

<!-- #endregion -->

```python tags=["to_remove"]
pais_count = inai.groupby('pais')['folio'].count().reset_index()

pais_count = pais_count.sort_values(by = 'folio', ascending = False)

pais_count ['prop'] = (pais_count.folio / pais_count.folio.sum()) * 100
#pais_count
```

```python tags=["to_remove"]
#inai[inai.pais == 'México'].estado.value_counts()
```

```python tags=["to_remove"]
# inai[inai.pais != 'México']
```

```python tags=["to_remove"]
year_count = inai.groupby('year_solicitud')['folio'].count().reset_index()
#year_count
plt.figure(figsize=(18, 9))

plt.plot(year_count.index, year_count.folio)
plt.xticks([0, 1,2,3,4,5,6,7], ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"])
plt.ylim([0, 280000])

plt.yticks([0, 50000, 100000, 150000, 200000, 250000],
          ["0", "50,000", "100,000", "150,000", "200,000", "250,000"])
plt.xlabel('Año')
plt.ylabel('Número de solicitudes por año')
plt.show()
```

El número de solicitudes totales por año fue aumentando poco a poco del 2012 al 2017, año en que alcanzó su punto máximo, y después disminuyó. De hecho los 3 días en que más solicitudes hubo fueron el 8 de febrero 2017, 9 de febrero del 2017 y el 21 de febrero del 2017. Las solicitudes hechas en esos días son de diversos temas, pero un interés recurrente es conocer el sueldo de los funcionarios públicos. 

Para conocer un poco más el detalle del número de solicitudes, ahora vemos cómo se ven las solicitudes por mes y año.

```python tags=["to_remove"]
fecha_count = inai.groupby('fecha_solicitud')['folio'].count().reset_index()
fecha_count = fecha_count.sort_values(by = 'folio', ascending = False)
```

```python tags=["to_remove"]
top_fechas = inai[inai.fecha_solicitud.isin(fecha_count.fecha_solicitud.head(3))]

# top_fechas.sector.value_counts()
```

```python tags=["to_remove"]
count = inai.groupby(['year_solicitud', 'mes_solicitud'])['folio'].count().reset_index()
# count.head()
```

```python tags=["to_remove"]
plt.figure(figsize=(18, 9))

plt.plot(count.folio)
plt.xticks([0,12,24,36,48,60,72, 84], ["2012", "2013", "2014","2015",
                                   "2016","2017", "2018", "2019"])
plt.xlabel('Número de solicitudes por mes y año')
plt.ylabel('Año')
plt.show()
```

Al analizar el número de solicitudes por mes y año podemos ver un patrón interesante: el número de preguntas baja en los meses finales del año y luego aumenta al inicio del año siguiente. Las combinaciones de mes-año con mayor número de preguntas fueron febrero 2017 y octubre 2018. 

Ya que conocemos cómo ha cambiado el número de solicitudes por mes y año ahora vamos a conocer (a grandes rasgos) los sectores y las dependencias de las que preguntan los solicitantes.


Una vez que las solicitudes son revisadas se les asigna un sector y una dependencia. En las solicitudes que aquí estudiamos hay 26 sectores distintos y 858 dependencias. El sector con el mayor número de solicitudes es "Aportaciones a Seguridad Social".  

```python tags=["to_remove"]
count_sector = inai.groupby('sector')['folio'].count().reset_index()
count_sector = count_sector.sort_values(by = 'folio', ascending = False).reset_index()
count_sector['prop'] = (count_sector.folio / count_sector.folio.sum()) * 100
count_sector = count_sector.drop(columns = ['index'])
#count_sector
```

```python tags=["to_remove"]
plt.figure(figsize=(40, 50))

plt.barh(count_sector.sector, count_sector.prop)

plt.yticks(size = 35)
plt.xticks(size = 38)
plt.xlabel('Proporción de solicitudes %', size = 40)

plt.show()
```

Ahora bien, como hay 858 dependencias distintas solo vamos a enseñar aquellas que acumulan el **50%** de las solicitudes. 

```python tags=["to_remove"]
count_dep = inai.groupby('dependencia')['folio'].count().reset_index()
count_dep = count_dep.sort_values(by = 'folio', ascending = False).reset_index()
count_dep = count_dep.drop(columns = ['index'])
count_dep['prop'] = (count_dep.folio /  count_dep.folio.sum())*100
count_dep['cum_prop'] = count_dep.prop.cumsum()

count_dep_filter = count_dep[count_dep.cum_prop < 51]
```

```python tags=["to_remove"]
# count_dep_filter
```

```python tags=["to_remove"]
plt.figure(figsize=(40, 50))

plt.barh(count_dep_filter.dependencia, count_dep_filter.prop)

plt.yticks(size = 35)
plt.xticks(size = 38)
plt.xlabel('Proporción de solicitudes %', size = 40)

plt.show()
```

Hay 15 dependencias que acumulan el 50% de todas las solicitudes. Las solicitudes de información al IMSS representan el 17.4% de todas las solicitudes. Podemos ver que hay congruencia entre el número de preguntas por sector y dependencia.

Ya que vimos a grandes rasgos de qué sector vienen las solicitudes, vamos a analizar el medio de entrada. 

```python tags=["to_remove"]
count_medio = inai.groupby('medio_entrada')['folio'].count().reset_index()
count_medio['prop'] = (count_medio.folio / count_medio.folio.sum()) * 100
# count_medio
```

```python tags=["to_remove"]
plt.figure(figsize=(18, 9))

plt.bar(count_medio.medio_entrada, count_medio.prop)
plt.xlabel('Medio de entrada')
plt.ylabel('Proporción de Solicitudes %')
plt.show()
```

Cerca del 96% de las solicitudes se realizaron por medio electrónico. Aunque no es totalmente sorprendente (dada la burocracia que sigue presente en todos los trámites de gobierno), sí llama la atención que alrededor de 56 mil solicitudes se hicieron por medios manuales. Vamos a conocerlas un poco más. 

```python tags=["to_remove"]
manuales = inai[inai.medio_entrada == 'Manual']
 
```

```python tags=["to_remove"]
manual_dependencia = (
    manuales
    .groupby('dependencia')['folio']
    .count()
    .reset_index()
    .sort_values(by = 'folio', ascending = False) 
).reset_index()

manual_dependencia['prop'] = (manual_dependencia.folio / manual_dependencia.folio.sum()) * 100
manual_dependencia['prop_cum'] = manual_dependencia.prop.cumsum()
#manual_dependencia
```

```python tags=["to_remove"]
#manual_dependencia.head(7).dependencia.unique()
```

<!-- #region -->
El 50% de las solicitudes manuales corresponden a 7 dependencias: 

1. Hospital Regional de Alta Especialidad de Ixtapaluca con 12.15% 


2. Instituto Mexicano del Seguro Social con 11.39% 


3. Instituto de Seguridad y Servicios Sociales de los Trabajadores del Estado con 7.32%


4. Instituto Nacional de Ciencias Médicas y Nutrición Salvador Zubirán con 5.34%


5. Procuraduría Federal de la Defensa del Trabajo coon 4.74%


6. Consejo de la Judicatura Federal con 3.91%


7. Suprema Corte de Justicia de la Nación con 3.58%


<!-- #endregion -->

El 99% de las solicitudes tuvieron origen en México, en especial en la Ciudad de México. Analicemos el tipo de solicitud de las consultas hechas a mano: 

```python tags=["to_remove"]
manual_tipo_sol = (
    manuales
    .groupby('tipo_solicitud')['folio']
    .count()
    .reset_index()
    .sort_values(by = 'folio', ascending = False) 
).reset_index()

manual_tipo_sol['prop'] = (manual_tipo_sol.folio / manual_tipo_sol.folio.sum()) * 100
manual_tipo_sol['prop_cum'] = manual_tipo_sol.prop.cumsum()
# manual_tipo_sol
```

```python tags=["to_remove"]
plt.figure(figsize=(18, 9))

plt.bar(manual_tipo_sol.tipo_solicitud, manual_tipo_sol.prop)
plt.xlabel('Tipo de solicitud')
plt.ylabel('Proporción de Solicitudes Manuales%')
plt.show()
```

De las solicitudes manuales el 51.42% son para solicitar información pública, 45.25% es de datos personales y 3.32% es de corrección de dato personales. Vamos a contrastar esto con las solicitudes realizadas de manera electrónica. 

```python tags=["to_remove"]
ts = (
    inai[inai.medio_entrada != 'Manual']
    .groupby('tipo_solicitud')['folio']
    .count()
    .reset_index()
    .sort_values(by = 'folio', ascending = False) 
).reset_index()

ts['prop'] = (ts.folio / ts.folio.sum()) * 100
ts['prop_cum'] = ts.prop.cumsum()
#ts
```

```python tags=["to_remove"]
plt.figure(figsize=(18, 9))

plt.bar(ts.tipo_solicitud, ts.prop)
plt.xlabel('Tipo de solicitud')
plt.ylabel('Proporción de Solicitudes Electrónicas%')
plt.show()
```

Diferente a lo observado en las solicitudes manuales, el 80.90% de las solicitudes electrónicas son para solicitar información pública, 18.99% son sobre datos personales y 0.09% son para la corrección de datos personales. 

El tipo de solicitud sí cambia según el medio de entrada pues en las consultas manuales hay un mayor balance entre solicitudes de información pública y de datos personales. Además, hay un mayor porcentaje de corrección de datos personales en las solicitudes manuales. 

El medio de entrega también cambia según el medio de entrada. 


```python tags=["to_remove"]
count_medio_entrega = inai.groupby(['medio_entrada','medio_entrega'])['folio'].count().reset_index()

count_medio.rename(columns = {'folio':'total'}, inplace = True)

count_medio_entrega = count_medio_entrega.merge(count_medio[['medio_entrada', 'total']])
count_medio_entrega['prop_medio'] = (count_medio_entrega.folio / count_medio_entrega.total) * 100
# count_medio_entrega
```

```python tags=["to_remove"]
#plt.figure(figsize=(100, 100))

g = sns.FacetGrid(count_medio_entrega, col="medio_entrada", height = 5, aspect = 2)

g = (g.map(plt.bar, "medio_entrega", "prop_medio")
    .set(ylim=(0, 100))
    .set_xticklabels(rotation=50, ha='right')
    .set_axis_labels("Medio Entrega", "Proporción de solicitudes %"))

plt.show()
```

Podemos ver que el medio de entrega más popular en el medio Eléctronico es Entrega por Internet en la "PNT" (Plataforma Nacional de Transparencia), mientras que las solicitudes manuales la entrega más común es "Otro Medio". Aunque no lo podemos apreciar, hubo 709 solicitudes (0.05% de las solicitudes Electrónicas) que se entregaron de forma "Verbal". 

Ya que conocemos la forma en que se entregan las respuestas, hay que conocer cuáles son las respuestas otorgadas por el INAI. 

```python tags=["to_remove"]
count_resp = inai.groupby('respuesta')['folio'].count().reset_index()
count_resp = count_resp.sort_values(by = 'folio', ascending = False).reset_index()
count_resp['prop'] = (count_resp.folio / count_resp.folio.sum()) * 100
count_resp = count_resp.drop(columns = ['index'])
# count_resp
```

```python tags=["to_remove"]
plt.figure(figsize=(40, 50))

plt.barh(count_resp.respuesta, count_resp.prop)

plt.yticks(size = 35)
plt.xticks(size = 38)
plt.xlabel('Proporción de solicitudes %', size = 40)

plt.show()
```

<!-- #region -->
Podemos observar que las respuestas registradas no son específicas a las solicitudes, sino que más bien reflejan el estatus de la solicitud o la forma en que fue entregada. La respuesta más común es que la entrega se dio por medio de un archivo electrónico, que es muy congruente con lo que vimos en el medio de entrega. 

Hay respuestas que indican que al solicitante le faltó un paso extra: 

+ Requerimiento de información adicional


+ Notificación de pago


+ No es de competencia de la unidad de enlace



Hay respuestas que nos intrigan: 

+ La solicitud no corresponde al marco de la Ley


+ Inexistencia de la información solicitada


+ Negativa por ser reservada o confidencial


+ Información parcialmente reservada o confidencial


+ No se dará trámite a la solicitud


Más adelante haremos un análisis detallado sobre las preguntas que dieron lugar a las respuestas que nos intrigan. Con una vista muy rápida pudimos notar que los solicitantes hacían preguntas *muy específicas* (productos de madera, acceso a Internet, calentadores, minutas de reuniones, etc.), y es importante resaltar que muchas de estas preguntas buscaban conocer sobre contratos celebrados entre organismos o la marca de coche y renumeración de los servidores públicos. Pudimos ver también que una porción importante de estas preguntas eran sobre los candidatos presidenciales para las elecciones del 2018. 
<!-- #endregion -->

```python tags=["to_remove"]
intriga = inai[inai.respuesta.isin(['La solicitud no corresponde al marco de la Ley ',
                          'Inexistencia de la información solicitada',
                         'Negativa por ser reservada o confidencial', 
                         'Información parcialmente reservada o confidencial', 
                         'No se dará trámite a la solicitud'])]

intriga = intriga[['tipo_solicitud', 'descripcion', 'respuesta', 'texto_respuesta']]

#intriga.to_csv('intriga.csv')
```

Ahora bien, regresando un poquito al tema de las respuestas, un campo que está muy relacionado con la respuesta a las solicitudes es el estatus de la solicitud. 

```python tags=["to_remove"]
count_est = inai.groupby('estatus')['folio'].count().reset_index()
count_est = count_est.sort_values(by = 'folio', ascending = False).reset_index()
count_est['prop'] = (count_est.folio / count_est.folio.sum()) * 100
count_est = count_est.drop(columns = ['index'])
# count_est
```

```python
count_est
```

```python tags=["to_remove"]
plt.figure(figsize=(40, 50))

plt.barh(count_est.estatus, count_est.prop)

plt.yticks(size = 35)
plt.xticks(size = 38)
plt.xlabel('Proporción de solicitudes %', size = 40)

plt.show()
```

<!-- #region -->
El 87% de las solicitudes se cuentan como terminadas. El resto de las solicitudes siguen en proceso, están esperando a un pago o respuesta del ciudadano, o fueron rechazadas. Como las claves identificadoras de las solicitudes son únicas, realmente no hay forma de saber si las solicitudes "en proceso" o "en espera" sí se concluyeron o no.






Como no hay una forma muy clara de conocer si al final todas las solicitudes sí se completaron 

<!-- #endregion -->

```python

```

```python

```

```python

```

```python

```

## Un poquillo de tiempo

```python ExecuteTime={"end_time": "2019-08-22T04:29:06.689370Z", "start_time": "2019-08-22T04:29:05.689563Z"}
plt.figure(figsize=(18, 9))

tseries = inai.groupby('fecha_solicitud').size()
sns.lineplot(tseries.index, tseries.values)
```

```python ExecuteTime={"end_time": "2019-08-22T04:29:10.070971Z", "start_time": "2019-08-22T04:29:10.064338Z"}
tseries[tseries.values > 3000]
```

```python
#inai['year_solicitud'] =  pd.to_datetime(inai['fecha_solicitud']).dt.year

```

```python ExecuteTime={"end_time": "2019-08-22T10:54:06.839654Z", "start_time": "2019-08-22T10:54:02.184090Z"}
inai['semana_solicitud'] = pd.to_datetime(inai['fecha_solicitud']).dt.week
inai['por_semana_sol'] = inai.año.astype(str) + '-' + inai.semana_solicitud.astype(str)
inai['mes_solicitud'] = pd.to_datetime(inai['fecha_solicitud']).dt.month
inai['por_mes_sol'] = inai.año.astype(str) + '-' + inai.mes_solicitud.astype(str)
```

```python ExecuteTime={"end_time": "2019-08-22T10:59:26.263381Z", "start_time": "2019-08-22T10:59:26.259391Z"}
todos_meses = []
for year in range(2012, 2020):
    y = str(year)
    for month in range(1, 13):
        m = str(month)
        todos_meses.append(y+'-'+m)
```

### Respuestas por año-mes

```python ExecuteTime={"end_time": "2019-08-22T10:58:53.993957Z", "start_time": "2019-08-22T10:58:53.859830Z"}
respuestas = inai.respuesta.unique()
```

```python ExecuteTime={"end_time": "2019-08-22T10:58:54.574251Z", "start_time": "2019-08-22T10:58:54.571499Z"}
from itertools import product
```

```python ExecuteTime={"end_time": "2019-08-22T10:59:29.342988Z", "start_time": "2019-08-22T10:59:29.338391Z"}
ii = pd.DataFrame(list(product(respuestas, todos_meses)))
```

```python ExecuteTime={"end_time": "2019-08-22T10:59:41.485775Z", "start_time": "2019-08-22T10:59:41.482379Z"}
ii.columns = ['respuesta', 'por_mes_sol']
```

```python ExecuteTime={"end_time": "2019-08-22T11:05:45.436715Z", "start_time": "2019-08-22T11:05:40.941523Z"}
plt.figure(figsize=(22, 11))


tseries = inai.groupby(['por_mes_sol', 'respuesta']).size().to_frame('n').reset_index()
tseries = ii.merge(tseries, how='left').fillna(0)
sns.lineplot(tseries.por_mes_sol, tseries.n, hue=tseries.respuesta)


```

```python ExecuteTime={"end_time": "2019-08-22T11:06:20.422830Z", "start_time": "2019-08-22T11:06:00.013853Z"}
sns.relplot(x='por_mes_sol', y='n', 
            row='respuesta', 
            kind='line',
            height = 3,
            aspect = 7,
            data=tseries)
```

### Número de solicitudes año-mes-respuesta

```python
count_resp =  inai.groupby(['year_solicitud', 'mes_solicitud','respuesta'])['folio'].count().reset_index()
count_resp['mes_solicitud'] =  count_resp.mes_solicitud.map("{:02}".format)
count_resp['period'] = count_resp.year_solicitud.map(str) + '-' + count_resp.mes_solicitud.map(str)

count_resp
```

```python
count_resp_pivot = count_resp.pivot(index= 'period', 
                  columns = 'respuesta', values = 'folio')

count_resp_pivot
```

```python
plt.figure(figsize=(18, 9))

plt.plot(count_resp_pivot)
plt.legend(count_resp_pivot.columns, loc=2, prop={'size': 7})
plt.xticks(rotation = 70, size = 6.5)
#plot.legend()
plt.figure(figsize=(24,12))
plt.show()
```

```python

```

### Número de solicitudes por año-mes-sector

```python
count_sector =  inai.groupby(['year_solicitud', 'mes_solicitud','sector'])['folio'].count().reset_index()
count_sector['mes_solicitud'] =  count_sector.mes_solicitud.map("{:02}".format)
count_sector['period'] = count_sector.year_solicitud.map(str) + '-' + count_sector.mes_solicitud.map(str)

count_sector
```

```python
count_sect_pivot = count_sector.pivot(index= 'period', 
                  columns = 'sector', values = 'folio')

count_sect_pivot
```

```python
plt.figure(figsize=(24,12))

plt.plot(count_sect_pivot)
plt.legend(count_sect_pivot.columns, loc=2, prop={'size': 7})
plt.xticks(rotation = 70, size = 6.5)
#plot.legend()

plt.show()
```

```python
from itertools import product
```

```python ExecuteTime={"end_time": "2019-08-22T11:11:37.384799Z", "start_time": "2019-08-22T11:11:37.289222Z"}
#iii = pd.DataFrame(product(todos_meses, inai.sector.unique()))

iii = pd.DataFrame(list(product(todos_meses, inai.sector.unique())))
```

```python ExecuteTime={"end_time": "2019-08-22T11:11:56.356519Z", "start_time": "2019-08-22T11:11:56.353180Z"}
iii.columns = ['todos-meses', 'sector']
```

```python ExecuteTime={"end_time": "2019-08-22T11:17:54.548719Z", "start_time": "2019-08-22T11:17:54.283847Z"}
tseries = inai.groupby(['por_mes_sol', 'sector']).size().to_frame('n').reset_index()
tseries = iii.merge(tseries, how='left')
```

```python ExecuteTime={"end_time": "2019-08-22T11:18:31.399815Z", "start_time": "2019-08-22T11:17:54.950985Z"}
plt.figure(figsize=(24,12))

sns.lineplot(tseries.por_mes_sol, tseries.n, hue=tseries.sector)
```

```python ExecuteTime={"end_time": "2019-08-22T11:19:30.428894Z", "start_time": "2019-08-22T11:18:35.155661Z"}
sns.relplot(x='por_mes_sol', y='n', 
            row='sector', 
            kind='line',
            height = 3,
            aspect = 7,
            data=tseries)
```

> Hacer análisis de punto de cambio.


## Eficiencia

```python ExecuteTime={"end_time": "2019-08-25T17:52:37.237185Z", "start_time": "2019-08-25T17:52:37.232369Z"}
inai.columns
```

## Tiempo de respuesta

```python ExecuteTime={"end_time": "2019-08-25T17:52:52.241735Z", "start_time": "2019-08-25T17:52:46.096401Z"}
inai['tiempo_respuesta'] = (inai.fecha_respuesta - inai.fecha_solicitud).dt.days
```

```python ExecuteTime={"end_time": "2019-08-25T17:53:04.386949Z", "start_time": "2019-08-25T17:53:03.734656Z"}
plt.figure(figsize=(24,12))

sns.distplot(inai.tiempo_respuesta, kde=False)
```

```python ExecuteTime={"end_time": "2019-08-25T17:53:06.825904Z", "start_time": "2019-08-25T17:53:06.118368Z"}
plt.figure(figsize=(24,12))


sns.distplot(inai.tiempo_respuesta, 
             kde=False,
             hist_kws={'cumulative':True})
```

```python ExecuteTime={"end_time": "2019-08-25T17:53:09.099271Z", "start_time": "2019-08-25T17:53:09.059564Z"}
inai.tiempo_respuesta.quantile(q=[0.95, 0.975, 0.99, 0.999])
```

```python ExecuteTime={"end_time": "2019-08-25T17:53:11.374781Z", "start_time": "2019-08-25T17:53:10.676332Z"}
plt.figure(figsize=(24,12))

sns.distplot(inai.tiempo_respuesta[inai.tiempo_respuesta < 141], 
             kde=False, norm_hist=True)
```

```python ExecuteTime={"end_time": "2019-08-25T17:53:37.717203Z", "start_time": "2019-08-25T17:53:17.573833Z"}
plt.figure(figsize=(24,12))

g = sns.catplot(y='tiempo_respuesta', x='sector',
            kind='boxen',
            aspect=5,
            data=inai[inai.tiempo_respuesta<141].sort_values('tiempo_respuesta'))
g = g.set_xticklabels(rotation=90)
```

```python ExecuteTime={"end_time": "2019-08-25T17:58:04.882554Z", "start_time": "2019-08-25T17:58:04.877231Z"}
inai.dtypes
```

```python ExecuteTime={"end_time": "2019-08-25T18:11:23.462925Z", "start_time": "2019-08-25T18:10:57.863200Z"}
plt.figure(figsize=(24,12))


sns.relplot(x='fecha_solicitud', y='tiempo_respuesta', 
            row='sector',
            estimator='mean',
            ci='sd',
            kind='line',
            facet_kws={'sharey': False, 'sharex': True},
            aspect=3,
            data=inai)
```

En casi todos los sectores, el tiempo medio de respuesta va a la baja con respecto al inicio del año. En el último mes de 2018 hay muchos ceros. A ver qué dice calidad.

```python ExecuteTime={"end_time": "2019-08-25T18:21:48.609479Z", "start_time": "2019-08-25T18:21:48.254693Z"}
dic18 = inai[(pd.to_datetime(inai.fecha_solicitud).dt.year==2018) & (pd.to_datetime(inai.fecha_solicitud).dt.month==12)]
```

```python ExecuteTime={"end_time": "2019-08-25T18:25:54.841370Z", "start_time": "2019-08-25T18:25:54.319876Z"}
plt.figure(figsize=(24,12))

g = sns.countplot(dic18.respuesta)
g.set_xticklabels(g.get_xticklabels(), rotation=70)
```

Intentemos generalizar.


## Calidad de respuesta

```python ExecuteTime={"end_time": "2019-08-25T18:35:37.138926Z", "start_time": "2019-08-25T18:35:36.600800Z"}
inai.respuesta.unique().shape
```

```python ExecuteTime={"end_time": "2019-08-25T18:36:31.278566Z", "start_time": "2019-08-25T18:36:31.140534Z"}
labels = inai.respuesta.unique().astype(str)
labels
```

```python ExecuteTime={"end_time": "2019-08-25T18:46:16.887278Z", "start_time": "2019-08-25T18:46:16.883702Z"}
categorias = [0, 1, 0, 1, -1, 0, 0, 0, 0, -1, 0, 0, 0, -1, -1, 1, 1, 1, -1]
category_translation = dict(zip(labels, categorias))
```

```python ExecuteTime={"end_time": "2019-08-25T18:46:34.656737Z", "start_time": "2019-08-25T18:46:34.514717Z"}
inai['calidad_respuesta'] = inai.respuesta.map(category_translation)
```

```python ExecuteTime={"end_time": "2019-08-25T19:08:51.288810Z", "start_time": "2019-08-25T19:08:49.939565Z"}
inai.groupby(['sector', 'calidad_respuesta']).size().unstack().plot(kind='bar', stacked=True)
plt.figure(figsize=(24,12))

```

```python ExecuteTime={"end_time": "2019-08-25T21:34:46.293434Z", "start_time": "2019-08-25T21:34:25.187570Z"}
g = (
    inai.assign(mes=lambda df: df.fecha_solicitud.astype(str).apply(lambda s: s[0:7]))
    .groupby(['mes', 'calidad_respuesta', 'sector'])
    .size()
    .to_frame('n')
    .reset_index(drop=False)
)
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:01.911377Z", "start_time": "2019-08-25T21:35:01.900649Z"}
g = g.sort_values(['mes', 'sector', 'calidad_respuesta'])
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:04.341080Z", "start_time": "2019-08-25T21:35:04.333591Z"}
g_todas_fechas = []
for year in range(2012, 2019):
    for month in range(1, 13):
        if month < 10:
            strm = '0'+str(month)
        else:
            strm = str(month)
        g_todas_fechas.append(str(year)+'-'+strm)
for month in range(1, 7):
    if month < 10:
        strm = '0'+str(month)
    else:
        strm = str(month)
    g_todas_fechas.append('2019-'+strm)
        
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:05.742163Z", "start_time": "2019-08-25T21:35:05.738657Z"}
sectores = g.sector.unique()
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:08.526495Z", "start_time": "2019-08-25T21:35:08.491422Z"}
ii = pd.DataFrame(list(product(g_todas_fechas, [-1, 0, 1], sectores)))
ii.columns = ['mes', 'calidad_respuesta', 'sector']
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:11.333873Z", "start_time": "2019-08-25T21:35:11.307945Z"}
g = ii.merge(g, how='left').fillna(0).sort_values(['mes', 'sector', 'calidad_respuesta'])
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:12.686899Z", "start_time": "2019-08-25T21:35:12.666502Z"}
gg = g.groupby(['mes', 'sector']).agg({'n':'sum'}).reset_index()
gg.columns = ['mes', 'sector', 'n']
gg['calidad_respuesta'] = 2
gg.head()
```

```python ExecuteTime={"end_time": "2019-08-25T21:35:17.225157Z", "start_time": "2019-08-25T21:35:17.210574Z"}
gg = pd.concat((g, gg), sort=False).sort_values(['mes', 'sector', 'calidad_respuesta'])
```

```python ExecuteTime={"end_time": "2019-08-25T21:38:12.069023Z", "start_time": "2019-08-25T21:38:12.065760Z"}
plt.rcParams['figure.figsize'] = (15, 5)
sns_ch = sns.cubehelix_palette(n_colors=3, as_cmap=True)
```

```python ExecuteTime={"end_time": "2019-08-25T21:39:29.824401Z", "start_time": "2019-08-25T21:39:18.019434Z"}
for i, s in enumerate(sectores):
    plt.figure(i)
    df = gg[gg.sector==s].drop('sector', axis=1)
    df = df.pivot(index='mes', columns='calidad_respuesta', values='n')
    df.columns = ['falta del solicitante', 'mala', 'buena', 'total']
    df.drop('total', axis=1, inplace=True)
    df.plot.area(colormap=sns_ch, alpha=0.75)
    plt.title(s)
```

```python ExecuteTime={"end_time": "2019-08-25T21:12:43.421449Z", "start_time": "2019-08-25T21:12:10.121030Z"}
sns.relplot(x='mes',  y='n',
            row='sector', hue='calidad_respuesta',
            kind='line',
            aspect=3, 
            facet_kws={'sharey':False},
            data=g)
```

```python

```
