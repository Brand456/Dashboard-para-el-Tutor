import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import random
import dash_table
import os
# Inicializar la aplicación de Dash

df_url_porcentajes = 'https://raw.githubusercontent.com/Brand456/CSV-Files/main/Archivo_de_ingenieria_porcentajes.csv'
df_url_calificaciones = 'https://raw.githubusercontent.com/Brand456/CSV-Files/main/Archivo_de_ingenieria.csv'
df_url_totales = 'https://raw.githubusercontent.com/Brand456/CSV-Files/main/Archivo_de_ingenieria_totales.csv'
df_url_datos = 'https://raw.githubusercontent.com/Brand456/CSV-Files/main/Archivo_de_ingenieria_datos.csv'

df = pd.read_csv(df_url_porcentajes, encoding='utf-8', delimiter=',')
df_calificaciones = pd.read_csv(df_url_calificaciones,  encoding='utf-8',delimiter=',')
df_totales = pd.read_csv(df_url_totales,  encoding='utf-8', delimiter=',')
df_pie = pd.read_csv(df_url_datos,  encoding='utf-8', delimiter=',')

dfTI_url_porcentajes = 'https://raw.githubusercontent.com/Brand456/CSV-Files/main/Archivo_de_TIC_porcentajes.csv'
dfTI_url_calificaciones = 'https://raw.githubusercontent.com/Brand456/CSV-Files/main/Archivo_de_TIC.csv'
dfTI_url_totales = 'https://raw.githubusercontent.com/Brand456/CSV-Files/main/Archivo_de_TIC_totales.csv'
dfTI_url_datos = 'https://raw.githubusercontent.com/Brand456/CSV-Files/main/Archivo_de_TIC_datos.csv'

#segundos datos
df_TE =pd.read_csv(dfTI_url_porcentajes, encoding='utf-8', delimiter=',')
df_calificaciones_TE = pd.read_csv(dfTI_url_calificaciones,  encoding='utf-8', delimiter=',')
df_totales_TE = pd.read_csv(dfTI_url_totales,  encoding='utf-8', delimiter=',')
df_pie_TE = pd.read_csv(dfTI_url_datos,  encoding='utf-8', delimiter=',')

external_stylesheets = ['estilo_offcanvas.css']
combined_df = pd.concat([df.assign(Tipo='Ingeniería'), df_TE.assign(Tipo='Licenciatura')])
category_order = combined_df['Nombres'].unique()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server



semestres = {
    'General': ['Primavera 2018', 'Verano 2018', 'Otoño 2018', 'Primavera 2019', 'Verano 2019', 'Otoño 2019', 'Primavera 2020', 'Otoño 2020', 'Primavera 2021', 'Verano 2021', 'Otoño 2021', 'Primavera 2022', 'Verano 2022', 'Otoño 2022', 'Primavera 2023', 'Verano 2023'],
    'Semestre 1': ['Metodologia de la programacion', 'Algebra Superior', 'Formacion Humana y Social', 'Lengua Extranjera 1', 'Matemáticas'],
    'Semestre 2': ['Calculo Diferencial', 'Fisica I', 'Álgebra Lineal Con Elementos En Geo AN', 'Programacion I',  'Lengua Extranjera II', 'DHPC'],
    'Semestre 3': ['Calculo Integral', 'Fisica II', 'Matemáticas Discretas', 'Programación II', 'Ensamblador','Lengua Extranjera III' ],
    'Semestre 4': ['Ecuaciones Diferencial', 'Circuitos Eléctricos','Graficacion','Estructura de Datos','Lengua Extranjera IV'],
    'Semestre 5': ['Probab y Estadistica','Circuitos Electrónicos','Sistemas Operativos I','Análisis y Diseño de Algoritmos','Ingenieria de Software'],
    'Semestre 6': ['Modelos de Redes','Diseño Digital','Bases de Datos para Ingenieria','Sistemas Operativos II','Administracion de Proyectos'],
    'Semestre 7': ['Redes Inalámbricas','Mineria de Datos','Arquitectura de Comp','Programacion Concurrente y Paralela','Desarrollo de Aplicaciones Web'], 
    'Semestre 8': ['Teoría de Control','Administracion de redes','Tecnicas de Inteligencia Artificial','Programacion Distribuida Aplicada','Desarrollo de Aplicaciones Moviles','Optativa I'], 
    'Semestre 9': ['Intercomun. Y Seguridad en Redes','Sistemas Empotrados','Optativa II'],
    'Semestre 10':['Optativa Desit', 'Proyecto I+DI'],
}

