# Pacotes 
import dash 
import folium 
import pymysql
import dash_core_components as dcc 
import dash_html_components as html 
import dash_bootstrap_components as dbc
import pandas as pd 
import numpy as np 
import scipy.stats as sc
import plotly.express as px 
import plotly.graph_objects as go 
from dash.dependencies import Input, Output
import json 


# Importando os dados  
# Estrutura de conexão do banco de dados 
host = 'localhost'
user = 'root'
passwd = "34340012"
db = "Data_saude"
port= 3306
db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
db_cur = db_conn.cursor()

# Criando o dataframe
# Select municipio,Receitas_apuração_sps.codigo_municipio,estado,Receitas_apuração_sps.ano,campo,Receitas_realizadas_Bimestre, populacao.populacao_estimada as população, Produto_interno_bruto.Produto_interno_bruto  FROM Receitas_apuração_sps  LEFT JOIN populacao ON populacao.Codigo = Receitas_apuração_sps.codigo_Municipio AND populacao.Ano=Receitas_apuração_sps.Ano LEFT JOIN Produto_interno_bruto ON Produto_interno_bruto.Codigo_municipio = Receitas_apuração_sps.codigo_Municipio AND Produto_interno_bruto.Ano =Receitas_apuração_sps.Ano;
# Select municipio,Receitas_adicionais_financiamento.codigo_municipio,estado,Receitas_adicionais_financiamento.ano,campo,Receitas_realizadas_Bimestre, populacao.populacao_estimada as população, Produto_interno_bruto.Produto_interno_bruto  FROM Receitas_adicionais_financiamento  LEFT JOIN populacao ON populacao.Codigo = Receitas_adicionais_financiamento.codigo_Municipio AND populacao.Ano=Receitas_adicionais_financiamento.Ano LEFT JOIN Produto_interno_bruto ON Produto_interno_bruto.Codigo_municipio = Receitas_adicionais_financiamento.codigo_Municipio AND Produto_interno_bruto.Ano =Receitas_adicionais_financiamento.Ano;
# Select municipio,Despesas_saúde_subfunção.codigo_municipio,estado,Despesas_saúde_subfunção.ano,campo,despesas_executadas_liquidadas, populacao.populacao_estimada as população, Produto_interno_bruto.Produto_interno_bruto  FROM Despesas_saúde_subfunção  LEFT JOIN populacao ON populacao.Codigo = Despesas_saúde_subfunção.codigo_Municipio AND populacao.Ano=Despesas_saúde_subfunção.Ano LEFT JOIN Produto_interno_bruto ON Produto_interno_bruto.Codigo_municipio = Despesas_saúde_subfunção.codigo_Municipio AND Produto_interno_bruto.Ano =Despesas_saúde_subfunção.Ano;
# Select municipio,Despesas_saúde_não_computadas.codigo_municipio,estado,Despesas_saúde_não_computadas.ano,campo,despesas_executadas_liquidadas, populacao.populacao_estimada as população, Produto_interno_bruto.Produto_interno_bruto  FROM Despesas_saúde_não_computadas  LEFT JOIN populacao ON populacao.Codigo = Despesas_saúde_não_computadas.codigo_Municipio AND populacao.Ano=Despesas_saúde_não_computadas.Ano LEFT JOIN Produto_interno_bruto ON Produto_interno_bruto.Codigo_municipio = Despesas_saúde_não_computadas.codigo_Municipio AND Produto_interno_bruto.Ano =Despesas_saúde_não_computadas.Ano;
# Select municipio,Despesas_saude_natureza.codigo_municipio,estado,Despesas_saude_natureza.ano,campo,despesas_executadas_liquidadas, populacao.populacao_estimada as população, Produto_interno_bruto.Produto_interno_bruto  FROM Despesas_saude_natureza  LEFT JOIN populacao ON populacao.Codigo = Despesas_saude_natureza.codigo_Municipio AND populacao.Ano=Despesas_saude_natureza.Ano LEFT JOIN Produto_interno_bruto ON Produto_interno_bruto.Codigo_municipio = Despesas_saude_natureza.codigo_Municipio AND Produto_interno_bruto.Ano =Despesas_saude_natureza.Ano;

