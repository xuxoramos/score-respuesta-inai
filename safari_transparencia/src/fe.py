def RespuestaReal(respuesta, tipo_archivo, cantidad_archivos, rechazo):
    """
    Función para crear la columna respuestareal que considera las reglas
    de negocio definidas.

    Args:
        respuesta: columna de respuesta
        tipo_archivo: columna que tiene la extensión del archivorespuesta
        cantidad_archivos: columna con el número de archivos que contenía
        el URL del archivorespuesta
        rechazo: etiqueta que define si el texto que se extrajo contiene las
        frases de rechazo compartidas por SocialTIC.
    Return:
        si se cumple alguna de las condiciones (reglas de negocio) regresa
        la etiqueta 'sin respuesta', en el caso contrario no modifica la respuesta
        dada inicialmente.
    """

    tipo_archivo = tipo_archivo.lower()

    if (respuesta == 'entrega de informacion en medio electronico' or
        respuesta == 'la informacion esta disponible publicamente') and (
        (tipo_archivo == None) or
        (tipo_archivo == 'zip' and cantidad_archivos < 5) or
        (tipo_archivo == 'pdf' and  rechazo == True)
    ):
        return 'sin respuesta'
    else:
        return respuesta



def CalidadRespuesta(df, columna_respuesta, nueva_columna):
    """
    Función para crear la columna calidad_respuesta que agrupa en:
        1. satisfactoria
        2. no respondida
        3. en proceso

    Args:
        df: dataframe en el que se creara la columna nueva
        columna_respuesta: nombre de la columna respuesta
        nueva_columna: nombre de la nueva columna que se creara que contendra la
        calidad de la respuesta
    Return:
        df: dataframe con la nueva columna de calidad de respusta
    """

    df.loc[df[columna_respuesta] == 'entrega de informacion en medio electronico', nueva_columna] = 'satisfactoria'
    df.loc[df[columna_respuesta] == 'notificacion de disponibilidad de informacion', nueva_columna] = 'satisfactoria'
    df.loc[df[columna_respuesta] == 'notificacion lugar y fecha de entrega', nueva_columna] = 'satisfactoria'
    df.loc[df[columna_respuesta] == 'notificacion de envio', nueva_columna] = 'satisfactoria'
    df.loc[df[columna_respuesta] == 'respuesta del solicitante a la notificacion de entrega de informacion con costo', nueva_columna] = 'satisfactoria'
    df.loc[df[columna_respuesta] == 'respuesta del solicitante a la notificacion de entrega de informacion sin costo', nueva_columna] = 'satisfactoria'
    df.loc[df[columna_respuesta] == 'notificacion de pago', nueva_columna] = 'satisfactoria'
    df.loc[df[columna_respuesta] == 'la informacion esta disponible publicamente', nueva_columna] = 'satisfactoria'


    df.loc[df[columna_respuesta] == 'no es de competencia de la unidad de enlace', nueva_columna] = 'no respondida'
    df.loc[df[columna_respuesta] == 'inexistencia de la informacion solicitada', nueva_columna] = 'no respondida'
    df.loc[df[columna_respuesta] == 'sin respuesta', nueva_columna] = 'no respondida'
    df.loc[df[columna_respuesta] == 'negativa por ser reservada o confidencial', nueva_columna] = 'no respondida'
    df.loc[df[columna_respuesta] == 'informacion parcialmente reservada o confidencial', nueva_columna] = 'no respondida'
    df.loc[df[columna_respuesta] == 'la solicitud no corresponde al marco de la ley', nueva_columna] = 'no respondida'
    df.loc[df[columna_respuesta] == 'no se dara tramite a la solicitud', nueva_columna] = 'no respondida'


    df.loc[df[columna_respuesta] == 'requerimiento de informacion adicional', nueva_columna] = 'en proceso'
    df.loc[df[columna_respuesta] == 'notificacion de prorroga', nueva_columna] = 'en proceso'
    df.loc[df[columna_respuesta] == 'respuesta a solicitud de informacion adicional', nueva_columna] = 'en proceso'
    df.loc[df[columna_respuesta] == 'notificacion de cambio de tipo de solicitud', nueva_columna] = 'en proceso'

    return df
