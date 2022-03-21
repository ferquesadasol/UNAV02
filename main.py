# import libraries
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
import functions as fc
import plotly.express as px
import dash_bootstrap_components as dbc
import zipfile
#prueba
# formato
color_pallet = "OrRd"

zf= zipfile.ZipFile("database.zip")

# load data
datos_ordenes = pd.read_csv(zf.open("database/items_ordered_2years.txt"), sep="|")
datos_productos = pd.read_csv(zf.open("database/products.csv"))

# limpieza de datos
datos_ordenes = fc.clean_ordenes(datos_ordenes)
histogram_ordenes = fc.histograma(datos_ordenes,datos_productos)
scatter_ordenes = fc.scatter(datos_ordenes,datos_productos)
scatter_acumulado = fc.scatter_acum(datos_ordenes)


# inicializa la aplicacion
app = dash.Dash(external_stylesheets=[dbc.themes.LUMEN])
server = app.server
#external_stylesheets = [
#    {
#        "href": "https://fonts.googleapis.com/css2?"
#                "family=Lato:wght@400;700&display=swap",
#        "rel": "stylesheet",
#    },
#]
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "CAJAMAR HACKATHON"



app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    dcc.Location(id="url",refresh=False),
    html.Div([ dbc.NavbarSimple( children=[ dbc.NavItem(dbc.NavLink("🏠" + "Home", href="/", active = "exact")),
                                            dbc.NavItem(dbc.NavLink("🛒" + "Productos", href="/productos", active = "exact")),
                                            dbc.NavItem(dbc.NavLink("📈" + "Histórico", href="/historico", active = "exact")),
                                            dbc.DropdownMenu(
                                                children=[
                                                    dbc.DropdownMenuItem("Victor Valín Gamarra", href="https://www.linkedin.com/in/victor-valin-gamarra/"),
                                                    dbc.DropdownMenuItem("Fernando Quesada Solís", href="https://www.linkedin.com/in/fernando-quesada-sol%C3%ADs-93b29b1a4/")],
                                                nav=True,
                                                in_navbar=True,
                                                label="LinkedIn")],
                                 brand = "Sales Management Report",
                                 color = "primary",
                                 dark = True,)]),
    #html.Div([
    #    dbc.Tabs(id="tabs-example", children=[
    #        dbc.Tab(label='Home', tab_id='tab-0-example',active_label_style={"color": "#FB79B3"}),
    #        dbc.Tab(label='Categorías / Productos', tab_id='tab-1-example',active_label_style={"color": "#FB79B3"}),
    #        dbc.Tab(label='Histórico de ventas', tab_id='tab-2-example',active_label_style={"color": "#FB79B3"}),
    #        dbc.Tab(label='-', tab_id='tab-3-example'),
    #        dbc.Tab(label='-', tab_id='tab-4-example'),
    #], active_tab="tab-0-example")]),
    html.Div(id='tabs-content-example')
    ])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('url', 'pathname')])
