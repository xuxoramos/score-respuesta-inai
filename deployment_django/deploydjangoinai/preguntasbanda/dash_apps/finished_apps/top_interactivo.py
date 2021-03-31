import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px 
import numpy as np
import pandas as pd
import plotly.graph_objects as go 
from django_plotly_dash import DjangoDash
import os

print("el path es:",os.getcwd())

lista_g = pd.read_csv('/home/rafaelortega/Documentos/INAI_consultas/inai_rafaelortegar/deployment_django/deploydjangoinai/preguntasbanda/dash_apps/finished_apps/lista_g.csv')
respaldo = pd.read_csv('/home/rafaelortega/Documentos/INAI_consultas/inai_rafaelortegar/deployment_django/deploydjangoinai/preguntasbanda/dash_apps/finished_apps/respaldo.csv')
df = lista_g.copy()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('top_interactivo', external_stylesheets=external_stylesheets)

available_indicators = lista_g['dependencia_clean']

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='dep',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='cfe'
            ),
            dcc.Checklist(
                id='activaciones',
                options=[
                    {'label': 'Usar Dependencia', 'value': 'uso_dep'},
                    {'label': 'Usar Top', 'value': 'uso_top'}
                ],
                value=[]
            ),
            html.Div(dcc.Slider(
                id='year--slider',
                min=df['año_dependencia'].min(),
                max=df['año_dependencia'].max(),
                value=df['año_dependencia'].max(),
                marks={str(year): str(year) for year in df['año_dependencia'].unique()},
                step=1
            ), style={ 'padding': '0px 20px 20px 20px'}),
            html.Div(dcc.Slider(
                id='top--slider',
                min=1,
                max=df['dependencia_clean'].nunique(),
                value=df['dependencia_clean'].nunique(),
                marks={str(topp): str(topp) for topp in range(0,df['dependencia_clean'].nunique())},
                step=1
            ), style={ 'padding': '0px 20px 20px 20px'})
        ],
        style={'width': '90%', 'display': 'inline-block'}),

    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='graph',
            hoverData={'points': [{'customdata': 'cfe'}]}
        )
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        html.Div(id='my_div')
    ])
]) 

##########################

#@app.callback(Output(component_id='my_div', component_property='children'),
#              [Input(component_id='activaciones',component_property='value')]    
#)
#def imprime(input_value):
#    return "Ingresaste{}".format(input_value)



@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dep', 'value'),
     dash.dependencies.Input('activaciones', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
     dash.dependencies.Input('top--slider','value')])
def update_graph(dep,
                 activaciones,
                 year_value,
                 top_value):
    
    vector = activaciones
    
    uso_ano = True
    
    if 'uso_dep' in vector:
        uso_dep = True
    else:
        uso_dep= False
    
    if 'uso_top' in vector:
        uso_top = True
    else:
        uso_top = False
    
    ano = year_value
    top = top_value
    
    vec_bool = [uso_ano,uso_dep,uso_top]
    
    df = lista_g.copy()
    df2 = lista_g.copy()
    
    if (vec_bool==[True,True,True]): #caso 1
        df=df[df['año_dependencia']==ano]
        df=df[df['dependencia_clean']==dep]
    elif (vec_bool==[True,True,False]): #caso 2
        df=df[df['año_dependencia']==ano]
        df=df[df['dependencia_clean']==dep]
    elif vec_bool==[True,False,True]: # Caso 3
        df = df[df['año_dependencia']==ano]
        df=df.sort_values('total', ascending = False)
        df = df.head(top)
    elif vec_bool==[True,False,False]: # Caso 4
        df = df[df['año_dependencia']==ano]
        df=df.sort_values('total', ascending = False)
    elif vec_bool==[False,True,True]: # Caso 5
        df = df[df['dependencia_clean']==dep]
        df=df.sort_values('año_dependencia', ascending = True)
    elif vec_bool==[False,True,False]: # Caso 6
        df = df[df['dependencia_clean']==dep]
        df=df.sort_values('año_dependencia', ascending = True)
    elif vec_bool==[False,False,True]: # Caso 7
        df = respaldo.copy()
        df=df.sort_values('total', ascending = False)
        df = df.head(top)
        
    x_ultima = list(df2['dependencia_clean'].unique())

    data = {
        "x":x_ultima,
        "año_dependencia": df['año_dependencia'],
        "calidad_original_en_proceso": df['calidad_original_en_proceso'],
        "calidad_original_no_respondida": df['calidad_original_no_respondida'],
        "calidad_original_satisfactoria": df['calidad_original_satisfactoria'],
        "calidad_real_en_proceso": df['calidad_real_en_proceso'],
        "calidad_real_no_respondida": df['calidad_real_no_respondida'],
        "calidad_real_satisfactoria": df['calidad_real_satisfactoria'],
        "total": df['total'],
    }



    trace1 = go.Bar(
                name="calidad_original_en_proceso",
                x=data["x"],
                y=data["calidad_original_en_proceso"],
                offsetgroup=0,
                marker=dict(color='blue',opacity=0.5),
            )
    trace2 = go.Bar(
                name="calidad_original_no_respondida",
                x=data["x"],
                y=data["calidad_original_no_respondida"],
                offsetgroup=0,
                base=data["calidad_original_en_proceso"],
                marker=dict(color='red',opacity=0.5),

            )

    trace3 = go.Bar(
                name="calidad_original_satisfactoria",
                x=data["x"],
                y=data["calidad_original_satisfactoria"],
                offsetgroup=0,
                base=data["calidad_original_no_respondida"]+data["calidad_original_en_proceso"],
                marker=dict(color='green',opacity=0.5),
            )


    trace4 = go.Bar(
                name="calidad_real_en_proceso",
                x=data["x"],
                y=data["calidad_real_en_proceso"],
                offsetgroup=1,
                #base=data["model_1"],
                marker=dict(color='blue',opacity=0.5),
            )
    trace5 = go.Bar(
                name="calidad_real_no_respondida",
                x=data["x"],
                y=data["calidad_real_no_respondida"],
                offsetgroup=1,
                base=data["calidad_real_en_proceso"],
                marker=dict(color='red',opacity=0.5),
            )
    trace6 = go.Bar(
                name="calidad_real_satisfactoria",
                x=data["x"],
                y=data["calidad_real_satisfactoria"],
                offsetgroup=1,
                base=data["calidad_real_no_respondida"]+data["calidad_real_en_proceso"],
                marker=dict(color='green',opacity=0.5),
            )
    
    
    data1 = [trace1,trace2,trace3,trace4,trace5,trace6]
    
    #margin=go.Margin(
    #l=250
    ##r=100
    #)
    
    layout=go.Layout(
        title="Comparacion de calidad de respuesta  y calidad de respuesta real por año por dependencia",
        yaxis_title="Conteo"#, margin=margin
        #barmode='group'
    )
    
    #layout.xaxis(automargin=True)
    
    g = go.FigureWidget(data=data1,layout=layout)    
    
    return g
    






#if __name__ == '__main__':
#    app.run_server(debug=True)