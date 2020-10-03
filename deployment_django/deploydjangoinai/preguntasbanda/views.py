from django.shortcuts import render
from . import forms


import boto3
import pandas as pd
import numpy as np
import spacy
import nltk
import re
import pickle
from nltk import SnowballStemmer
from datetime import date
import lime
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from lime import lime_tabular
from lime import explanation

import os
import string
import json
from sklearn.utils import check_random_state

from . import fixdependencia

nlp = spacy.load('es_core_news_sm')


# bucket = 'inai-summerofdata'
# folder = 'parquet'
# f = f's3://{bucket}/{folder}/inai_dependencia.parquet'
# dframe = pd.read_parquet(f, engine='pyarrow')
# print("el head del dframe: ")
# print(dframe.head())
print("Inicializando las variables")
resultado_prediccion = ""
score = " "
sp=" "
print("resultado:"+resultado_prediccion+".")
print("score:"+score+".")
print("sp:"+sp+".")

print("cargando el mejor modelo")
session = boto3.session.Session()
#print(session)
s3client = session.client('s3')
#print(s3client)
response = s3client.get_object(Bucket='inai-summerofdata', Key='modeling/GBC/1_temporalidad/1_iteracion/grid_search.pkl')
#print(response)
#print(response['Body'])
body = response['Body'].read()
#print(body)
grid_search = pickle.loads(body)


best_gbc = grid_search.best_estimator_
#print(best_gbc)

print("Cargando el modelo de interpretabilidad")
session = boto3.session.Session()
s3client = session.client('s3')
response = s3client.get_object(Bucket='inai-summerofdata', Key='modeling/GBC/1_temporalidad/1_iteracion/features.pkl')
body = response['Body'].read()
X_train = pickle.loads(body)

#mover a partir de aqui
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


        # mover hasta aqui al inicio
print("Modelos y variables cargados correctamente")


