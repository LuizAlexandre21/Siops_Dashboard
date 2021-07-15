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
import dash_table

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

dados = pd.read_csv("Receitas_apuração_sps.csv")

# Importando as latitudes e longitudes dos municipios 
cities = open('CE.json')
cities = json.load(cities)

# Ano 
Ano=[]
for i in range(2013,2020):
   Ano.append({'label':i,"value":i}) 
# Campos
Rubrica =[]
for i in np.unique(dados['campo'].to_list()):
    Rubrica.append({"label":i,"value":i})
# Tipo de Dados
Tipo =[{'label':'Padrão','value':'Padrão'},{'label':'População','value':'População'},{'label':'Produto interno bruto','value':'Produto interno bruto'}]

# Criando o Dash
app = dash.Dash(__name__)

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
                        id = 'rubrica',
                        options = Rubrica,
                        value = 'Selecione uma Rubrica'
                        ),
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

# Create elementos graficos dinamicos
@app.callback(Output('Mapa','figure'),[Input('Ano','value'),Input('rubrica','value'),Input('Tipo','value')])
def Mapa(Ano,rubrica,Tipo):
    data = dados 
    ano = data[data['ano']==Ano]
    print(ano)
    rubrica = ano[ano['campo']==rubrica]
    print(rubrica)
    if Tipo == 'População':
        rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['população']
    elif Tipo == 'Produto interno bruto':
        rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['Produto_interno_bruto']
    else:
        rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']
    print(rubrica.columns)
    print(rubrica['Choropleth'])
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

@app.callback(Output('Barplot','figure'),[Input('Ano','value'),Input('rubrica','value'),Input('Tipo','value')])
def Barplot(Ano,rubrica,Tipo):
    data = dados 
    ano = data[data['ano']==Ano]
    rubrica = ano[ano['campo']==rubrica]
    if Tipo == 'População':
        rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['população']
    elif Tipo == 'Produto interno bruto':
        rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['Produto_interno_bruto']
    else:
        rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']
    fig = px.bar(rubrica,x='municipio',y='Choropleth')
    return fig 

@app.callback(Output("Histogram",'figure'),[Input('Ano','value'),Input('rubrica','value'),Input('Tipo','value')])
def Histogram(Ano,rubrica,Tipo):
    data =dados 
    ano = data[data['ano']==Ano]
    rubrica = ano[ano['campo']==rubrica]
    if Tipo == 'População':
        rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['população']
    elif Tipo == 'Produto interno bruto':
        rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']/rubrica['Produto_interno_bruto']
    else:
        rubrica['Choropleth'] = rubrica['Receitas_realizadas_Bimestre']

    fig = px.histogram(rubrica,x='Choropleth')
    return fig 


@app.callback(Output("Dataframe",'data'),[Input('Ano','value'),Input('rubrica','value')])
def Dataframe(Ano,rubrica):
    data = dados[dados['ano']==str(Ano)]
    data = data[data['campo']==rubrica]
    df = pd.DataFrame(
        {
            "Parâmetros": ["media","variancia","desvio padrão","curtoses","assimetria"],
            "Valores":[np.mean(data['Receitas_realizadas_Bimestre']),np.var(data['Receitas_realizadas_Bimestre']),np.std(data['Receitas_realizadas_Bimestre']),sc.kurtosis(data['Receitas_realizadas_Bimestre']),sc.skew(data['Receitas_realizadas_Bimestre'])]
  
        }   
    )
    return df

if __name__ == "__main__":
    app.run_server(debug=True)