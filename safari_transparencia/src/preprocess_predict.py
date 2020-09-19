import boto3
import pandas as pd
import numpy as np
import spacy
import nltk
import re
import pickle
import lime
from nltk import SnowballStemmer
from datetime import date
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from lime import lime_tabular
from lime import explanation

pd.options.display.max_columns = None

# Valor en automatico cuando se realiza una solicitud
today =  date.today()

######### Estos valures los da el usuario  ########## SE TOMARA UN EJEMPLO
texto = 'compra de medicamentos en la ciudad de mexico'

# Para esta variable se sugiere un combo box donde el usuario solo pueda seleccionar de los 65 casos de dependencias
# estandarizadas. Si queda libre, tendria que hacerse un estandarizador
dependencia = 'instituto mexicano del seguro social (imss)'

#####################################################

data = {
    'fechasolicitud': today,
    'descripcionsolicitud': texto,
    'dependencia': dependencia
}

df = pd.DataFrame(data, index=[0])


df['fechasolicitud'] = pd.to_datetime(df['fechasolicitud'])

# agregamos año de la solicitud
df['anosolicitud'] = pd.DatetimeIndex(df['fechasolicitud']).year


# agregamos mes de la solicitud
df['messolicitud'] = pd.DatetimeIndex(df['fechasolicitud']).month


# agregamos semana de la solicitud
df['semanasolicitud'] = df['fechasolicitud'].dt.week


# agregamos dia de la semana de la solicitud
df['diasolicitud'] = df['fechasolicitud'].dt.dayofweek


# estandarizamos todo a lower case
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

    for col in StringColumns:
        df[col] = df[col].str.lower()

    return df

df = StringLowercase(df)


# quitamos acentos
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

    for col in StringColumns:
        df[col] = df[col].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    return df


df = StringAcentos(df)


# quitamos espacios al inicio y al final del texto
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

df = StringStrip(df)


# quitamos espacios dobles
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

df = StringEspacios(df)


# lematizamos texto
nlp = spacy.load('es_core_news_sm')

def LematizarTexto(texto):

    doc = nlp(texto)
    words = [t.lemma_ for t in doc if not t.is_punct | t.is_stop]
    lexical_tokens = [t.lower() for t in words if len(t) > 3 and t.isalpha()]
    lemmatized_text = ' '.join(lexical_tokens)

    return lemmatized_text


df['descripcionsolicitud_lemma'] = df['descripcionsolicitud'].map(LematizarTexto)


# quitamos cloud de palabras revisadas con socialTIC
session = boto3.session.Session()
s3client = session.client('s3')
response = s3client.get_object(Bucket='inai-summerofdata', Key='raw/stopwords.pkl')
body = response['Body'].read()
banned = pickle.loads(body)

f = lambda x: ' '.join([item for item in x.split() if item not in banned])

df['descripcionsolicitud_lemma'] = df['descripcionsolicitud_lemma'].apply(f)


# agregamos longitud del texto de la solicitud lematizada
df['solicitud_lemma_longitud'] = df['descripcionsolicitud_lemma'].str.len()


# quitamos la columna fecha solicitud
df = df.drop('fechasolicitud', axis=1)


# acomodamos las columnas
columns = ['anosolicitud', 'messolicitud', 'semanasolicitud',
        'diasolicitud', 'descripcionsolicitud_lemma', 'solicitud_lemma_longitud',
        'dependencia']

df = df[columns]


# Generamos dependencia con dummies