# Create your views here.
def index(request):
    resultado_prediccion = ""
    score=""
    sp=""
    figure_lime=""
    lista_lime = ""
    hay_respuesta=False
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)
        hay_respuesta=True

    if form.is_valid():
        print("VALIDATION SUCCESS!")
        nombre = form.cleaned_data['nombre']
        email = form.cleaned_data['email']
        texto_de_la_solicitud = form.cleaned_data['texto_de_la_solicitud']
        depend = form.cleaned_data['dependencia']
        dependencia = limpiando_dependencia(depend)
        print("NAME: "+form.cleaned_data['nombre'])
        print("EMAIL: "+form.cleaned_data['email'])
        print("Texto: "+form.cleaned_data['texto_de_la_solicitud'])
        print("dependencia: "+form.cleaned_data['dependencia'])
        print("dependencia_SUBMITTED: "+dependencia)
        today =  date.today()
        texto_de_la_solicitud = texto_de_la_solicitud
        dependencia = dependencia

        data = {
            'fechasolicitud': today,
            'descripcionsolicitud': texto_de_la_solicitud,
            'dependencia': dependencia
        }

        df = pd.DataFrame(data, index=[0])

        df['fechasolicitud'] = pd.to_datetime(df['fechasolicitud'])

        df['anosolicitud'] = pd.DatetimeIndex(df['fechasolicitud']).year

        df['messolicitud'] = pd.DatetimeIndex(df['fechasolicitud']).month

        df['semanasolicitud'] = df['fechasolicitud'].dt.week

        df['diasolicitud'] = df['fechasolicitud'].dt.dayofweek

        df = StringLowercase(df)

        df = StringAcentos(df)

        df = StringStrip(df)

        df = StringEspacios(df)

        #nlp = spacy.load('es_core_news_sm')

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

        # generamos dependencia con dummies

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

        #print(df.head())
        #print(len(df))
        #print(features)

        #Ejecución de una predicción

        # session = boto3.session.Session()
        # print(session)
        # s3client = session.client('s3')
        # print(s3client)
        # response = s3client.get_object(Bucket='inai-summerofdata', Key='modeling/GBC/1_temporalidad/1_iteracion/best_gbc.pkl')
        # print(response)
        # print(response['Body'])
        # body = response['Body'].read()
        # print(body)
        # best_gbc = pickle.loads(body)
        #best_gbc = pickle.loads('https://inai-summerofdata.s3-us-west-2.amazonaws.com/modeling/GBC/1_temporalidad/1_iteracion/best_gbc.pkl')


        gbc_pred = best_gbc.predict(features)

        print(gbc_pred)

        score = best_gbc.predict_proba(features)
        print(score)
        print(score[0])
        score_solo = score[0]
        score_postivo = score_solo[0]
        print("score_positivo:")
        print(score_postivo)
        print('iniciando preprocesamiento para lime...')

        tfidf_names = get_column_names_from_ColumnTransformer(best_gbc['preprocess'])

        class_names = np.array([False, True])


        print('entrando al for')
        features_names = []
        features_names = tfidf_names

        df_names = list(df.columns)
        for i in df_names:
            if i != 'descripcionsolicitud_lemma':
                features_names.append(i)
        print('ya salio del for, empezando explicación del modelo')
        explainer_model = lime_tabular.LimeTabularExplainer(
                                                training_data=best_gbc['preprocess'].transform(X_train), #el set de entrenamiento con el que se entreno
                                                mode="classification",
                                                feature_names=features_names, #nombre de las variables, en el orden que se envian
                                                class_names=class_names, #el nombre de las etiquetas de clasificación
                                                kernel_width=1) #el tamaño de la ventana para generar datos (mientras más pequeño más cercano a los valores reales)


        print('terminó de cargar el modelo')
        # aqui es donde hace la explicación del modelo
        sp = explainer_model.explain_instance(best_gbc['preprocess'].transform(features), best_gbc['clf'].predict_proba, num_features=5, distance_metric='cosine')
        print(sp)
        #sp.save_to_file("templates/lime_model.html")
        #figure_lime = sp.as_pyplot_figure()
        print("el path de django views es:",os.getcwd())
        lista_lime = sp.as_list()
        print(lista_lime)
        save_to_file_mio(sp,sp,'templates/lime_model.html', show_predicted_value=True)
        #sp.show_in_notebook(show_table=True, show_all=True)
        #sp.as_pyplot_figure();

        if gbc_pred == 0:
            resultado_prediccion = "No satisfactorio"
        else:
            resultado_prediccion = "Satisfactorio"

        print(resultado_prediccion)
        print('empieza a cargar pagina')
    return render(request,'index.html', {'form':form, 'hay_respuesta':hay_respuesta, 'resultado_prediccion':resultado_prediccion, 'score':score, 'sp':sp, 'figure_lime':figure_lime, 'lista_lime':lista_lime})
    #return render(request, 'index.html')


def preguntasbanda(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)

    if form.is_valid():
        print("VALIDATION SUCCESS!")
        nombre = form.cleaned_data['nombre']
        email = form.cleaned_data['email']
        texto_de_la_solicitud = form.cleaned_data['texto_de_la_solicitud']
        depend = form.cleaned_data['dependencia']
        dependencia = limpiando_dependencia(depend)
        print("NAME: "+form.cleaned_data['nombre'])
        print("EMAIL: "+form.cleaned_data['email'])
        print("Texto: "+form.cleaned_data['texto_de_la_solicitud'])
        print("dependencia: "+form.cleaned_data['dependencia'])
        print("dependencia_SUBMITTED: "+dependencia)
        today =  date.today()
        texto_de_la_solicitud = texto_de_la_solicitud
        dependencia = dependencia

        data = {
            'fechasolicitud': today,
            'descripcionsolicitud': texto_de_la_solicitud,
            'dependencia': dependencia
        }

        df = pd.DataFrame(data, index=[0])

        df['fechasolicitud'] = pd.to_datetime(df['fechasolicitud'])

        df['anosolicitud'] = pd.DatetimeIndex(df['fechasolicitud']).year

        df['messolicitud'] = pd.DatetimeIndex(df['fechasolicitud']).month

        df['semanasolicitud'] = df['fechasolicitud'].dt.week

        df['diasolicitud'] = df['fechasolicitud'].dt.dayofweek

        df = StringLowercase(df)

        df = StringAcentos(df)

        df = StringStrip(df)

        df = StringEspacios(df)

        #nlp = spacy.load('es_core_news_sm')

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

        # generamos dependencia con dummies

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

        #print(df.head())
        #print(len(df))
        #print(features)

        #Ejecución de una predicción

        # session = boto3.session.Session()
        # print(session)
        # s3client = session.client('s3')
        # print(s3client)
        # response = s3client.get_object(Bucket='inai-summerofdata', Key='modeling/GBC/1_temporalidad/1_iteracion/best_gbc.pkl')
        # print(response)
        # print(response['Body'])
        # body = response['Body'].read()
        # print(body)
        # best_gbc = pickle.loads(body)
        #best_gbc = pickle.loads('https://inai-summerofdata.s3-us-west-2.amazonaws.com/modeling/GBC/1_temporalidad/1_iteracion/best_gbc.pkl')


        gbc_pred = best_gbc.predict(features)

        print(gbc_pred)

        if gbc_pred == 0:
            resultado_prediccion = "No satisfactorio"
        else:
            resultado_prediccion = "Satisfactorio"

        print(resultado_prediccion)

    return render(request,'index.html', {'form':form})

