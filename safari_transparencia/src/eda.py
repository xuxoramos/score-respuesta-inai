import os
import boto3
import botocore
import numpy as np



def UneCategoriaRespuestaString(df):
    """
    Esta función une los tipos de respuesta en tres categorías: En proceso, Satisfactoria y No respondida o denegada.
    categorías de Satisfactoria:["Entrega de información en medio electrónico","Notificación de disponibilidad de información",
                                "Notificación lugar y fecha de entrega", "Notificación de envío", 
                                "Respuesta del solicitante a la notificación de entrega de información con  costo",
                                "Respuesta del solicitante a la notificación de entrega de información sin costo",
                                "Notificación de pago","Notificación de cambio de tipo de solicitud"]
    categorías de No respondida o denegada:["No es de competencia de la unidad de enlace","Inexistencia de la información solicitada",
                                            "La información está disponible públicamente", "Sin respuesta","Negativa por ser reservada o confidencial",
                                            "Información parcialmente reservada o confidencial", "La solicitud no corresponde al marco de la Ley",
                                            "No se dará trámite a la solicitud"]
    categorías de En proceso:["Requerimiento de información adicional","Notificación de prórroga","Respuesta a solicitud de información adicional"]
    ==========
    * Args:
      - df: el data frame que contiene los parquets importados.
    * Return:
      - Data Frame: entrega el data frame con los la categoría de la columna RESPUESTA modificada.
    ==========
    Ejemplo:
      >>df = UneCategoriaRespuestaString(df)
    """
    #df["RESPUESTA"] = df["RESPUESTA"].str.lower()
    # Las variables 
    df.loc[df["RESPUESTA"] == "Entrega de información en medio electrónico", "RESPUESTA"] = 'Satisfactoria'
    df.loc[df["RESPUESTA"] == "Notificación de disponibilidad de información", "RESPUESTA"] = 'Satisfactoria'
    df.loc[df["RESPUESTA"] == "Notificación lugar y fecha de entrega", "RESPUESTA"] = 'Satisfactoria'
    df.loc[df["RESPUESTA"] == "Notificación de envío", "RESPUESTA"] = 'Satisfactoria'
    df.loc[df["RESPUESTA"] == "Respuesta del solicitante a la notificación de entrega de información con  costo", "RESPUESTA"] = 'Satisfactoria'
    df.loc[df["RESPUESTA"] == "Respuesta del solicitante a la notificación de entrega de información sin costo", "RESPUESTA"] = 'Satisfactoria'
    df.loc[df["RESPUESTA"] == "Notificación de pago", "RESPUESTA"] = 'Satisfactoria'
    df.loc[df["RESPUESTA"] == "Notificación de cambio de tipo de solicitud", "RESPUESTA"] = 'Satisfactoria'
    
    df.loc[df["RESPUESTA"] == "No es de competencia de la unidad de enlace", "RESPUESTA"] = 'No respondida'
    df.loc[df["RESPUESTA"] == "Inexistencia de la información solicitada", "RESPUESTA"] = 'No respondida'
    df.loc[df["RESPUESTA"] == "La información está disponible públicamente", "RESPUESTA"] = 'No respondida'
    df.loc[df["RESPUESTA"] == "Sin respuesta", "RESPUESTA"] = 'No respondida'
    df.loc[df["RESPUESTA"] == "Negativa por ser reservada o confidencial", "RESPUESTA"] = 'No respondida'
    df.loc[df["RESPUESTA"] == "Información parcialmente reservada o confidencial", "RESPUESTA"] = 'No respondida'
    df.loc[df["RESPUESTA"] == "La solicitud no corresponde al marco de la Ley ", "RESPUESTA"] = 'No respondida'
    df.loc[df["RESPUESTA"] == "No se dará trámite a la solicitud", "RESPUESTA"] = 'No respondida'
    
    df.loc[df["RESPUESTA"] == "Requerimiento de información adicional", "RESPUESTA"] = 'En proceso'
    df.loc[df["RESPUESTA"] == "Notificación de prórroga", "RESPUESTA"] = 'En proceso'
    df.loc[df["RESPUESTA"] == "Respuesta a solicitud de información adicional", "RESPUESTA"] = 'En proceso'
    
    return df  



