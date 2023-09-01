# bibliotecas necesarias para crear una aplicación web interactiva utilizando Dash. dash es el marco principal de la aplicación, dash_core_components proporciona componentes gráficos interactivos y dash_html_components permite crear elementos HTML dentro de la aplicación.
import dash
import dash_core_components as dcc
import dash_html_components as html

#Aquí, se importan las clases Input y Output de dash.dependencies, que se utilizan para establecer las dependencias entre las entradas y salidas en la aplicación Dash. También se importa ClientsideFunction, que es una función que se ejecuta en el lado del cliente (navegador). Además, se importa dash_bootstrap_components que es una biblioteca para usar estilos y componentes de Bootstrap con Dash
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc

#Estas líneas importan la clase Dash de Dash, así como los módulos html y dcc que proporcionan funciones para crear elementos HTML y componentes interactivos, respectivamente.
from dash import Dash, html, dcc

# Aquí se importan los módulos plotly.express y plotly.graph_objects, que son bibliotecas para la creación de gráficos interactivos.
import plotly.express as px
import plotly.graph_objects as go

# Se importan las bibliotecas numpy para operaciones matemáticas, pandas para el manejo de datos en forma de marcos de datos y json para trabajar con datos en formato JSON
import numpy as np
import pandas as pd
import json

# Aquí se definen dos variables CENTER_LAT y CENTER_LON con valores específicos de latitud y longitud. Estos valores parecen representar el centro geográfico de algún lugar.
CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474


# =====================================================================
# Data Generation
# df = pd.read_csv("HIST_PAINEL_COVIDBR_13mai2021.csv", sep=";")
# df_states = df[(~df["estado"].isna()) & (df["codmun"].isna())]
# df_brasil = df[df["regiao"] == "Brasil"]
# df_states.to_csv("df_states.csv")
# df_brasil.to_csv("df_brasil.csv")

# =====================================================================
# Estas líneas leen archivos CSV y crean dos marcos de datos (DataFrames) en Pandas. df_states y df_brasil son utilizados para almacenar datos relacionados con estados y datos generales de Brasil, respectivamente
df_states = pd.read_csv("df_states.csv") 
df_brasil = pd.read_csv("df_brasil.csv")

# Aquí se lee el contenido del archivo .mapbox_token, que probablemente contiene un token de acceso a Mapbox. Este token se utiliza para acceder a los servicios de Mapbox, como la visualización de mapas en la aplicación Dash.
token = open(".mapbox_token").read()

# Esta línea carga un archivo JSON llamado brazil_geo.json que contiene datos geográficos de los estados de Brasil en formato GeoJSON. El contenido del archivo se almacena en la variable brazil_states.
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

# accede a las claves (keys) del primer elemento en la lista de características dentro del diccionario brazil_states. Esto ayuda a comprender qué información está disponible para cada estado en los datos geográficos
brazil_states["features"][0].keys()

# Aquí se crea un nuevo DataFrame df_states_ al filtrar el DataFrame df_states para incluir solo las filas correspondientes a la fecha "2020-05-13" para trabajar con datos específicos de esa fecha.
df_states_ = df_states[df_states["data"] == "2020-05-13"]
select_columns = {"casosAcumulado": "Casos Acumulados", 
                "casosNovos": "Novos Casos", 
                "obitosAcumulado": "Óbitos Totais",
                "obitosNovos": "Óbitos por dia"}


# =====================================================================
# Se crea una instancia de la aplicación Dash llamada app. Se utiliza el tema CYBORG de Bootstrap para aplicar un estilo visual a la aplicación.
app = Dash(external_stylesheets=[dbc.themes.CYBORG])

# Se crea un gráfico de mapa de coropletas usando Plotly Express (px). Se utiliza el DataFrame df_states_ como fuente de datos. El mapa muestra datos de casos nuevos por estado en Brasil. Se especifican ubicaciones, datos geográficos (GeoJSON), centro del mapa, nivel de zoom, escala de color, opacidad y datos para la información al pasar el cursor (hover).
fig = px.choropleth_mapbox(df_states_, 
                           locations="estado",
                           geojson=brazil_states, 
                           center={"lat": -16.95, "lon": -47.78},  # https://www.google.com/maps/ -> right click -> get lat/lon
                           zoom=4, 
                           color="casosNovos", 
                           color_continuous_scale="Redor", 
                           opacity=0.4,
                           hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": True}
    )

# Se actualizan las configuraciones del diseño del gráfico (fig) utilizando el método update_layout(). Aquí se podría incluir el token de acceso a Mapbox (mapbox_accesstoken) si estuviera disponible. Se establece el color de fondo del papel, el estilo de Mapbox, el tamaño automático, los márgenes y se oculta la leyenda.
fig.update_layout(
                # mapbox_accesstoken=token,
                paper_bgcolor="#242424",
                mapbox_style="carto-darkmatter",
                autosize=True,
                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                showlegend=False,)