#    return render(request, 'index.html')

def form_name_view(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)

    if form.is_valid():
        print("VALIDATION SUCCESS!")
        nombre = form.cleaned_data['nombre']
        email = form.cleaned_data['email']
        texto_de_la_solicitud = form.cleaned_data['texto_de_la_solicitud']
        depend = form.cleaned_data['dependencia']
        dependencia = limpiando_dependencia(depend)
        print("NAME: "+form.cleaned_data['nombre'])
        print("EMAIL: "+form.cleaned_data['email'])
        print("Texto: "+form.cleaned_data['texto_de_la_solicitud'])
        print("dependencia: "+form.cleaned_data['dependencia'])
        print("dependencia_SUBMITTED: "+dependencia)
        today =  date.today()
        texto_de_la_solicitud = texto_de_la_solicitud
        dependencia = dependencia

        data = {
            'fechasolicitud': today,
            'descripcionsolicitud': texto_de_la_solicitud,
            'dependencia': dependencia
        }

        df = pd.DataFrame(data, index=[0])

        df['fechasolicitud'] = pd.to_datetime(df['fechasolicitud'])

        df['anosolicitud'] = pd.DatetimeIndex(df['fechasolicitud']).year

        df['messolicitud'] = pd.DatetimeIndex(df['fechasolicitud']).month

        df['semanasolicitud'] = df['fechasolicitud'].dt.week

        df['diasolicitud'] = df['fechasolicitud'].dt.dayofweek

        df = StringLowercase(df)

        df = StringAcentos(df)

        df = StringStrip(df)

        df = StringEspacios(df)

        #nlp = spacy.load('es_core_news_sm')

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

        # generamos dependencia con dummies

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

        #print(df.head())
        #print(len(df))
        #print(features)

        #Ejecución de una predicción

        # session = boto3.session.Session()
        # print(session)
        # s3client = session.client('s3')
        # print(s3client)
        # response = s3client.get_object(Bucket='inai-summerofdata', Key='modeling/GBC/1_temporalidad/1_iteracion/best_gbc.pkl')
        # print(response)
        # print(response['Body'])
        # body = response['Body'].read()
        # print(body)
        # best_gbc = pickle.loads(body)
        #best_gbc = pickle.loads('https://inai-summerofdata.s3-us-west-2.amazonaws.com/modeling/GBC/1_temporalidad/1_iteracion/best_gbc.pkl')


        gbc_pred = best_gbc.predict(features)

        print(gbc_pred)

    return render(request,'formpage.html', {'form':form})




# Modelo
def limpiando_dependencia(depend):
    dummydf = pd.DataFrame({'DEPENDENCIA':depend},index=[0])
    dummydf = fixdependencia.FixDependencia(dummydf)
    depp = dummydf['dependencia_clean'][0]
    return depp


pd.options.display.max_columns = None

