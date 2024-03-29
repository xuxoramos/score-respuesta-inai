import os
import numpy as np
import boto3
import botocore
import requests, zipfile, io
import textract
import re


def Folio13(folio):
    """
    Función para garantizar que el folio sea de 13 dígitos de tipo string,
    cuando encuentra que un folio es menor de 13 dígitos, agrega 0 (ceros) a
    la izquierda

    Args:
        folio: folio que se validará
    Return:
        output: folio de 13 dígitos en formato string
    """

    folio = str(folio)
    size = len(folio)
    dif = 13 - size
    output = dif*'0' + folio
    output = str(output)

    return output



def MimeType(url):
    """Función para:
    1. Descargar los archivos respuesta PDF y TXT desde un URL y guardarlos
    en S3
    2. Obtener el mime type del archivo contenido en el URL
    3. Contar el número de archivos contenidos en el URL. (Existen casos ZIP
    en los que cuenta al interior del ZIP cuantos archivos contiene)

    Args:
        url: URL del que se decargarán los archivos con formato PDF y TXT

    Returns:
        mime: mime type del archivo contenido en el URL
        num_files: número de archivos contenidos en el URL
    """

    # bucket de la S3 donde se descargaran los documentos pdf
    bucket_name = 'inai-summerofdata'
    # folder de la S3 donde se decargaran los documentos pdf
    folder = 'raw/respuestas_adjuntos/'

    try:
        response = requests.get(url, verify=False)
        content_type = response.headers['Content-Disposition']
        aux = content_type.split('.')
        mime = str(aux[1])
        num_files = 1
        val = mime.lower()

        ### PDF y TXT
        if val == 'pdf' or val == 'txt':
            aux1 = content_type.split('=')
            file = str(aux1[1])
            s3 = boto3.client('s3')
            s3.put_object(
                Bucket = bucket_name,
                Key = f'{folder}{file}',
                Body = response.content)

            return mime, num_files

        ### ZIP
        if val == 'zip':
            z = zipfile.ZipFile(io.BytesIO(response.content))
            num_files = len(z.infolist())

            return mime, num_files

        ### Todos los demas
        if val not in ('pdf', 'txt', 'zip'):

            return mime, num_files

    except:
        return None, None



def TextractPDF(folio, ext):
    """
    Función para extraer texto de los documentos PDF
    Args:
        folio: nombre del archivo (en este caso folio) del que se desea
        extraer el texto
        ext: extensión del archivo del que se desea extraer el texto

    Returns:
        texto: texto extraído del documento PDF
    """

    # bucket de la S3 donde se encuentran los documentos pdf
    bucket_download = 'inai-summerofdata'
    # ruta de la S3 donde se encuentran los documentos pdf
    path_download = 'raw/respuestas_adjuntos/'

    try:
        folio = str(folio)
        ext = str(ext)
        val = ext.lower()

        if val == 'pdf':
            documentName = path_download + folio + '.' + ext
            output = folio + '.' + ext

            # descargamos archivo de la S3
            s3 = boto3.resource('s3')
            BUCKET_NAME = bucket_download
            KEY = documentName

            try:
                s3.Bucket(BUCKET_NAME).download_file(KEY, f'{output}')

            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise

            file = f'{output}'
            text = textract.process(file, method='tesseract', language='spa')
            text = str(text)

            text = text.replace('-\n', ' ')
            text = text.replace('\n', ' ')
            text = text.replace('\\n', ' ')
            text = text.replace('\\x0c', '')
            text = text.replace('\\xe2\\x80\\x9c', '')
            text = text.replace('\\xe2\\x80\\x9d', '')
            text = text.replace('\\xc2\\xa3', '')
            text = text.replace("'", '')

            text = text.replace('\\xc3\\xb1', 'n')
            text = text.replace('\\xc3\\xb3', 'o')
            text = text.replace('\\xc3\\xa1', 'a')
            text = text.replace('\\xc3\\xa9', 'e')
            text = text.replace('\\xc3\\xba', 'u')
            text = text.replace('\\xc3\\xad', 'i')

            text = text.replace('\\xc3\\x91', 'N')
            text = text.replace('\\xc3\\x93', 'O')
            text = text.replace('\\xc3\\x81', 'A')
            text = text.replace('\\xc3\\x89', 'E')
            text = text.replace('\\xc3\\x9a', 'U')
            text = text.replace('\\xc3\\x8d', 'I')

            text = text.replace('\\xc3\\xbc', 'u')
            text = text.replace('\\xc3\\x9c', 'U')

            texto = text[1:]

            # eliminamos el archivo descargado
            os.remove(f'{output}')

            return texto

        if val != 'pdf':

            return None
    except:
        return None