dep = ['dependencia_clean_administracion portuaria integral',
 'dependencia_clean_administracion publica federal',
 'dependencia_clean_aeropuertos y servicios auxiliares (asa)',
 'dependencia_clean_archivo general de la nación',
 'dependencia_clean_auditoría superior de la federación',
 'dependencia_clean_banca de desarrollo',
 'dependencia_clean_camara de dipuados',
 'dependencia_clean_capufe',
 'dependencia_clean_cfe',
 'dependencia_clean_cnbv',
 'dependencia_clean_cofepris',
 'dependencia_clean_conacyt',
 'dependencia_clean_empresas de participacion estatal',
 'dependencia_clean_hospitales',
 'dependencia_clean_inah',
 'dependencia_clean_inai',
 'dependencia_clean_ine',
 'dependencia_clean_instituciones de educacion superior autonomas',
 'dependencia_clean_instituto del fondo nacional de la vivienda para los trabajadores',
 'dependencia_clean_instituto federal de telecomunicaciones (ift)',
 'dependencia_clean_instituto mexicano de la propiedad industrial',
 'dependencia_clean_instituto mexicano del seguro social (imss)',
 'dependencia_clean_instituto nacional de migración',
 'dependencia_clean_ipn',
 'dependencia_clean_lotenal',
 'dependencia_clean_organismo autonomo',
 'dependencia_clean_organismo descentralizado',
 'dependencia_clean_partidos politicos',
 'dependencia_clean_pemex',
 'dependencia_clean_pgr',
 'dependencia_clean_poder judicial de la federacion',
 'dependencia_clean_policia federal',
 'dependencia_clean_presidencia de la republica',
 'dependencia_clean_procuraduría federal del consumidor',
 'dependencia_clean_profeco',
 'dependencia_clean_registro agrario nacional',
 'dependencia_clean_sader',
 'dependencia_clean_sae',
 'dependencia_clean_sagarpa',
 'dependencia_clean_sat',
 'dependencia_clean_scjn',
 'dependencia_clean_sct',
 'dependencia_clean_se',
 'dependencia_clean_secretaria de bienestar',
 'dependencia_clean_secretariado ejecutivo del sistema nacional de seguridad pública',
 'dependencia_clean_secretaría de cultura',
 'dependencia_clean_sectur',
 'dependencia_clean_sedatu',
 'dependencia_clean_sedena',
 'dependencia_clean_sedesol',
 'dependencia_clean_segob',
 'dependencia_clean_semar',
 'dependencia_clean_semarnat',
 'dependencia_clean_senado de la república',
 'dependencia_clean_sener',
 'dependencia_clean_sep',
 'dependencia_clean_sfp',
 'dependencia_clean_shcp',
 'dependencia_clean_sindicatos',
 'dependencia_clean_sre',
 'dependencia_clean_ssa',
 'dependencia_clean_sspc',
 'dependencia_clean_stps',
 'dependencia_clean_tribunales administrativos',
 'dependencia_clean_unam']

for d in dep:
    aux0 = d.split('_')
    aux1 = df['dependencia'][0]
    if aux1 == aux0[2]:
        df[d] = 1
    else:
        df[d] = 0


df = df.drop('dependencia', axis=1)


features = np.array(df)

# Ejecución de una predicción

session = boto3.session.Session()
s3client = session.client('s3')
response = s3client.get_object(Bucket='inai-summerofdata', Key='modeling/GBC/1_temporalidad/1_iteracion/grid_search.pkl')
body = response['Body'].read()
grid_search = pickle.loads(body)

best_gbc = grid_search.best_estimator_

gbc_pred = best_gbc.predict(features)

print(gbc_pred)

score = best_gbc.predict_proba(features)

print(score)


# Interpretabilidad
######### Obtenemos vocaulario de tfidf

def get_column_names_from_ColumnTransformer(column_transformer):
    col_name = []
    for transformer_in_columns in column_transformer.transformers_[:-1]:#the last transformer is ColumnTransformer's 'remainder'
        raw_col_name = transformer_in_columns[2]
        if isinstance(transformer_in_columns[1],Pipeline):
            transformer = transformer_in_columns[1].steps[-1][1]
        else:
            transformer = transformer_in_columns[1]
        try:
            names = transformer.get_feature_names()
        except AttributeError: # if no 'get_feature_names' function, use raw column name
            names = raw_col_name
        if isinstance(names,np.ndarray): # eg.
            col_name += names.tolist()
        elif isinstance(names,list):
            col_name += names
        elif isinstance(names,str):
            col_name.append(names)
    return col_name

tfidf_names = get_column_names_from_ColumnTransformer(best_gbc['preprocess'])

class_names = np.array([False, True])
df_names = list(df.columns)


features_names = []
features_names = tfidf_names
for i in df_names:
    if i != 'descripcionsolicitud_lemma':
        features_names.append(i)

session = boto3.session.Session()
s3client = session.client('s3')
response = s3client.get_object(Bucket='inai-summerofdata', Key='modeling/GBC/1_temporalidad/1_iteracion/features.pkl')
body = response['Body'].read()
X_train = pickle.loads(body)

explainer_model = lime_tabular.LimeTabularExplainer(
    training_data=best_gbc['preprocess'].transform(X_train), #el set de entrenamiento con el que se entreno
    mode="classification",
    feature_names=features_names, #nombre de las variables, en el orden que se envian
    class_names=class_names, #el nombre de las etiquetas de clasificación
    kernel_width=1) #el tamaño de la ventana para generar datos (mientras más pequeño más cercano a los valores reales)


sp = explainer_model.explain_instance(best_gbc['preprocess'].transform(features), best_gbc['clf'].predict_proba, num_features=5, distance_metric='cosine')

bucket='inai-summerofdata'
key='interpretability/outputs/lime_model.pkl'
pickle_byte_obj = pickle.dumps(sp)
s3_resource = boto3.resource('s3')
s3_resource.Object(bucket, key).put(Body=pickle_byte_obj)