# Valor en automatico cuando se realiza una solicitud
#today =  date.today()

######### Estos valures los da el usuario  ########## SE TOMARA UN EJEMPLO
#texto_de_la_solicitud = 'compra de medicamentos en la ciudad de mexico'

# Para esta variable se sugiere un combo box donde el usuario solo pueda seleccionar de los 65 casos de dependencias
# estandarizadas. Si queda libre, tendria que hacerse un estandarizador
#dependencia = 'instituto mexicano del seguro social (imss)'

#####################################################

# data = {
#     'fechasolicitud': today,
#     'descripcionsolicitud': texto_de_la_solicitud,
#     'dependencia': dependencia
# }

#df = pd.DataFrame(data, index=[0])

#df.head()

#df['fechasolicitud'] = pd.to_datetime(df['fechasolicitud'])

# agregamos año de la solicitud
#df['anosolicitud'] = pd.DatetimeIndex(df['fechasolicitud']).year

#df.head()

# agregamos mes de la solicitud
#df['messolicitud'] = pd.DatetimeIndex(df['fechasolicitud']).month

#df.head()

# agregamos semana de la solicitud
#df['semanasolicitud'] = df['fechasolicitud'].dt.week

#df.head()

# agregamos dia de la semana de la solicitud
#df['diasolicitud'] = df['fechasolicitud'].dt.dayofweek

#df.head()