def UneCategoriaRespuestaNumerical(df):
    """
    Esta función une los tipos de respuesta en tres categorías: En proceso (0) , Satisfactoria (1) y No respondida o denegada (-1).
    categorías de Satisfactoria:["Entrega de información en medio electrónico","Notificación de disponibilidad de información",
                                "Notificación lugar y fecha de entrega", "Notificación de envío", 
                                "Respuesta del solicitante a la notificación de entrega de información con  costo",
                                "Respuesta del solicitante a la notificación de entrega de información sin costo",
                                "Notificación de pago","Notificación de cambio de tipo de solicitud"]
    categorías de No respondida o denegada:["No es de competencia de la unidad de enlace","Inexistencia de la información solicitada",
                                            "La información está disponible públicamente", "Sin respuesta","Negativa por ser reservada o confidencial",
                                            "Información parcialmente reservada o confidencial", "La solicitud no corresponde al marco de la Ley",
                                            "No se dará trámite a la solicitud"]
    categorías de En proceso:["Requerimiento de información adicional","Notificación de prórroga","Respuesta a solicitud de información adicional"]
    ==========
    * Args:
      - df: el data frame que contiene los parquets importados.
    * Return:
      - Data Frame: entrega el data frame con los la categoría de la columna RESPUESTA modificada.
    ==========
    Ejemplo:
      >>df = UneCategoriaRespuestaNumerical(df)
    """
    #df["RESPUESTA"] = df["RESPUESTA"].str.lower()
    df.loc[df["RESPUESTA"] == "Entrega de información en medio electrónico", "RESPUESTA"] = 1
    df.loc[df["RESPUESTA"] == "Notificación de disponibilidad de información", "RESPUESTA"] = 1
    df.loc[df["RESPUESTA"] == "Notificación lugar y fecha de entrega", "RESPUESTA"] = 1
    df.loc[df["RESPUESTA"] == "Notificación de envío", "RESPUESTA"] = 1
    df.loc[df["RESPUESTA"] == "Respuesta del solicitante a la notificación de entrega de información con  costo", "RESPUESTA"] = 1
    df.loc[df["RESPUESTA"] == "Respuesta del solicitante a la notificación de entrega de información sin costo", "RESPUESTA"] = 1
    df.loc[df["RESPUESTA"] == "Notificación de pago", "RESPUESTA"] = 1
    df.loc[df["RESPUESTA"] == "Notificación de cambio de tipo de solicitud", "RESPUESTA"] = 1
    
    df.loc[df["RESPUESTA"] == "No es de competencia de la unidad de enlace", "RESPUESTA"] = -1
    df.loc[df["RESPUESTA"] == "Inexistencia de la información solicitada", "RESPUESTA"] = -1
    df.loc[df["RESPUESTA"] == "La información está disponible públicamente", "RESPUESTA"] = -1
    df.loc[df["RESPUESTA"] == "Sin respuesta", "RESPUESTA"] = -1
    df.loc[df["RESPUESTA"] == "Negativa por ser reservada o confidencial", "RESPUESTA"] = -1
    df.loc[df["RESPUESTA"] == "Información parcialmente reservada o confidencial", "RESPUESTA"] = -1
    df.loc[df["RESPUESTA"] == "La solicitud no corresponde al marco de la Ley ", "RESPUESTA"] = -1
    df.loc[df["RESPUESTA"] == "No se dará trámite a la solicitud", "RESPUESTA"] = -1
    
    df.loc[df["RESPUESTA"] == "Requerimiento de información adicional", "RESPUESTA"] = 0
    df.loc[df["RESPUESTA"] == "Notificación de prórroga", "RESPUESTA"] = 0
    df.loc[df["RESPUESTA"] == "Respuesta a solicitud de información adicional", "RESPUESTA"] = 0
    
    return df  



def CreaTablaConteoPorcentaje(df, nomColumna, booleanNA):
    """
    Esta función crea la tabla con información sobre los conteos y el porcentaje al que corresponden del total de los datos.
    
    ==========
    * Args:
      - df: el data frame que contiene los parquets importados.
      - nomColumna: El nombre de la columna sobre la que se quiere realizar la tabla.
      - booleanNA: Indicador booleano que indica si se requiere que se muestren los NA's en la tabla.
    * Return:
      - Data Frame: entrega el data frame con los la categoría de la columna RESPUESTA modificada.
    ==========
    Ejemplo:
      >>df = CreaTablaConteoPorcentaje(df, 'RESPUESTA', True)
    
    """
    
    df_resultado = df[nomColumna].value_counts(dropna=booleanNA)
    df_resultado = pd.DataFrame(data=df_resultado)
    
    #obteniendo los porcentajes
    df_resultado['porcentaje'] = df[nomColumna].value_counts(dropna=booleanNA, normalize=True).mul(100).round(2).astype(str)+'%'
    
    return df_resultado