# Se crea un DataFrame df_data al filtrar el DataFrame df_states para incluir solo las filas correspondientes al estado "RO" (Rondônia). Este DataFrame se utiliza para crear un gráfico de líneas que muestra el número de casos acumulados en Rondônia a lo largo del tiempo.
df_data = df_states[df_states["estado"] == "RO"]

# Se crea una instancia de un gráfico vacío utilizando go.Figure() del módulo plotly.graph_objects (go). El parámetro layout se establece con un diccionario que tiene la clave "template" y el valor "plotly_dark". Esto configura el estilo de trazado en modo oscuro.
fig2 = go.Figure(layout={"template":"plotly_dark"})

# Se agrega una línea a la figura fig2 utilizando go.Scatter(). Se utiliza el DataFrame df_data para los valores de los ejes x e y. La columna "data" se utiliza en el eje x y la columna "casosAcumulado" se utiliza en el eje y. Esto crea un trazado de dispersión (scatter plot) de los casos acumulados a lo largo del tiempo.
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))

# Se actualizan las configuraciones del diseño de fig2 utilizando el método update_layout(). Se cambia el color de fondo del papel y del área del trazado a #242424, que es un tono oscuro. También se establece autosize en True para que el tamaño del gráfico se ajuste automáticamente al espacio disponible, y se ajustan los márgenes en cada lado del gráfico.
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, b=10, t=10),
    )