# estandarizamos todo a lower case
def StringLowercase(df):
    """
    Función cambiar todos los strings de un dataframe a lowercase
    (columnas y observaciones)
​
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

#df = StringLowercase(df)

#df.head()

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


#df = StringAcentos(df)
#df.head()

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

#df = StringStrip(df)

#df.head()

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

#df = StringEspacios(df)


# lematizamos texto
#nlp = spacy.load('es_core_news_sm')

def LematizarTexto(texto):

    doc = nlp(texto)
    words = [t.lemma_ for t in doc if not t.is_punct | t.is_stop]
    lexical_tokens = [t.lower() for t in words if len(t) > 3 and t.isalpha()]
    lemmatized_text = ' '.join(lexical_tokens)

    return lemmatized_text


#df['descripcionsolicitud_lemma'] = df['descripcionsolicitud'].map(LematizarTexto)

#df.head()

# # quitamos cloud de palabras revisadas con socialTIC
# session = boto3.session.Session()
# s3client = session.client('s3')
# response = s3client.get_object(Bucket='inai-summerofdata', Key='raw/stopwords.pkl')
# body = response['Body'].read()
# banned = pickle.loads(body)
#
# f = lambda x: ' '.join([item for item in x.split() if item not in banned])
#
# df['descripcionsolicitud_lemma'] = df['descripcionsolicitud_lemma'].apply(f)

#df.head()

# # agregamos longitud del texto de la solicitud lematizada
# df['solicitud_lemma_longitud'] = df['descripcionsolicitud_lemma'].str.len()

#df.head()

# quitamos la columna fecha solicitud
#df = df.drop('fechasolicitud', axis=1)

#df.head()

# # acomodamos las columnas
# columns = ['anosolicitud', 'messolicitud', 'semanasolicitud',
#         'diasolicitud', 'descripcionsolicitud_lemma', 'solicitud_lemma_longitud',
#         'dependencia']
#
# df = df[columns]

#df.head()


# # generamos dependencia con dummies
#
# dep = ['dependencia_clean_administracion portuaria integral',
#  'dependencia_clean_administracion publica federal',
#  'dependencia_clean_aeropuertos y servicios auxiliares (asa)',
#  'dependencia_clean_archivo general de la nación',
#  'dependencia_clean_auditoría superior de la federación',
#  'dependencia_clean_banca de desarrollo',
#  'dependencia_clean_camara de dipuados',
#  'dependencia_clean_capufe',
#  'dependencia_clean_cfe',
#  'dependencia_clean_cnbv',
#  'dependencia_clean_cofepris',
#  'dependencia_clean_conacyt',
#  'dependencia_clean_empresas de participacion estatal',
#  'dependencia_clean_hospitales',
#  'dependencia_clean_inah',
#  'dependencia_clean_inai',
#  'dependencia_clean_ine',
#  'dependencia_clean_instituciones de educacion superior autonomas',
#  'dependencia_clean_instituto del fondo nacional de la vivienda para los trabajadores',
#  'dependencia_clean_instituto federal de telecomunicaciones (ift)',
#  'dependencia_clean_instituto mexicano de la propiedad industrial',
#  'dependencia_clean_instituto mexicano del seguro social (imss)',
#  'dependencia_clean_instituto nacional de migración',
#  'dependencia_clean_ipn',
#  'dependencia_clean_lotenal',
#  'dependencia_clean_organismo autonomo',
#  'dependencia_clean_organismo descentralizado',
#  'dependencia_clean_partidos politicos',
#  'dependencia_clean_pemex',
#  'dependencia_clean_pgr',
#  'dependencia_clean_poder judicial de la federacion',
#  'dependencia_clean_policia federal',
#  'dependencia_clean_presidencia de la republica',
#  'dependencia_clean_procuraduría federal del consumidor',
#  'dependencia_clean_profeco',
#  'dependencia_clean_registro agrario nacional',
#  'dependencia_clean_sader',
#  'dependencia_clean_sae',
#  'dependencia_clean_sagarpa',
#  'dependencia_clean_sat',
#  'dependencia_clean_scjn',
#  'dependencia_clean_sct',
#  'dependencia_clean_se',
#  'dependencia_clean_secretaria de bienestar',
#  'dependencia_clean_secretariado ejecutivo del sistema nacional de seguridad pública',
#  'dependencia_clean_secretaría de cultura',
#  'dependencia_clean_sectur',
#  'dependencia_clean_sedatu',
#  'dependencia_clean_sedena',
#  'dependencia_clean_sedesol',
#  'dependencia_clean_segob',
#  'dependencia_clean_semar',
#  'dependencia_clean_semarnat',
#  'dependencia_clean_senado de la república',
#  'dependencia_clean_sener',
#  'dependencia_clean_sep',
#  'dependencia_clean_sfp',
#  'dependencia_clean_shcp',
#  'dependencia_clean_sindicatos',
#  'dependencia_clean_sre',
#  'dependencia_clean_ssa',
#  'dependencia_clean_sspc',
#  'dependencia_clean_stps',
#  'dependencia_clean_tribunales administrativos',
#  'dependencia_clean_unam']
#
# for d in dep:
#     aux0 = d.split('_')
#     aux1 = df['dependencia'][0]
#     if aux1 == aux0[2]:
#         df[d] = 1
#     else:
#         df[d] = 0

#df.head()

#df = df.drop('dependencia', axis=1)

#df

#features = np.array(df)

#features

# Ejecución de una predicción
#
# session = boto3.session.Session()
# s3client = session.client('s3')
# response = s3client.get_object(Bucket='inai-summerofdata', Key='modeling/GBC/1_temporalidad/1_iteracion/best_gbc.pkl')
# body = response['Body'].read()
# print(body)
# best_gbc = pickle.loads(body)
#
#
# gbc_pred = best_gbc.predict(features)
#
# gbc_pred


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


def as_pyplot_figure_mio(explicacion, label=1, **kwargs):
    """Returns the explanation as a pyplot figure.
    Will throw an error if you don't have matplotlib installed
    Args:
        label: desired label. If you ask for a label for which an
            explanation wasn't computed, will throw an exception.
            Will be ignored for regression explanations.
        kwargs: keyword arguments, passed to domain_mapper
    Returns:
        pyplot figure (barchart).
    """
    import matplotlib.pyplot as plt
    exp = explicacion.as_list(label=label, **kwargs)
    fig = plt.figure()
    vals = [x[1] for x in exp]
    names = [x[0] for x in exp]
    vals.reverse()
    names.reverse()
    colors = ['green' if x > 0 else 'red' for x in vals]
    pos = np.arange(len(exp)) + .5
    plt.barh(pos, vals, align='center', color=colors)
    plt.yticks(pos, names)
    if modo == "classification":
        title = 'Explicacion local para la clase %s' % explicacion.class_names[label]
    else:
        title = 'explicacion local'
    plt.title(title)
    return fig

def as_html_mio(explicacion,sp,labels=None,predict_proba=True,show_predicted_value=True,modo="classification",**kwargs):
    def jsonize(x):
        return json.dumps(x, ensure_ascii=False)

    if labels is None and modo == "classification":
        labels = sp.available_labels()

    this_dir, _ = os.path.split(os.getcwd())
    bundle = open(os.path.join(this_dir, 'bundle.js'),encoding="utf8").read()

    out = u'''<html>
    <meta http-equiv="content-type" content="text/html; charset=UTF8">
    <head><script>%s </script></head><body>''' % bundle
    random_id = id_generator(size=15, random_state=check_random_state(sp.random_state))
    out += u'''
    <div class="lime top_div" id="top_div%s"></div>
    ''' % random_id

    predict_proba_js = ''
    if modo == "classification" and predict_proba:
        predict_proba_js = u'''
        var pp_div = top_div.append('div')
                            .classed('lime predict_proba', true);
        var pp_svg = pp_div.append('svg').style('width', '100%%');
        var pp = new lime.PredictProba(pp_svg, %s, %s);
        ''' % (jsonize([str(x) for x in sp.class_names]),
                jsonize(list(sp.predict_proba.astype(float))))

    predict_value_js = ''
    if modo == "regression" and show_predicted_value:
        # reference explicacion.predicted_value
        # (svg, predicted_value, min_value, max_value)
        predict_value_js = u'''
                var pp_div = top_div.append('div')
                                    .classed('lime predicted_value', true);
                var pp_svg = pp_div.append('svg').style('width', '100%%');
                var pp = new lime.PredictedValue(pp_svg, %s, %s, %s);
                ''' % (jsonize(float(sp.predicted_value)),
                        jsonize(float(sp.min_value)),
                        jsonize(float(sp.max_value)))

    exp_js = '''var exp_div;
        var exp = new lime.Explanation(%s);
    ''' % (jsonize([str(x) for x in sp.class_names]))

    if modo == "classification":
        for label in labels:
            exp = jsonize(sp.as_list(label))
            exp_js += u'''
            exp_div = top_div.append('div').classed('lime explanation', true);
            exp.show(%s, %d, exp_div);
            ''' % (exp, label)
    else:
        exp = jsonize(sp.as_list())
        exp_js += u'''
        exp_div = top_div.append('div').classed('lime explanation', true);
        exp.show(%s, %s, exp_div);
        ''' % (exp, sp.dummy_label)

    raw_js = '''var raw_div = top_div.append('div');'''

    if modo == "classification":
        html_data = sp.local_exp[labels[0]]
    else:
        html_data = sp.local_exp[explicacion.dummy_label]

    raw_js += sp.domain_mapper.visualize_instance_html(
            html_data,
            labels[0] if modo == "classification" else sp.dummy_label,
            'raw_div',
            'exp',
            **kwargs)
    out += u'''
    <script>
    var top_div = d3.select('#top_div%s').classed('lime top_div', true);
    %s
    %s
    %s
    %s
    </script>
    ''' % (random_id, predict_proba_js, predict_value_js, exp_js, raw_js)
    out += u'</body></html>'

    return out

def id_generator(size=15, random_state=None):
    """Helper function to generate random div ids. This is useful for embedding
    HTML into ipython notebooks."""
    chars = list(string.ascii_uppercase + string.digits)
    return ''.join(random_state.choice(chars, size, replace=True))

def save_to_file_mio(explicacion,sp,
                     file_path,
                     labels=None,
                     predict_proba=True,
                     show_predicted_value=True,
                     **kwargs):
    """Saves html explanation to file. .
    Params:
        file_path: file to save explanations to
    See as_html() for additional parameters.
    """
    file_ = open(file_path, 'w', encoding='utf8')
    file_.write(as_html_mio(sp,sp,labels=labels,
                                 predict_proba=predict_proba,
                                 show_predicted_value=show_predicted_value,
                                 modo = "classification",
                                 **kwargs))