def StringLowercase(df):
    """
    Función cambiar todos los strings de un dataframe a lowercase
    (columnas y observaciones)

    Args:
        df: dataframe al que se desea hacer la modificación
    Return:
        df: dataframe modificado
    """

    ### Columnas

    DataFrameColumns = df.columns

    for col in DataFrameColumns:
        df.rename(columns={col:col.lower()}, inplace=True)

    ### Observaciones

    filtro = df.dtypes == np.object
    objects = df.dtypes[filtro]
    StringColumns = list(objects.index)
    # Quitamos las columnas que por su naturaleza no deben modificarse
    StringColumns.remove('archivorespuesta')
    StringColumns.remove('tipo_archivo_respuesta')

    for col in StringColumns:
        df[col] = df[col].str.lower()

    return df



def StringAcentos(df):
    """
    Función para eliminar acentos, dieresis y eñes de los strings de un
    dataframe (columnas y observaciones)

    Args:
        df: dataframe al que se desea hacer la modificación
    Return:
        df: dataframe modificado
    """

    ### Columnas

    df.columns = df.columns.str.replace('á', 'a')
    df.columns = df.columns.str.replace('é', 'e')
    df.columns = df.columns.str.replace('í', 'i')
    df.columns = df.columns.str.replace('ó', 'o')
    df.columns = df.columns.str.replace('ú', 'u')
    df.columns = df.columns.str.replace('ü', 'u')
    df.columns = df.columns.str.replace('ñ', 'n')

    ### Observaciones

    filtro = df.dtypes == np.object
    objects = df.dtypes[filtro]
    StringColumns = list(objects.index)
    # Quitamos las columnas que por su naturaleza no deben modificarse
    StringColumns.remove('archivorespuesta')
    StringColumns.remove('tipo_archivo_respuesta')

    for col in StringColumns:
        df[col] = df[col].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    return df



def StringStrip(df):
    """
    Función para eliminar espacios al inicio y al final de los strings de un
    dataframe (columnas y observaciones)

    Args:
        df: dataframe al que se desea hacer la modificación
    Return:
        df: dataframe modificado
    """

    ### Columnas

    df.columns = [col.strip() for col in df.columns]

    ### Observaciones

    filtro = df.dtypes == np.object
    objects = df.dtypes[filtro]
    StringColumns = list(objects.index)

    for col in StringColumns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    return df



def StringEspacios(df):
    """
    Función para eliminar espacios dobles (o mas) de los strings de un
    dataframe (columnas y observaciones)

    Args:
        df: dataframe al que se desea hacer la modificación
    Return:
        df: dataframe modificado
    """

    ### Columnas

    df.columns = [re.sub(' +', ' ', col) for col in df.columns]

    ### Observaciones

    filtro = df.dtypes == np.object
    objects = df.dtypes[filtro]
    StringColumns = list(objects.index)

    for col in StringColumns:
        df[col] = df[col].apply(lambda x: re.sub(' +', ' ', x) if isinstance(x, str) else x)

    return df



def EliminarNulos(df):
    """
    Función para eliminar nulos de un dataframe:
    1. Columnas. Elimina columnas con valores nulos en todas las observaciones
    2. Observaciones. Elimina observaciones con valores nulos en todas las
    columnas

    Args:
        df: dataframe al que se desea hacer la modificación
    Return:
        df: dataframe modificado
    """

    df = df.replace(r'^\s*$', np.nan, regex=True)

    ### Columnas

    df = df.dropna(how='all', axis=1)

    ### Observaciones

    df = df.dropna(how='all')

    return df