# =====================================================================
# Layout 
# Configuración del diseño de la aplicación
app.layout = dbc.Container(
    children=[
        # Fila con columnas para la interfaz de usuario
        dbc.Row([
            # Columna izquierda
            dbc.Col([
                    # Elementos visuales como logo, título y botón
                    html.Div([
                        # Logo
                        html.Img(id="logo", src=app.get_asset_url("logo.png"), height=50),
                        # Título
                        html.H5(children="COVID-19"),
                        # Botón de ubicación
                        dbc.Button("BRASIL", color="primary", id="location-button", size="lg")
                    ], style={"background-color": "#1E1E1E", "margin": "-25px", "padding": "25px"}),
                    
                    # Selector de fecha
                    html.P("Informe la fecha en la que desea obtener información:", style={"margin-top": "40px"}),
                    html.Div(
                            className="div-for-dropdown",
                            id="div-test",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=df_states.groupby("estado")["data"].min().max(),
                                    max_date_allowed=df_states.groupby("estado")["data"].max().min(),
                                    initial_visible_month=df_states.groupby("estado")["data"].min().max(),
                                    date=df_states.groupby("estado")["data"].max().min(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),

                    # Tarjetas de estadísticas
                    dbc.Row([
                        dbc.Col([dbc.Card([
                                # Contenido de la tarjeta
                                dbc.CardBody([
                                    html.Span("Casos recuperados", className="card-text"),
                                    html.H3(style={"color": "#adfc92"}, id="casos-recuperados-text"),
                                    html.Span("Em acompanhamento", className="card-text"),
                                    html.H5(id="em-acompanhamento-text"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF"})], md=4),
                        # ... Otras tarjetas similares
                    ]),

                    # Selector de tipo de dato
                    html.Div([
                        html.P("Selecione que tipo de dado deseja visualizar:", style={"margin-top": "25px"}),
                        dcc.Dropdown(
                            id="location-dropdown",
                            options=[{"label": j, "value": i}
                                for i, j in select_columns.items()
                            ],
                            value="casosNovos",
                            style={"margin-top": "10px"}
                        ),
                        # Gráfico de línea
                        dcc.Graph(id="line-graph", figure=fig2, style={
                            "background-color": "#242424",
                        }),
                    ], id="teste")
                ], md=5, style={
                    "padding": "25px",
                    "background-color": "#242424"
                }),

            # Columna derecha
            dbc.Col(
                [
                    # Gráfico de mapa coroplético
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[dcc.Graph(id="choropleth-map", figure=fig, 
                            style={'height': '100vh', 'margin-right': '10px'})],
                    ),
                ], md=7),
            ], no_gutters=True)
    ], fluid=True, 
)

# =====================================================================
# Interactivity
# Definición de una función de retroalimentación que actualizará varios componentes de salida
def display_status(date, location):
    # Comprobación de la ubicación y selección de los datos correspondientes
    if location == "BRASIL":
        # Si la ubicación es "BRASIL", se seleccionan los datos correspondientes de df_brasil para la fecha dada
        df_data_on_date = df_brasil[df_brasil["data"] == date]
    else:
        # Si la ubicación es un estado específico, se seleccionan los datos de df_states para ese estado y fecha
        df_data_on_date = df_states[(df_states["estado"] == location) & (df_states["data"] == date)]

    # Formateo de los valores y manejo de casos nulos
    recuperados_novos = "-" if df_data_on_date["Recuperadosnovos"].isna().values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",", ".") 
    acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna().values[0]  else f'{int(df_data_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(",", ".") 
    casos_acumulados = "-" if df_data_on_date["casosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".") 
    casos_novos = "-" if df_data_on_date["casosNovos"].isna().values[0]  else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",", ".") 
    obitos_acumulado = "-" if df_data_on_date["obitosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",", ".") 
    obitos_novos = "-" if df_data_on_date["obitosNovos"].isna().values[0]  else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",", ".") 
    
    # Devolución de los valores actualizados para los textos en la interfaz de usuario
    return (
            recuperados_novos, 
            acompanhamentos_novos, 
            casos_acumulados, 
            casos_novos, 
            obitos_acumulado, 
            obitos_novos,
            )


# Definición de la función que actualiza el gráfico de líneas
def plot_line_graph(plot_type, location):
    # Seleccionar los datos según la ubicación elegida
    if location == "BRASIL":
        df_data_on_location = df_brasil.copy()  # Copiar datos de Brasil
    else:
        df_data_on_location = df_states[(df_states["estado"] == location)]  # Datos del estado elegido
    
    # Crear una nueva figura de Plotly con el estilo oscuro
    fig2 = go.Figure(layout={"template":"plotly_dark"})
    
    # Lista de tipos de gráficos de barras
    bar_plots = ["casosNovos", "obitosNovos"]

    # Agregar trazos al gráfico según el tipo de gráfico seleccionado
    if plot_type in bar_plots:
        fig2.add_trace(go.Bar(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    else:
        fig2.add_trace(go.Scatter(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    
    # Actualizar configuraciones del diseño del gráfico
    fig2.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
    )
    
    # Devolver la figura actualizada para actualizar el gráfico en la interfaz de usuario
    return fig2

# Definición de la función que actualiza el gráfico de mapa coroplético
def update_map(date):
    # Filtrar los datos por la fecha seleccionada
    df_data_on_states = df_states[df_states["data"] == date]

    # Crear un gráfico de mapa coroplético utilizando Plotly Express
    fig = px.choropleth_mapbox(df_data_on_states, locations="estado", geojson=brazil_states, 
        center={"lat": CENTER_LAT, "lon": CENTER_LON},  # Coordenadas del centro del mapa
        zoom=4, color="casosAcumulado", color_continuous_scale="Redor", opacity=0.55,
        hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": False}
        )

    # Actualizar configuraciones del diseño del gráfico
    fig.update_layout(paper_bgcolor="#242424", mapbox_style="carto-darkmatter", autosize=True,
                    margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    
    # Devolver el gráfico de mapa coroplético actualizado para la interfaz de usuario
    return fig


# @app.callback: Define una función de retroalimentación (callback) en la aplicación Dash.
# Output("location-button", "children"): Indica que esta función actualizará el contenido del componente con el ID "location-button". La propiedad "children" es el contenido dentro del componente.
# [Input("choropleth-map", "clickData"), Input("location-button", "n_clicks")]: Especifica las entradas que desencadenarán la función de retroalimentación. Estas son el evento de hacer clic en # el mapa coroplético con ID "choropleth-map" y el número de clics en el botón con ID "location-button".
@app.callback(
    Output("location-button", "children"),
    [Input("choropleth-map", "clickData"), Input("location-button", "n_clicks")]
)

# Define la función update_location, que toma dos argumentos: click_data y n_clicks. Estos argumentos corresponden a las entradas especificadas en el decorador @app.callback.
def update_location(click_data, n_clicks):
    
    # Obtiene la identificación del elemento que causó la llamada a la función. Utiliza dash.callback_context.triggered para acceder a la información sobre el contexto del callback.
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    # Comprueba si hay datos de clic (click_data) y si el cambio no fue causado por el botón ("location-button.n_clicks"). Si es así, obtiene la ubicación (estado) del punto en el que se hizo clic en el mapa coroplético.
    if click_data is not None and changed_id != "location-button.n_clicks":
        
        # Si se hizo clic en el mapa, obtiene la ubicación (estado) del punto en el que se hizo clic en el mapa coroplético.
        state = click_data["points"][0]["location"]
        
        #Si se hizo clic en el mapa y no fue causado por el botón, devuelve el nombre del estado como texto que se mostrará en el botón.
        return "{}".format(state)
    
    # Si no se hizo clic en el mapa o el cambio fue causado por el botón, devuelve "BRASIL" como texto que se mostrará en el botón.
    else:
        return "BRASIL"

# Esta línea verifica si el archivo está siendo ejecutado como el programa principal.
# Si es así, inicia el servidor de la aplicación Dash para que pueda ser accesible en el navegador. El modo de depuración (debug) está configurado como False, y el puerto es establecido en 8051.
if __name__ == "__main__":
    app.run_server(debug=False, port=8051)