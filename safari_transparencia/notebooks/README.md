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
