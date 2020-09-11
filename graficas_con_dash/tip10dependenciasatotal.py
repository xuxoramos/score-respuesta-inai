import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import pandas as pd



lista_g = pd.read_csv('lista_g.csv')
respaldo = pd.read_csv('respaldo.csv')

def filtra_df_plot(df, ano, dep, top, uso_ano = False,uso_dep = False,uso_top = False):
    vec_bool = [uso_ano,uso_dep,uso_top]

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
#    else: #vec_bool==[False,False,False]: # Caso 8
#        df = respaldo.copy()
        #df=df.sort_values('total', ascending = False)

    return df


x_ultima = list(lista_g['dependencia_clean'].unique())

data = {
    "x":x_ultima,
    "año_dependencia": lista_g['año_dependencia'],
    "calidad_original_en_proceso": lista_g['calidad_original_en_proceso'],
    "calidad_original_no_respondida": lista_g['calidad_original_no_respondida'],
    "calidad_original_satisfactoria": lista_g['calidad_original_satisfactoria'],
    "calidad_real_en_proceso": lista_g['calidad_real_en_proceso'],
    "calidad_real_no_respondida": lista_g['calidad_real_no_respondida'],
    "calidad_real_satisfactoria": lista_g['calidad_real_satisfactoria'],
    "total": lista_g['total'],
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

layout=go.Layout(
    title="Comparacion de calidad de respuesta  y calidad de respuesta real por año por dependencia",
    yaxis_title="Conteo"
    #barmode='group'
)


g = go.FigureWidget(data=data1,layout=layout)



def validate():
    if dependencia_listbox.value in lista_g['dependencia_clean'].unique():
        return True
    else:
        return False


def response(change):
    if validate():

        temp_df = filtra_df_plot(lista_g, ano = year.value, dep = dependencia_listbox.value,
                                 top =top_listbox.value, uso_ano = use_date,uso_dep = use_dep.value,
                                 uso_top = use_top.value)



        x1 = temp_df['dependencia_clean']
        y1 = temp_df['calidad_original_en_proceso']
        y2 = temp_df['calidad_original_no_respondida']
        y3 = temp_df['calidad_original_satisfactoria']
        y4 = temp_df['calidad_real_en_proceso']
        y5 = temp_df['calidad_real_no_respondida']
        y6 = temp_df['calidad_real_satisfactoria']
        with g.batch_update():
            temp_df = filtra_df_plot(lista_g, ano = year.value, dep = dependencia_listbox.value,
                                 top =top_listbox.value, uso_ano = use_date,uso_dep = use_dep.value,
                                 uso_top = use_top.value)
            x1 = temp_df['dependencia_clean']
            y1 = temp_df['calidad_original_en_proceso']
            y2 = temp_df['calidad_original_no_respondida']
            y3 = temp_df['calidad_original_satisfactoria']
            y4 = temp_df['calidad_real_en_proceso']
            y5 = temp_df['calidad_real_no_respondida']
            y6 = temp_df['calidad_real_satisfactoria']

            g.data[0].x = x1
            g.data[1].x = x1
            g.data[2].x = x1
            g.data[3].x = x1
            g.data[4].x = x1
            g.data[5].x = x1

            g.data[0].y = y1
            g.data[1].y = y2
            g.data[2].y = y3
            g.data[3].y = y4
            g.data[4].y = y5
            g.data[5].y = y6

            g.data[1].base =y1
            g.data[2].base =y1+y2
            g.data[4].base=y4
            g.data[5].base=y4+y5



            #g.layout.barmode = 'stack'


year.observe(response, names="value")
dependencia_listbox.observe(response, names="value")
top_listbox.observe(response, names="value")

#use_date.observe(response, names="value")
use_dep.observe(response, names="value")
use_top.observe(response, names="value")


grafica_final=widgets.VBox([container,
              container2,
              container3,
              #container4,
              g])

grafica_final

app = dash.Dash()

app.layout = html.Div(children = [
            html.H1('Hello Dash!'),
            html.Div('Dash: Web Dashboards with Python'),
            dcc.Graph(id='example',
                        figure={'data':data,
                        'layout':layout
                        })

])

if __name__ == '__main__':
    app.run_server()
