# Estructura de la carpeta notebooks

### step1
**notebook: step1_crear_parquet_guardarS3.ipynb**

+ Consolidar información raw de los años 2012 a 2019. (Archivos xls)
+ Descargar los archivos adjuntos como respuesta con formato pdf y txt a la S3.
+ Agregar 2 columnas:
  - **tipo_archivo_respuesta.** Contiene el mime type del archivo descargado del URL de la columna ARCHIVORESPUESTA.
  - **cantidad_archivos_respuesta.** Contiene el número de archivos contenidos en el URL. (Existen casos ZIP en los que cuenta al interior del ZIP cuantos archivos contiene)
+ Generar output en formato parquet y guardarlo en la S3. (inai.parquet)

Nota: Decidimos crear estas dos columnas en esta etapa ya que pasar por los URLs era demasiado tardado, aprovechamos la descarga para obtener la información de las columnas mencionadas arriba.

**notebook: step1_crear_parquet_guardarS3_parallelization.ipynb**

Ejecuta las mismas tareas que el notebook step1_crear_parquet_guardarS3.ipynb solo que paraleliza las tareas para mejorar los tiempos de procesamiento.

### step2
**notebook: step2_textract_pdf.ipynb**

+ Extraer texto de los archivos pdf descargados previamente en el step1.
+ Agregar columna:
  - **texto_respuesta_adjunto.** Contiene el texto extraído de los documentos PDF.
+ Actualizar archivo inai.parquet


### step3
**notebook: step3_clean.ipynb**

+ Limpeza de información del archivo inai.parquet
+ Tareas desempeñadas:
  - Estandarización de nulos.
  - Validación del tipo de las columnas.
  - Modificación de strings a lowercase.
  - Eliminamos acentos, dieresis y eñes de strings.
  - Eliminamos espacios al inicio y al final de strings.
  - Eliminamos espacios dobles (o mas) de strings.
  - Eliminamos columnas con observaciones con puros valores nulos.
  - Eliminamos observaciones con valores nulos en todas las columnas.
  - Eliminamos observaciones repetidas.
+ Generar output en formato parquet (inai.parquet) y guarlarlo en la S3 en la carpeta clean.


### step4
**notebook: step4_fe.ipynb**

+ Transformación de columna descripcionsolicitud. Se eliminaron "stopwords" del diccionario compartido por SocialTIC.
+ Se agregó columna respuestareal. Esta columna considera las reglas de negocio definidas por el equipo. (issue 25)
+ Generar output en formato parquet (inai.parquet) y guardarlo en la S3 en la carpeta mlpreproc.

**notebook: step4_fe_2.ipynb**

+ Se filtró solo por los tipos de solicitud "informacion publica"
+ Agregar columnas:
  - **calidad_respuesta**
  - **calidad_respuesta_real**

La calidad de las respuestas se agrupan en las categorias:
1. satisfactoria
2. no respondida
3. en proceso

+ Se actualiza el archivo inai.parquet de la carpeta mlpreproc en la S3.

**notebook: step4_fe_3.ipynb**

+ Eliminamos casos con un número menor a 16 caracteres de la columna descripcionsolicitud
+ Eliminamos casos en los que calidad_respuesta_real = 'en proceso'

**notebook: step4_fe_3_sample_year_dependencia.ipynb**


### step5
**notebook: step5_model_LDA_0.ipynb**

**notebook: step5_model_LDA_1.ipynb**

**notebook: step5_model_LDA_2.ipynb**

**notebook: step5_model_LDA_3.ipynb**

**notebook: step5_model_LDA_4.ipynb**

**notebook: step5_model_LDA_resultados.ipynb**

**notebook: step5_model_GBC_0.ipynb**

**notebook: step5_model_Random_Forest_0.ipynb**

**notebook: step5_model_SVM_0.ipynb**
