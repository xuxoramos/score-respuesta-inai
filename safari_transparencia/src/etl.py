import boto3
import requests, zipfile, io


def Folio13(folio):
    """
    Función para garantizar que el folio sea de 13 dígitos de tipo string,
    cuando encuentra que un folio en menor de 13 digitos, agrega 0 (ceros) a
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


    bucket_name = 'inai-summerofdata'
    folder = 'raw/respuestas_adjuntos'

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
                Key = f'{folder}/{file}',
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