Informes ={
    'General': ['Porcentaje de activos','Porcentaje dados de baja', 'Porcentaje de completados'],
    'Informe activos':['Semestre 1', 'Semestre 2', 'Semestre 3', 'Semestre 4', 'Semestre 5', 'Semestre 6', 'Semestre 7', 'Semestre 8', 'Semestre 9', 'Semestre 10']
}

semestres_TIC = {
    'General': ['Otoño 2018', 'Primavera 2019', 'Verano 2019', 'Otoño 2019', 'Primavera 2020', 'Otoño 2020', 'Primavera 2021', 'Verano 2021', 'Otoño 2021', 'Primavera 2022', 'Verano 2022', 'Otoño 2022', 'Primavera 2023', 'Verano 2023'],
    'Semestre 1': ['Introduccion a las matemáticas','Introduccion a la programamcion','Teoria Gral. De sistemas y sistemas de informacion','formacion humana y social','Lengua extranjera I'],
    'Semestre 2': ['Calculo diferencial e Integral', 'Algebra Lineal con Aplicaciones', 'Programacion orientada a objetos', 'Modelado de procesos de negocio',  'DHPC', 'Lengua extranjera II'],
    'Semestre 3': ['Probabilidad y Estadistica', 'Matemáticas Discretas', 'Programacion orientada a objetos II', 'Herramientas web', 'Lengua extranjera III'],
    'Semestre 4': ['Redes de computadoras', 'Metodos estadisticos','Ingenieria de Software I','Diseño de base de datos','Lengua Extranjera IV'],
    'Semestre 5': ['Redes y Servicios','Fundamentos de la programacion logica','Ingenieria de Software II','Administracion de base de datos','Administracion de sistemas operativos'],
    'Semestre 6': ['Administracion de red','Administracion de proyectos','Diseño de la interaccion','Mineria de datos','Computo Distribuido','Tecnologias web'],
    'Semestre 7': ['Control de calidad y  SW','Inteligencia de negocios','Modelos de desarrollo web','Optativa I','Optativa Desit'], 
    'Semestre 8': ['Servicio social','Trabajo colaborativo','Servicios web','Optativa 2','Optativa 3'],
    'Semestre 9': ['Integraccion de sistemas y arquitecturas','Practica profesional','Programacion de Disp. Moviles','Proyecto I + D1' ], 
}

Informes_TIC ={
    'General': ['Porcentaje de activos','Porcentaje dados de baja', 'Porcentaje de completados'],
    'Informe activos':['Semestre 1', 'Semestre 2', 'Semestre 3', 'Semestre 4', 'Semestre 5', 'Semestre 6', 'Semestre 7', 'Semestre 8', 'Semestre 9']
}

# Dropdown para seleccionar el semestre
dropdown_semestre = dcc.Dropdown(
    id='dropdown-semestre',
    options=[
        {'label': semestre, 'value': semestre} for semestre in semestres.keys()
    ],
    value='General',  # Semestre seleccionado por defecto
    clearable=False,
    style={'width': '50%'}
)

# Dropdown para seleccionar al alumno
dropdown_alumno = dcc.Dropdown(
    id='dropdown-alumno',
    options=[
        {'label': alumno, 'value': alumno} for alumno in df_calificaciones['Nombres']
    ],
    value='AGUIRRE CHALTEL ARMANDO',  # Alumno seleccionado por defecto
    clearable=False,
    style={'width': '50%'}
)


dropdown_informe = dcc.Dropdown(
    id='dropdown-informe',
    options=[
        {'label': informe, 'value': informe} for informe in Informes.keys()
    ],
    value='General',  # Alumno seleccionado por defecto
    clearable=False,
    style={'width': '50%'}
)

# Dropdown para seleccionar el semestre
dropdown_semestre_TIC = dcc.Dropdown(
    id='dropdown-semestre-TI',
    options=[
        {'label': semestre_TIC, 'value': semestre_TIC} for semestre_TIC in semestres_TIC.keys()
    ],
    value='General',  # Semestre seleccionado por defecto
    clearable=False,
    style={'width': '50%'}
)