Raf = pd.read_csv("Receitas_apuração_sps.csv")
Raa = pd.read_csv("Receitas_adicionais_financiamento.csv")
Dss = pd.read_csv("Despesas_saúde_não_computadas.csv")
Dsn = pd.read_csv("Despesas_saude_natureza.csv")
Dsc = pd.read_csv("Despesas_saúde_subfunção.csv")

# Importando as latitudes e longitudes dos municipios 
cities = open('CE.json')
cities = json.load(cities)

# Tabela 
Tabela=[{'label':'Despesas com saúde - grupo de natureza','value':'Despesas com saúde - grupo de natureza'},
{'label':'Despesas com saúde - subfunção ','value':'Despesas com saúde - subfunção '},
{'label':'Despesas com saúde não computadas','value':'Despesas com saúde não computadas'},
{'label':'Receitas para apuração da aplicação em ações ','value':'Receitas para apuração da aplicação em ações '},
{'label':'Receitas_adicionais_financiamento','value':'Receitas_adicionais_financiamento'}]

# Menu - Rubrica
# Dsn
Rubrica_Dsn =[]
for i in np.unique(Dsn['campo'].to_list()):
    Rubrica_Dsn.append({"label":i,"value":i})

# Dss 
Rubrica_Dss =[]
for i in np.unique(Dss['campo'].to_list()):
    Rubrica_Dss.append({"label":i,"value":i})

# Dsc 
Rubrica_Dsc =[]
for i in np.unique(Dsc['campo'].to_list()):
    Rubrica_Dsc.append({"label":i,"value":i})

# Raf 
Rubrica_Raf =[]
for i in np.unique(Raf['campo'].to_list()):
    Rubrica_Raf.append({"label":i,"value":i})

# Raa 
Rubrica_Raa =[]
for i in np.unique(Raa['campo'].to_list()):
    Rubrica_Raa.append({"label":i,"value":i})

# Ano
Ano=[]
for i in range(2013,2020):
   Ano.append({'label':i,"value":i}) 



# Ano 
Ano=[]
for i in range(2013,2020):
   Ano.append({'label':i,"value":i}) 

# Tipo de Dados
Tipo =[{'label':'Padrão','value':'Padrão'},{'label':'População','value':'População'},{'label':'Produto interno bruto','value':'Produto interno bruto'}]

# Criando o Dash
app = dash.Dash(__name__)
server = app.server
# Titulo
Titulo = html.Div(
    html.H1(
        " Sistema de Informações sobre Orçamentos Públicos em Saúde - (SIOPS)"
        )
)

# Subtitulo 
Subtitulo = html.Div(
    [
    html.Div([
    html.H2("O que é o Siops?"),
    html.P("O SIOPS é o sistema informatizado, de alimentação obrigatória e acesso público, operacionalizado pelo Ministério da Saúde, instituído para coleta, recuperação, processamento, armazenamento, organização, e disponibilização de informações referentes às receitas totais e às despesas com saúde dos orçamentos públicos em saúde. O sistema possibilita o acompanhamento e monitoramento da aplicação de recursos em saúde, no âmbito da União, Estados, Distrito Federal e Municípios, sem prejuízo das atribuições próprias dos Poderes Legislativos e dos Tribunais de Contas."),
    ]),
    html.Div([
    html.H2("Objetivo do Siops?"),
    html.P("Para garantir tanto o acesso da população como o financiamento do SUS foi criado Sistema de Informações sobre Orçamentos Públicos em Saúde (SIOPS), que constitui instrumento para o acompanhamento do cumprimento do dispositivo constitucional que determina, em orçamento, a aplicação mínima de recursos em ações e serviços públicos de saúde (ASPS).")
    ]),
    html.Div([
    html.H2("Quem utiliza o Siops?"),
    html.P("gestores da União, estados e municípios declaram todos os anos os dados sobre gastos públicos em saúde. São essas declarações que garantem as transferências constitucionais de recursos para a oferta de ASPS.")
    ])
    ]
)

