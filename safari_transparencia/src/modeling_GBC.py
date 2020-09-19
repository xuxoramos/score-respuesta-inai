import boto3
import pickle
import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt
from dateutil.relativedelta import *
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from pprint import pprint



session = boto3.session.Session()
s3client = session.client('s3')

response = s3client.get_object(Bucket='inai-summerofdata', Key='mlpreproc/pickles_temporalidad/df_preproc.pkl')
body = response['Body'].read()
dum_df = pickle.loads(body)

response = s3client.get_object(Bucket='inai-summerofdata', Key='mlpreproc/pickles_temporalidad/index_cv_split.pkl')
body = response['Body'].read()
index_output = pickle.loads(body)

drop_columns = ['folio', 'codigo_calidad_respuesta_real']

X = dum_df.drop(drop_columns, axis=1)
y = pd.DataFrame(dum_df['codigo_calidad_respuesta_real'])

features_cv = np.array(X.drop('fechasolicitud', axis=1))
labels_cv = np.array(y)
labels_cv = np.ravel(labels_cv)

ngram_range = (1, 2)
min_df = 10
max_df = 1.
max_f = 300

preprocess = ColumnTransformer(
    [('descripcionsolicitud_tfidf', TfidfVectorizer(encoding='utf-8',
                                        ngram_range=ngram_range,
                                        stop_words=None,
                                        lowercase=False,
                                        max_df=max_df,
                                        min_df=min_df,
                                        max_features=max_f,
                                        norm='l2',
                                        sublinear_tf=True), 4)],
    remainder='passthrough')


clf = GradientBoostingClassifier(random_state=8)

gbc = Pipeline([('preprocess', preprocess), ('clf', clf)])

max_depth = [5, 10, 15]
max_features = ['auto']
min_samples_leaf = [1, 5, 7, 9]
min_samples_split = [10, 20]
n_estimators = [800, 1000, 1300]
learning_rate = [.1, .5]
subsample = [.5]

param_grid = {
    'clf__max_depth': max_depth,
    'clf__max_features': max_features,
    'clf__min_samples_leaf': min_samples_leaf,
    'clf__min_samples_split': min_samples_split,
    'clf__n_estimators': n_estimators,
    'clf__learning_rate': learning_rate,
    'clf__subsample': subsample
}

pprint(param_grid)

grid_search = GridSearchCV(estimator=gbc,
                          param_grid=param_grid,
                          scoring='accuracy',
                          cv=index_output,
                          n_jobs=-1,
                          verbose=1)

grid_search.fit(features_cv , labels_cv)

print("Best Parameters:", grid_search.best_params_)

print("Best Score:", grid_search.best_score_)

bucket='inai-summerofdata'
key='modeling/GBC/1_temporalidad/2_iteracion/grid_search.pkl'
pickle_byte_obj = pickle.dumps(grid_search)
s3_resource = boto3.resource('s3')
s3_resource.Object(bucket, key).put(Body=pickle_byte_obj)

best_gbc = grid_search.best_estimator_


training_accuracy = []
test_accuracy = []
for train_index, test_index in index_output:

    features_train = np.array(X.loc[train_index].drop('fechasolicitud', axis=1))
    labels_train = np.ravel(y.loc[train_index])

    features_test = np.array(X.loc[test_index].drop('fechasolicitud', axis=1))
    labels_test = np.ravel(y.loc[test_index])

    # Modeling train data
    best_gbc.fit(features_train, labels_train)

    # Predictions
    gbc_pred = best_gbc.predict(features_test)

    # Training accuracy
    training_accuracy.append(accuracy_score(labels_train, best_gbc.predict(features_train)))

    # Test accuracy
    test_accuracy.append(accuracy_score(labels_test, gbc_pred))


average_training_accuracy = np.mean(training_accuracy)
average_test_accuracy = np.mean(test_accuracy)

print("Average Training Accuracy:", average_training_accuracy)
print("Average Test Accuracy:", average_test_accuracy)


data = {
    'Modelo': 'GBC',
    'Average Training Set Accuracy': average_training_accuracy,
    'Average Test Set Accuracy': average_test_accuracy
}

df_models_gbc = pd.DataFrame(data, index=[0])

print(df_models_gbc)

features = np.array(X.drop('fechasolicitud', axis=1))
labels = np.ravel(y)

bucket='inai-summerofdata'
key='modeling/GBC/1_temporalidad/2_iteracion/features.pkl'
pickle_byte_obj = pickle.dumps(features)
s3_resource = boto3.resource('s3')
s3_resource.Object(bucket, key).put(Body=pickle_byte_obj)

bucket='inai-summerofdata'
key='modeling/GBC/1_temporalidad/2_iteracion/labels.pkl'
pickle_byte_obj = pickle.dumps(labels)
s3_resource = boto3.resource('s3')
s3_resource.Object(bucket, key).put(Body=pickle_byte_obj)

bucket='inai-summerofdata'
key='modeling/GBC/1_temporalidad/2_iteracion/df_models_gbc.pkl'
pickle_byte_obj = pickle.dumps(df_models_gbc)
s3_resource = boto3.resource('s3')
s3_resource.Object(bucket, key).put(Body=pickle_byte_obj)

bucket='inai-summerofdata'
key='modeling/GBC/1_temporalidad/2_iteracion/best_gbc.pkl'
pickle_byte_obj = pickle.dumps(best_gbc)
s3_resource = boto3.resource('s3')
s3_resource.Object(bucket, key).put(Body=pickle_byte_obj)