# Dropdown para seleccionar al alumno
dropdown_alumno_TIC = dcc.Dropdown(
    id='dropdown-alumno-TI',
    options=[
        {'label': alumno, 'value': alumno} for alumno in df_calificaciones_TE['Nombres']
    ],
    value='AMADOR RAMIREZ FRANCISCO JAVIER',  # Alumno seleccionado por defecto
    clearable=False,
    style={'width': '50%'}
)

dropdown_informe_TIC = dcc.Dropdown(
    id='dropdown-informe-TE',
    options=[
        {'label': informe, 'value': informe} for informe in Informes_TIC.keys()
    ],
    value='General',  # Alumno seleccionado por defecto
    clearable=False,
    style={'width': '50%'}
)


# Div donde se mostrará el gráfico
grafico_calificaciones = dcc.Graph(id='grafico-calificaciones')


grafico_calificaciones_TIC = dcc.Graph(id='grafico-calificaciones-TE')

grafico_informes = dcc.Graph(id='grafico-informe')

# Tabla con paginación para mostrar los datos en formato tabular
tabla_calificaciones = html.Div(id='tabla-calificaciones')

tabla_calificaciones_TIC = html.Div(id='tabla-calificaciones-TE')

# Div donde se mostrará el gráfico
grafico_informes_TIC = dcc.Graph(id='grafico-informe-TE')


 
#----------------------------Dashboard---------------------------------------------------------------------------------------------

data_style = {
    'backgroundColor': 'rgb(31, 32, 33)',  # Color de fondo
    'color': 'white',  # Color del texto
}

header_style = {
    'backgroundColor': 'rgb(31, 32, 33)',  # Color de fondo
    'color': 'white',  # Color del texto
}

# Definir el layout del navbar
navbar = dbc.Navbar(
    [
        dbc.NavbarBrand("Dashboard interactivo para el Tutor", href="http://127.0.0.1:8050/"),
        dbc.Button("Dashboard", id="open-offcanvas", n_clicks=0,style={'margin-left': '1000px'}),
    ],
    color='rgb(25,40,76)',
    dark=True,
    sticky="top",
)

offcanvas = html.Div(
    [
                dbc.Offcanvas(
          
            id="offcanvas",
            title="Dashboard",
            is_open=False,
             children=[
                   
                   html.Div(
                    [
                        html.Img(src="/assets/Logo_de_la_BUAP.png", className="img-fluid"),
                    ],
                ),
                dbc.NavItem(dbc.NavLink("Alumnos de ING. En Ciencias de la Computacíon", href="/page-1")),
                dbc.NavItem(dbc.NavLink("Alumnos de tecnologias de la informacion (TI)", href="/page-2"))
            ], 

            className="custom-offcanvas"
        )
    ]
)

# Definir el layout general de la aplicación
app.layout = html.Div([
    navbar,
    offcanvas,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    
])