# Menu
Menu = (dbc.Row([
    dbc.Col(
        dbc.Card(
            [
                dbc.FormGroup(
                    [
                    html.Label("Tabela"),
                    html.Br(),
                    dcc.Dropdown(
                        id="Tabela",
                        options = Tabela,
                        value = "Tabela"
                    )
                    ]
                )
            ]
        )
    ),  
    dbc.Col(
        dbc.Card(
            [
                dbc.FormGroup(
                    [
                    html.Label("Campos"),
                    html.Br(),
                    dcc.Dropdown(
                        id="campo",
                    )
                    ]
                )
            ]
        )
    ),
    dbc.Col(
      dbc.Card(
          [
              dbc.FormGroup(
                  [
                    html.Label("Ano"),
                    html.Br(),
                    dcc.Dropdown(
                        id="Ano",
                        options = Ano,
                        value="Ano"
                    )
                  ]
              )
          ]
      )  
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.FormGroup(
                    [
                        html.Label("Rubrica"),
                        dcc.Dropdown(
                            id = "Tipo",
                            options = Tipo,
                            value = "Selecione um tipo",
                        )
                    ]
                )
            ]
        )
    )
]))


# Layout 
dashboard = html.Div(
    [
    html.Div([
        html.Tr(
            [
            html.Td(
                [
                dbc.Card(
                    [
                        dcc.Graph(id='Mapa')
                    ],
                        ),
                ]
            ),
            html.Td(
                [
                    dbc.Card(
                        [
                            dcc.Graph(id='Barplot')
                        ]
                    )
                ]
            )
            ]
            ),
        html.Tr(
            [
                html.Td(
                        dbc.Card(
                            [
                                dcc.Graph(id='Histogram')
                            ]
                        )
                ),
                #html.Td(
                        
                            
                #                dash_table.DataTable(
                #                    id='Dataframe',
                #                    data = df.to_dict('records'),
                #                    columns=[{"name": i, "id": i} for i in df.columns])
       
                #),

            ]
                                
    ),
    ]
    )
    ]
)
app.layout = html.Div(
    [
    html.Div(Titulo),
    html.Div(dbc.CardBody(Menu)),
    html.Div(dashboard)
    ]
    
)



@app.callback(Output('campo','options'),[Input('Tabela','value')])
def campo(Tabela):
    if Tabela == 'Despesas com saúde não computadas':
        test = Rubrica_Dsc
    elif Tabela == 'Despesas com saúde - grupo de natureza':
        test = Rubrica_Dsn 
    elif Tabela == 'Despesas com saúde - subfunção ':
        test = Rubrica_Dss 
    elif Tabela == 'Receitas_adicionais_financiamento':
        test = Rubrica_Raf
    elif Tabela == 'Receitas para apuração da aplicação em ações ':
        test = Rubrica_Raa 
    else:
        test =[]

    return test




