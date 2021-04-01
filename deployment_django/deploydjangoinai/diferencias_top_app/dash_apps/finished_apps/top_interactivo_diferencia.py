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
diferencias_top = pd.read_csv('/home/ubuntu/score-respuesta-inai/deployment_django/deploydjangoinai/diferencias_top_app/dash_apps/finished_apps/diferencias_top.csv')
diferencias_top = diferencias_top.sort_values('diferencia', ascending = False)
respaldo = pd.read_csv('/home/ubuntu/score-respuesta-inai/deployment_django/deploydjangoinai/diferencias_top_app/dash_apps/finished_apps/diferencias_top.csv')
df = diferencias_top.copy()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('top_interactivo_diferencia', external_stylesheets=external_stylesheets)

available_indicators = diferencias_top['dependencia_clean']

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

###################total#######

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

    df = diferencias_top.copy()
    df2 = diferencias_top.copy()

    if (vec_bool==[True,True,True]): #caso 1
        df=df[df['año_dependencia']==ano]
        df=df[df['dependencia_clean']==dep]
    elif (vec_bool==[True,True,False]): #caso 2
        df=df[df['año_dependencia']==ano]
        df=df[df['dependencia_clean']==dep]
    elif vec_bool==[True,False,True]: # Caso 3
        df = df[df['año_dependencia']==ano]
        df=df.sort_values('diferencia', ascending = False)
        df = df.head(top)
    elif vec_bool==[True,False,False]: # Caso 4
        df = df[df['año_dependencia']==ano]
        df=df.sort_values('diferencia', ascending = False)
    elif vec_bool==[False,True,True]: # Caso 5
        df = df[df['dependencia_clean']==dep]
        df=df.sort_values('año_dependencia', ascending = True)
    elif vec_bool==[False,True,False]: # Caso 6
        df = df[df['dependencia_clean']==dep]
        df=df.sort_values('año_dependencia', ascending = True)
    elif vec_bool==[False,False,True]: # Caso 7
        df = respaldo.copy()
        df=df.sort_values('diferencia', ascending = False)
        df = df.head(top)

    x_ultima = list(df2['dependencia_clean'].unique())

    data = {
        "x":x_ultima,
        "año_dependencia": df['año_dependencia'],
        "diferencia": df['diferencia'],
    }



    trace1 = go.Bar(
                name="diferencia",
                x=data["x"],
                y=data["diferencia"],
                offsetgroup=0,
                marker=dict(color='blue',opacity=0.5),
            )


    data1 = [trace1]

    layout=go.Layout(
        title="Comparacion de calidad de respuesta  y calidad de respuesta real por año por dependencia",
        yaxis_title="Conteo"
        #barmode='group'
    )

    g = go.FigureWidget(data=data1,layout=layout)



    return g






#
#if __name__ == '__main__':
#    app.run_server(debug=True)
#