def render_content(pathname):
    if pathname == "/":
        return html.Div([
            html.Div(),
            html.Div(),
            html.H4("Resumen"),
            dbc.Card([

                dbc.CardBody(
                    [
                        html.Div(),
                        html.Div(),
                        html.P(
                            "La presente aplicación es desarrollada para la competición "
                            "Cajamar UniversityHack 2022 en el reto Atmira Pharma Visualization.",
                            className="card-text",
                        ),
                        dbc.CardLink("Link Competición", href="https://www.cajamardatalab.com/datathon-cajamar-universityhack-2022/"),
                        dbc.CardLink("Link Reto", href="https://www.cajamardatalab.com/datathon-cajamar-universityhack-2022/retos/atmira-pharma-visualization/"),
                        html.Div(),
                        html.Div(),
                    ]
                )],
            ),
            html.Div(),
            html.Div(),
            dbc.Row([
                dbc.Col(html.Div(
                    dbc.Card([
                        dbc.Row([
                            dbc.Col(
                                dbc.CardImg(
                                    src="assets/Victor.png",
                                    className="img_fluid rounded-start"
                                ),
                                className = "col-md-4"
                            ),

                            dbc.Col([
                                dbc.CardBody([
                                    html.H4("Victor Valín Gamarra", className="card-title"),
                                    html.P(
                                        "I’m a Data & Analytics Consultant focused on delivering innovative solutions to business commercial challenges through the power of data and its added value. My expertise includes data analysis and interpretation, and the development and implementation of data strategies across different industries. My colleagues would describe me as a data passionate professional keen on leveraging data to deliver actionable business insights",
                                        className="card-text"),
                                ]

                                )
                            ],
                                className="col-md-8"
                            )

                        ], className="g-0 d-flex align-items-center"

                        )
                    ], className="mb-3", style={"maxWidth": "900px"},)), width=6),



                dbc.Col(html.Div(
                    dbc.Card([
                        dbc.Row([
                            dbc.Col(
                                dbc.CardImg(
                                    src="assets/Fer.png",
                                    className="img_fluid rounded-start"
                                ),
                                className = "col-md-4"
                            ),

                            dbc.Col([
                                dbc.CardBody([
                                    html.H4("Fernando Quesada Solís", className="card-title"),
                                    html.P("I’m a industrial engineer with logistics experience in the food industry, inventory management, distribution to external and internal clients. Taking part in outsourcing processes and leading WMS implementation in different logistics operations. Aptitude for data analysis focused on decision making and knowledge of tools such as Power BI, Tableu and Excel.",
                                           className="card-text"),
                                            ]

                                            )

                                    ], className="col-md-8",

                                    )
                                ],className="g-0 d-flex align-items-center"
                                )
                            ],className="mb-3", style={"maxWidth": "900px"}
                            )
                                ), width=6
                        )
            ],
                justify="center"),
            html.Div([
                html.Img(
                    src='assets/mifarma.png',
                    style={
                        'height': '15%',
                        'width': '15%'
                    })
            ], style={'textAlign': 'center',"margin-top": "25px"})
        ])

    elif pathname == '/productos':
        fig1 = px.bar(histogram_ordenes, y=histogram_ordenes.index, x='total',
                      hover_data=['qty_ordered'], color='qty_ordered',
                      labels={'analytic_category': 'Categoría', "total": "Ventas", "qty_ordered": "Unidades vendidas"}
                      , orientation="h", color_continuous_scale=color_pallet, title="Ventas por Categoría")





        return html.Div([
            html.H4('Categorías y Productos'),
            html.Div(
                            dcc.Graph(figure=fig1),id='page-1-content', style={'textAlign': 'center',
                                                                               "margin-top": "25px",
                                                                               "margin-left":"25px",
                                                                               "margin-bottom":"25px",
                                                                               "margin-right":"25px"}),
            html.Div([
                    dbc.Select(
                        id='page-1-dropdown',
                        options=[
                            {"label": categoria, "value": categoria}
                            for categoria in np.sort(histogram_ordenes.index)],
                        value = "Cosmética y Belleza")], style={'textAlign': 'center',
                                                                               "margin-top": "25px",
                                                                               "margin-left":"25px",
                                                                               "margin-right":"25px"}),
            html.Div([
                    dbc.Select(
                        id='page-1-dropdown2',
                        options=[{"label": producto, "value": producto} for producto in np.sort(scatter_ordenes.name.unique())],
                        value = "Velastisa Intim Hidrogel Intimo 30 gramos")], style={'textAlign': 'center',
                                                                               "margin-left":"25px",
                                                                               "margin-bottom":"25px",
                                                                               "margin-right":"25px"} ),
            html.Div(
                    [dcc.Graph( id='page-1-content2')
                     ], style={'textAlign': 'center',
                                "margin-top": "25px",
                                "margin-left":"25px",
                                "margin-bottom":"25px",
                                "margin-right":"25px"})
            ])
    elif pathname == '/historico':

        fig = px.bar(x =scatter_acumulado.index, y=scatter_acumulado["total"],color=scatter_acumulado["total"],
                     color_continuous_scale = color_pallet,
                     labels={"color":"Ventas totales","x" : "Meses","y":"Ventas totales"})
        fig.add_scatter(x=scatter_acumulado.index,y=scatter_acumulado["total"],mode='lines',showlegend=False)


        return html.Div([
            html.H4('Histórico'),
            html.Div(dcc.Graph(figure = fig, id='page-2-content'),style={'textAlign': 'center',
                                                                   "margin-top": "25px",
                                                                   "margin-left":"25px",
                                                                   "margin-bottom":"25px",
                                                                   "margin-right":"25px"})])


@app.callback([dash.dependencies.Output('page-1-dropdown2', 'options'),
               dash.dependencies.Output('page-1-dropdown2', 'value')],
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def update_dropdown(value):
    return [[ {'label': i, 'value': i} for i in np.sort(scatter_ordenes[scatter_ordenes["analytic_category"]==value].name.unique())],"Velastisa Intim Hidrogel Intimo 30 gramos"]


@app.callback([dash.dependencies.Output('page-1-content2','figure')],
              [dash.dependencies.Input('page-1-dropdown2', 'value')])
               #dash.dependencies.Input('rango-fecha', 'start_date'),
               #dash.dependencies.Input('rango-fecha', 'end_date')

def update_graph(value):
    filterdata = scatter_ordenes[(scatter_ordenes["name"] == value)]
    filterdata2 = filterdata.groupby("created_at").sum()
    fig = px.line(filterdata2, x=filterdata2.index, y="total", color_discrete_map={"total": "#456987"},
                  labels={"created_at":"Fecha","total":"Ventas"},title="Ventas por Producto")
    return [fig]






# Tab 2 callback
#@app.callback(Output('page-2-content', 'children'),
 #             [Input('page-2-radios', 'value')])
#def page_2_radios(value):
 #   return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)