def UnificaTipodeArchivo(df):
    """
    Esta función unifica todos los tipos de archivo a minúsculas, para poder hacer correctamente el 
    análisis exploratorio con respecto al tipo de datos.
    ==========
    * Args:
      - df: el data frame que contiene los parquets importados.
    * Return:
      - Data Frame: entrega el data frame con los tipos de archivo unificados.
    ==========
    Ejemplo:
      >>df = unificaTipodeArchivo(df)
    """
    df["tipo_archivo_respuesta"] = df["tipo_archivo_respuesta"].str.lower()
    #df.loc[df["tipo_archivo_respuesta"] == "docx", "tipo_archivo_respuesta"] = 'doc'
    
    return df



def CreaFiltroArchivosIss20(df):
    """
    Esta función extrae un dataset auxiliar que contiene los casos donde no se encontraron archivos o donde el tipo de archivo encontrado es un zip/ZIP que se encuentra vacío.
    ==========
    * Args:
      - df: el data frame que contiene los parquets importados.
    * Return:
      - Data Frame: entrega el data frame auxiliar.
    ==========
    Ejemplo:
      >>df = CreaFiltroArchivosIss20(df)
    """
    df_filtrado1 = df[df['tipo_archivo_respuesta'].isna()]
    df_filtrado2 = df[df['tipo_archivo_respuesta']=='zip']
    df_filtrado3 = df[df['tipo_archivo_respuesta']=='ZIP']
    df_filtrado4 = df_filtrado2.append(df_filtrado3)
    df_filtrado5 = df[df['cantidad_archivos_respuesta']==0]
    df_filtrado = df_filtrado1.append(df_filtrado5)
    
    return df



def ConvierteTipoDatosFechas(df):
    """
    Esta función convierte las columnas que son de tipo fecha a Date y añade una columna con el año de solicitud.
    
    ==========
    * Args:
      - df: el data frame que contiene los parquets importados.
    * Return:
      - Data Frame: entrega el data frame con las fechas en tipo Date.
    ==========
    Ejemplo:
      >>df = ConvierteTipoDatosFechas(df)
    """
    
    for col in ['FECHASOLICITUD', 'FECHARESPUESTA']:#, 'FECHALIMITE']:
        df[col] = pd.to_datetime(df[col],format= "%Y-%m-%d %H:%M:%S")
    
    df['año_solicitud'] = pd.DatetimeIndex(df['FECHASOLICITUD']).year
    
    return df



def CreaCategoryURL(df):
    """
    Esta función convierte crea una columna que se llamará category_url, donde todos los renglones que contengan un url en la variable 'ARCHIVORESPUESTA' tendrán la palabra url, de lo contrario mantendrán el valor original.
    
    ==========
    * Args:
      - df: el data frame que contiene los parquets importados.
    * Return:
      - df: entrega el data frame con la columna adicional category_url.
    ==========
    Ejemplo:
      >>df = CreaCategoryURL(df)
    """    
    
    # Se extraen los valores que no sean null
    my_df = df[~df['ARCHIVORESPUESTA'].isnull()]
    
    # Se copia la columna 'ARCHIVORESPUESTA' para crear 'category_url'
    my_df['category_url'] = my_df['ARCHIVORESPUESTA']
    
    # Si 'category_url' contien un url, se le asigna la palabra 'url'
    my_df.loc[my_df["category_url"].str.contains('https', case=False, na=None), "category_url"] = 'url'
    
    # Se crean los data frames para hacer el merge con el data frame original
    data = [my_df["FOLIO"], my_df["category_url"]]
    headers = ["FOLIO", "category_url"]
    df3 = pd.concat(data, axis=1, keys=headers)
    #df3.head()
    
    # Se hace el merge con el data frame original
    df_nuevo = pd.merge(df, df3, how='left', on=['FOLIO', 'FOLIO'])
    
    return df_nuevo