# Definir el contenido de las diferentes páginas
page_1_layout = html.Div([
  
html.Div([
            
  dbc.Card(
    [  # Envuelve todo el contenido de la tarjeta en una lista

        dbc.CardHeader([   
            html.H6("No. De alumnos",
                style={
                    'textAlign': 'center',
                    'color': 'white',
                   
                 }
            ),
        ], style={'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardBody([
            html.P(f"{df_totales['No. De alumnos'].iloc[0]}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 40}
            ),
        ], style={'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardFooter([
            html.P("En total son 46 alumnos",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 15,
                       }
            ),
        ],  style={'background-color': 'rgb(31, 32, 33)'}),
    ], style={'width': '20%', 'display': 'inline-block'}
),

    dbc.Card(
    [  # Envuelve todo el contenido de la tarjeta en una lista

        dbc.CardHeader([   
            html.H6("Numero de alumnos activos",
                style={
                    'textAlign': 'center',
                    'color': 'white',
                   
                 }
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardBody([
            html.P(f"{df_totales['alumnos activos'].iloc[0]}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardFooter([
            html.P("Actualmente quedan 35 alumnos",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15,
                       }
            ),
        ],  style={'background-color': 'rgb(31, 32, 33)'}),
    ], style={'width': '20%', 'display': 'inline-block'}
),


     dbc.Card(
    [  # 3

        dbc.CardHeader([   
            html.H6("Alumnos dados de baja",
                style={
                    'textAlign': 'center',
                    'color': 'white',
                   
                 }
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardBody([
            html.P(f"{df_totales['baja'].iloc[0]}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardFooter([
            html.P("11 alumnos han si dados de baja",
                   style={
                       'textAlign': 'center',
                       'color': 'red',
                       'fontSize': 15,
                       }
            ),
        ],  style={'background-color': 'rgb(31, 32, 33)'}),
    ], style={'width': '20%', 'display': 'inline-block'}
),


     dbc.Card(
    [  #4

        dbc.CardHeader([   
            html.H6("Concluidos",
                style={
                    'textAlign': 'center',
                    'color': 'white',
                   
                 }
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardBody([
            html.P(f"{df_totales['No. De completados'].iloc[0]}",
                   style={
                       'textAlign': 'center',
                       'color': 'red',
                       'fontSize': 40}
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardFooter([
            html.P("Solo 3 alumnos han concluido",
                   style={
                       'textAlign': 'center',
                       'color': 'red',
                       'fontSize': 15,
                       }
            ),
        ],  style={'background-color': 'rgb(31, 32, 33)'}),
    ], style={'width': '20%', 'display': 'inline-block'}
),
         dbc.Card(
    [  # 5

        dbc.CardHeader([   
            html.H6("Porcentaje del grupo en general",
                style={
                    'textAlign': 'center',
                    'color': 'white',
                   
                 }
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardBody([
            html.P(f"{df_totales['promedio de porcentaje'].iloc[0]}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardFooter([
            html.P("El grupo en general tiene un 37%",
                   style={
                       'textAlign': 'center',
                       'color': 'red',
                       'fontSize': 15,
                       }
            ),
        ],  style={'background-color': 'rgb(31, 32, 33)'}),
    ], style={'width': '20%', 'display': 'inline-block'}
),

], style ={'background-color': 'rgb(31, 32, 33)'}),

    html.Div([
    
      html.Div([
        html.Label('Selecciona el semestre: ', style = {'color': 'white'}),
        dropdown_semestre,
        html.Label('Selecciona el alumno: ', style = {'color': 'white'}),
        dropdown_alumno,
       ], style={'color': 'black','background-color': 'rgb(31, 32, 33)' }),
    
       grafico_calificaciones,
        html.Div([
           tabla_calificaciones

       ], style={'color': 'black','background-color': 'rgb(144, 0, 164)' }),
    
      
    ], style ={'background-color': 'rgb(31, 32, 33)', 'color': 'white'}),
    

    
    html.Div([
        html.Label('Selecciona el informe: ', style = {'color': 'white'}),
        dropdown_informe, 
        grafico_informes 

    ], style ={'background-color': 'rgb(25,40,76)'}),

 
])

page_0_layout = html.Div([
    html.Div(
         style={
        'background-image': 'url("/assets/Facultad ciencias de la computacion.png")',
        'background-size': 'cover',
        'height': '100vh',  # Ajusta esto según tus necesidades
        'display': 'flex',
        'flex-direction': 'column',
       
    },
    children=[

        html.A(
        html.Button("Dashboard", id="open-offcanvas", n_clicks=0, style={'width': '150px', 'height': '40px',  'margin-left': '250px', 'margin-top':'400px'}),
      )]
    ),

      html.Div([
        dcc.Graph(id='line-plot'),
     ]),
    
      # Segunda fila
    html.Div([
        # Texto a la izquierda (｀・ω・´)”
        html.Div([
            html.H1('¿Qué es un Dashboard?', style={'color': 'White'}),
            html.P('Un dashboard es una herramienta de gestión de la información que monitoriza, analiza y muestra de manera visual los indicadores clave de desempeño', style={'color': 'White'}),
        ], style={'padding': '20px'}),
        
        # Foto a la derecha (｀・ω・´)”
        html.Img(src='/assets/ima.png', style={'width': '100%', 'max-width': '400px'})
    ], style={'display': 'flex', 'background-color': 'rgb(25,40,76)'}),
])

page_2_layout = html.Div([
  
html.Div([
            
  dbc.Card(
    [  # Envuelve todo el contenido de la tarjeta en una lista

        dbc.CardHeader([   
            html.H6("No. De alumnos",
                style={
                    'textAlign': 'center',
                    'color': 'white',
                   
                 }
            ),
        ], style={'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardBody([
            html.P(f"{df_totales_TE['No. De alumnos'].iloc[0]}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 40}
            ),
        ], style={'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardFooter([
            html.P("En total son 44 alumnos",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 15,
                       }
            ),
        ],  style={'background-color': 'rgb(31, 32, 33)'}),

    ], style={'width': '20%', 'display': 'inline-block'}
),

    dbc.Card(
    [  # Envuelve todo el contenido de la tarjeta en una lista

        dbc.CardHeader([   
            html.H6("Numero de alumnos activos",
                style={
                    'textAlign': 'center',
                    'color': 'white',
                   
                 }
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardBody([
            html.P(f"{df_totales_TE['alumnos activos'].iloc[0]}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardFooter([
            html.P("Actualmente quedan 23 alumnos",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15,
                       }
            ),
        ],  style={'background-color': 'rgb(31, 32, 33)'}),
    ], style={'width': '20%', 'display': 'inline-block'}
),


     dbc.Card(
    [  # 3

        dbc.CardHeader([   
            html.H6("Alumnos dados de baja",
                style={
                    'textAlign': 'center',
                    'color': 'white',
                   
                 }
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardBody([
            html.P(f"{df_totales_TE['baja'].iloc[0]}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardFooter([
            html.P("13 alumnos han si dados de baja",
                   style={
                       'textAlign': 'center',
                       'color': 'red',
                       'fontSize': 15,
                       }
            ),
        ],  style={'background-color': 'rgb(31, 32, 33)'}),
    ], style={'width': '20%', 'display': 'inline-block'} 
),


     dbc.Card(
    [  #4

        dbc.CardHeader([   
            html.H6("Concluidos",
                style={
                    'textAlign': 'center',
                    'color': 'white',
                   
                 }
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardBody([
            html.P(f"{df_totales_TE['Concluidos'].iloc[0]}",
                   style={ 
                       'textAlign': 'center',
                       'color': 'red',
                       'fontSize': 40}
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardFooter([
            html.P("Solo 8 alumnos han concluido",
                   style={
                       'textAlign': 'center',
                       'color': 'red',
                       'fontSize': 15,
                       }
            ),
        ],  style={'background-color': 'rgb(31, 32, 33)'}),
    ], style={'width': '20%', 'display': 'inline-block'}
), 
         dbc.Card(
    [  # 5

        dbc.CardHeader([   
            html.H6("Porcentaje del grupo en general",
                style={
                    'textAlign': 'center',
                    'color': 'white',
                   
                 }
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardBody([
            html.P(f"{df_totales_TE['promedio de porcentaje'].iloc[0]}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
            ),
        ], style={ 'background-color': 'rgb(31, 32, 33)'}),

        dbc.CardFooter([
            html.P("El grupo en general tiene un 52%",
                   style={
                       'textAlign': 'center',
                       'color': 'red',
                       'fontSize': 15,
                       }
            ),
        ],  style={'background-color': 'rgb(31, 32, 33)'}),
    ], style={'width': '20%', 'display': 'inline-block'}
),

], style ={'background-color': 'rgb(31, 32, 33)'}),

 html.Div([
    
      html.Div([
        html.Label('Selecciona el semestre: ',  style = {'color': 'white'}),
        dropdown_semestre_TIC,
        html.Label('Selecciona el alumno: ',  style = {'color': 'white'}),
       dropdown_alumno_TIC,
       ], style={'color': 'black','background-color': 'rgb(31, 32, 33)'}),
    
       grafico_calificaciones_TIC,
       html.Div([
           tabla_calificaciones_TIC

       ]),
    
      
    ] ),

     
    html.Div([
        html.Label('Selecciona el informe: ', style={'color':'white'}),
        dropdown_informe_TIC, 
        grafico_informes_TIC 

    ], style ={'background-color': 'rgb(25,40,76)'}),


])

#------------------------App------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
     dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)  
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return page_0_layout


# Función para obtener el DataFrame con las calificaciones de un semestre específico
def obtener_datos_por_semestre(semestre):
    columnas = ['Nombres'] + semestres[semestre]
    return df_calificaciones[columnas]

def obtener_datos_generales():
    columnas2 = ['Nombres'] + ['Promedio final']+['Estatus']+['Creditos']+['Materias reprobadas']
    return df_calificaciones[columnas2]

# Callback para actualizar el gráfico, la tabla y el texto al seleccionar un semestre o alumno en los Dropdowns
@app.callback(
    [dash.dependencies.Output('grafico-calificaciones', 'figure'),
     dash.dependencies.Output('tabla-calificaciones', 'children')],
    [dash.dependencies.Input('dropdown-semestre', 'value'),
     dash.dependencies.Input('dropdown-alumno', 'value')]
)
def actualizar_visualizacion(semestre, alumno):
    # Obtener los datos del semestre seleccionado
    datos_semestre = obtener_datos_por_semestre(semestre)
    datos_generales = obtener_datos_generales()
    # Obtener las calificaciones del alumno seleccionado
    calificaciones_alumno = datos_semestre[datos_semestre['Nombres'] == alumno]
    calificaciones_generales = datos_generales[datos_generales['Nombres'] == alumno]
    # Tamaño total deseado de la gráfica
    # Crear un gráfico de barras con Plotly Express
    fig = px.bar(x=calificaciones_alumno.columns[1:], y=calificaciones_alumno.values[0][1:],
                 labels={'x': 'Materia', 'y': 'Calificación'},
                 title=f'Calificaciones de {alumno} en el {semestre}',
                 )


# Cambiar el color de fondo del gráfico
    fig.update_layout(
          plot_bgcolor='rgb(31, 32, 33)',
          paper_bgcolor='rgb(31, 32, 33)',
           font=dict(color='white') 
    )
    # Tabla con paginación para mostrar los datos en formato tabular
    table = dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in calificaciones_generales ],
        data=calificaciones_generales.to_dict('records'),
        page_size=10,
        style_data=data_style,  # Aplica el estilo a los datos
        style_header=header_style  
    )

    return fig, table
    

    
#----
def obtener_datos_por_columna(informe):
    columna = Informes[informe]
    return df_pie[columna]

# Callback para actualizar el gráfico y la tabla al seleccionar un semestre en el Dropdown
# Callback para actualizar el gráfico y la tabla al seleccionar un informe en el Dropdown
@app.callback(
    dash.dependencies.Output('grafico-informe', 'figure'),
    [dash.dependencies.Input('dropdown-informe', 'value')]
)
def actualizar_grafico_informe(informe):
    # Obtener los datos del informe seleccionado
    datos_informe = obtener_datos_por_columna(informe)
    
    # Tomar la única fila de datos
    fila_informe = datos_informe.iloc[0]  # Ignora la primera columna que no es el nombre
    
    # Crear un gráfico de pastel con Plotly
    fig = go.Figure(data=[go.Pie(labels=fila_informe.index, values=fila_informe.values)])

    # Configurar el diseño del gráfico de pastel
    fig.update_traces(hoverinfo='label', textinfo='percent', textfont_size=12,
                      marker=dict(line=dict(color='white', width=2)))

    fig.update_layout(
        title=f'Calificaciones en el {informe}',
        plot_bgcolor='rgb(25,40,76)',
        paper_bgcolor='rgb(25,40,76)',
        font=dict(color='white')
    )

    return fig


# Función para obtener el DataFrame con las calificaciones de un semestre específico
def obtener_datos_por_semestre_TI(semestre_TI):
    columnas = ['Nombres'] + semestres_TIC[semestre_TI]
    return df_calificaciones_TE[columnas]

def obtener_datos_generales_TI():
    columnas2 = ['Nombres'] + ['Promedio final']+['Estatus']+['Creditos']+['Materia reprobadas']
    return df_calificaciones_TE[columnas2]

# Callback para actualizar el gráfico, la tabla y el texto al seleccionar un semestre o alumno en los Dropdowns
@app.callback(
    [dash.dependencies.Output('grafico-calificaciones-TE', 'figure'),
     dash.dependencies.Output('tabla-calificaciones-TE', 'children')],
    [dash.dependencies.Input('dropdown-semestre-TI', 'value'),
     dash.dependencies.Input('dropdown-alumno-TI', 'value')]
)
def actualizar_visualizacion_TI(semestre_TI, alumno_TI ):
    datos_semestre_TIC = obtener_datos_por_semestre_TI(semestre_TI)
    datos_generales_TIC = obtener_datos_generales_TI()
    # Obtener las calificaciones del alumno seleccionado
    calificaciones_alumno_TIC = datos_semestre_TIC[datos_semestre_TIC['Nombres'] == alumno_TI]
    calificaciones_generales_TIC = datos_generales_TIC[datos_generales_TIC['Nombres'] == alumno_TI]
    # Tamaño total deseado de la gráfica
    fig = px.bar(x=calificaciones_alumno_TIC.columns[1:], y=calificaciones_alumno_TIC.values[0][1:],
                 labels={'x': 'Materia', 'y': 'Calificación'},
                 title=f'Calificaciones de {alumno_TI} en el {semestre_TI}',
                 )


# Cambiar el color de fondo del gráfico
    fig.update_layout(
          plot_bgcolor='rgb(31, 32, 33)',
          paper_bgcolor='rgb(31, 32, 33)',
           font=dict(color='white') 
    )
    # Tabla con paginación para mostrar los datos en formato tabular
    table = dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in calificaciones_generales_TIC ],
        data=calificaciones_generales_TIC.to_dict('records'),
        page_size=10,
        style_data=data_style,  # Aplica el estilo a los datos
        style_header=header_style  # Aplica el estilo a las cabeceras
    )

    return fig, table


def obtener_datos_por_columna_TIC(informe):
    columna = Informes_TIC[informe]
    return df_pie_TE[columna]

# Callback para actualizar el gráfico y la tabla al seleccionar un informe en el Dropdown
@app.callback(
    dash.dependencies.Output('grafico-informe-TE', 'figure'),
    [dash.dependencies.Input('dropdown-informe-TE', 'value')]
)
def actualizar_grafico_informe(informe_TIC):
    # Obtener los datos del informe seleccionado
    datos_informe_TIC = obtener_datos_por_columna_TIC(informe_TIC)
    
    # Tomar la única fila de datos
    fila_informe_TIC = datos_informe_TIC.iloc[0]  # Ignora la primera columna que no es el nombre
    
    # Crear un gráfico de pastel con Plotly
    fig = go.Figure(data=[go.Pie(labels=fila_informe_TIC.index, values=fila_informe_TIC.values)])

    # Configurar el diseño del gráfico de pastel
    fig.update_traces(hoverinfo='label', textinfo='percent', textfont_size=12,
                      marker=dict(line=dict(color='white', width=2)))

    fig.update_layout(
        title=f'Calificaciones en el {informe_TIC}',
        plot_bgcolor='rgb(25,40,76)',
        paper_bgcolor='rgb(25,40,76)',
        font=dict(color='white')
    )

    return fig


@app.callback(
  dash.dependencies.Output("offcanvas", "is_open"),
  dash.dependencies.Input("open-offcanvas", "n_clicks"),
  [dash.dependencies.State("offcanvas", "is_open")],
)

def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(
    dash.dependencies.Output('line-plot', 'figure'),
    [dash.dependencies.Input('line-plot', 'relayoutData')]
)
def update_graph(relayout_data):
    df_sorted = combined_df .sort_values(by='porcentajes')
    fig = px.line(df_sorted,x = 'Nombres', y='porcentajes', color='Tipo',markers=True,
                  labels={'porcentajes': 'porcentajes', 'Nombres': 'Nombre del Alumno'},
                  title='Gráfica de Porcentajes para Ingeniería y Licenciatura',
                  category_orders={'Nombre': category_order} )
    
    fig.update_layout(
        xaxis={'tickvals': []},
        plot_bgcolor='rgb(31, 32, 33)',
        paper_bgcolor='rgb(31, 32, 33)',
        font=dict(color='white') 
        )


    return fig

# Ejecutar la aplicación de Dash
if __name__ == '__main__':
    app.run_server(debug=True)
