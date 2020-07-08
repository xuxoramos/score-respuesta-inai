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