@app.callback(Output('Mapa','figure'),[Input('Ano','value'),Input('Tabela','value'),Input('campo','value'),Input('Tipo','value'),])
def Mapa(Ano,Tabela,campo,Tipo):
    if Tabela == 'Despesas com saúde - grupo de natureza':
        dados = Dsn
        ano = dados[dados['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']
        fig = px.choropleth(
            rubrica,
            geojson=cities,
            locations='codigo_municipio',
            color='Choropleth',
            center={"lat":-3.71839,"lon":-38.5434},
            featureidkey='properties.GEOCODIGO')
        fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
    elif Tabela == 'Despesas com saúde - subfunção ':
        dados = Dss
        ano = dados[dados['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']
        fig = px.choropleth(
            rubrica,
            geojson=cities,
            locations='codigo_municipio',
            color='Choropleth',
            center={"lat":-3.71839,"lon":-38.5434},
            featureidkey='properties.GEOCODIGO')
        fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
    elif Tabela == 'Despesas com saúde não computadas':
        dados = Dsc
        ano = dados[dados['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']
        fig = px.choropleth(
            rubrica,
            geojson=cities,
            locations='codigo_municipio',
            color='Choropleth',
            center={"lat":-3.71839,"lon":-38.5434},
            featureidkey='properties.GEOCODIGO')
        fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
    elif Tabela == 'Receitas para apuração da aplicação em ações ':
        dados = Raa
        ano = dados[dados['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']
        fig = px.choropleth(
            rubrica,
            geojson=cities,
            locations='codigo_municipio',
            color='Choropleth',
            center={"lat":-3.71839,"lon":-38.5434},
            featureidkey='properties.GEOCODIGO')
        fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 


    elif Tabela == 'Receitas_adicionais_financiamento':
        dados = Raf
        ano = dados[dados['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']
        fig = px.choropleth(
            rubrica,
            geojson=cities,
            locations='codigo_municipio',
            color='Choropleth',
            center={"lat":-3.71839,"lon":-38.5434},
            featureidkey='properties.GEOCODIGO')
        fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 

    return fig

@app.callback(Output('Barplot','figure'),[Input('Ano','value'),Input('Tabela','value'),Input('campo','value'),Input('Tipo','value')])
def Barplot(Ano,Tabela,campo,Tipo):
    global fig
    if Tabela == 'Despesas com saúde - grupo de natureza':
        dados = Dsn 
        data = dados
        ano = data[data['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
          rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']
        fig = px.bar(rubrica,x='municipio',y='Choropleth')

    elif Tabela == 'Despesas com saúde - subfunção ':
        dados = Dss 
        data = dados 
        ano = data[data['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']
        
        fig = px.bar(rubrica,x='municipio',y='Choropleth')

    elif Tabela == 'Despesas com saúde não computadas':
        dados = Dsc 
        data = dados 
        ano = data[data['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']
        
        fig = px.bar(rubrica,x='municipio',y='Choropleth')
    elif Tabela == 'Receitas para apuração da aplicação em ações ':
        dados = Raa 
        data = dados 
        ano = data[data['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']
        
        fig = px.bar(rubrica,x='municipio',y='Choropleth')

    elif Tabela == 'Receitas_adicionais_financiamento' :
        dados = Raf 
        data = dados 
        ano = data[data['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']
        
        fig = px.bar(rubrica,x='municipio',y='Choropleth')
    return fig

@app.callback(Output("Histogram",'figure'),[Input('Ano','value'),Input('Tabela','value'),Input('campo','value'),Input('Tipo','value')])
def Histogram(Ano,Tabela,campo,Tipo):
    if Tabela == 'Despesas com saúde - grupo de natureza':
        dados = Dsn 
        data =dados 
        ano = data[data['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']

        fig = px.histogram(rubrica,x='Choropleth')

    elif Tabela == 'Despesas com saúde - subfunção ':
        dados = Dss 
        data =dados 
        ano = data[data['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']

        fig = px.histogram(rubrica,x='Choropleth')
    elif Tabela == 'Despesas com saúde não computadas':
        dados = Dsc
        data =dados 
        ano = data[data['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['despesas_executadas_liquidadas']

        fig = px.histogram(rubrica,x='Choropleth')

    elif Tabela == 'Receitas para apuração da aplicação em ações ':
        dados = Raa 
        data =dados 
        ano = data[data['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']

        fig = px.histogram(rubrica,x='Choropleth')

    elif Tabela == 'Receitas_adicionais_financiamento' :
        dados = Raf 
        data =dados 
        ano = data[data['ano']==Ano]
        rubrica = ano[ano['campo']==campo]
        if Tipo == 'População':
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['população']
        elif Tipo == 'Produto interno bruto':
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['Produto_interno_bruto']
        else:
            rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']

        fig = px.histogram(rubrica,x='Choropleth')

    return fig 


if __name__ == "__main__":
    app.run_server(debug=True)