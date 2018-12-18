
# coding: utf-8

# In[53]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('nama_10_gdp_1_Data.csv')
df = df[['TIME', 'GEO', 'NA_ITEM', 'Value', 'UNIT']]
df = df[~df.GEO.str.contains('Euro')]
df = df[df.Value != ':']

available_indicators = df['NA_ITEM'].unique()
available_units = df['UNIT'].unique()
available_countries = df['GEO'].unique()

app.layout = html.Div([
    html.H1(children='Economic Indicators in European Countries', 
            style={'textAlign': 'center', 'color': 'rgb(37, 131, 124)'}),
    html.Div([
        
    html.H2(children='Interactive Graph 1: Scatterplot with all European countries', 
               style={'color': 'rgb(37, 131, 124)', 'width': '45%', 'float': 'left', 'display': 'inline-block', 'textAlign': 'center', 'padding-top':10}),
    html.H2(children='Interactive Graph 2: Line Chart with specific country',
                style={'color': 'rgb(37, 131, 124)', 'width':'45%', 'display': 'inline-block','textAlign': 'center', 'padding-top':10}),
    ]),
    
    html.Div([

        html.Div([
            html.Label('Select indicator (x-axis):'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Wages and salaries' 
            )
        ],
        style={'width': '24%', 'display': 'inline-block', 'padding-top':10, 'padding-bottom':20, 'padding-right':15}),

        html.Div([
            html.Label('Select indicator (y-axis):'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '24%', 'float': 'left', 'display': 'inline-block', 'padding-top':10, 'padding-bottom':20}),
        
        html.Div([
            html.Label('Select indicator: '),
            dcc.Dropdown(
                id='yaxis',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '48%', 'display': 'inline-block', 'padding-top':10, 'padding-bottom':20})
    ]),
    html.Div([
        
        html.Div([
            html.Label('Select unit:', 
                       style={'width':'48%','display':'block'}),
            dcc.Dropdown(
                id='unit_selection',
                options=[{'label': i, 'value': i} for i in available_units],
                value='Current prices, million euro'
            )
        ],
            style={'width': '48%','float':'left','display': 'inline-block', 'padding-top':10, 'padding-bottom':20, 'padding-right':15}),
    
        html.Div([
            html.Label('Select unit:', 
                       style={'width':'100%','display':'inline-block'}),
            dcc.Dropdown(
                id='unit_selection2',
                options=[{'label': i, 'value': i} for i in available_units],
                value='Current prices, million euro'
            )
        ],
        style={'width': '48%', 'display': 'inline-block', 'padding-top':10, 'padding-bottom':20})
    
    ]), 
    
    html.Div([
        dcc.Graph(
            id='indicator-graphic',
            hoverData={'points': [{'customdata': 'Belgium'}]}
        )
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='country-graphic'),
    ], style={'display': 'inline-block', 'width': '48%'}),

    html.Div(dcc.Slider(
        id='TIME--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        marks={str(TIME): str(TIME) for TIME in df['TIME'].unique()}
    ), style={'width': '46%', 'padding': '0px 20px 20px 20px'})
])

    
@app.callback(dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
      dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('unit_selection', 'value'),
     dash.dependencies.Input('TIME--slider', 'value')])
    
def update_graph(xaxis_column_name, yaxis_column_name, select_unit, year_value):
    dff = df[df['TIME'] == year_value]
    dfn = dff[dff['UNIT'] == select_unit]
    return {
        'data': [go.Scatter(
            x=dfn[dfn['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dfn[dfn['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dfn[dfn['NA_ITEM'] == yaxis_column_name]['GEO'],
            customdata=dfn[dfn['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            line = dict(
                color = ('rgb(40, 142, 134)'),
                width = 3),
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'},
                
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name},
            yaxis={
                'title': yaxis_column_name},
            margin={'l': 65, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('country-graphic', 'figure'), 
     [dash.dependencies.Input('indicator-graphic', 'hoverData'),
      dash.dependencies.Input('unit_selection2', 'value'), 
      dash.dependencies.Input('yaxis', 'value')])

def update_graph2(hoverData, select_unit2, yaxis_column_name_2):
    dfi = df[df['GEO'] == hoverData['points'][0]['customdata']]
    dfk = dfi[dfi['UNIT'] == select_unit2]
    
    return {
        'data': [go.Scatter(
            y=dfk[dfk['NA_ITEM'] == yaxis_column_name_2]['Value'], 
            x=dfk['TIME'].unique(),
            line = dict(
                color = ('rgb(40, 142, 134)'),
                width = 3),
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Years'},
            yaxis={
                'title': yaxis_column_name_2},
            margin={'l': 75, 'b': 40, 't': 50, 'r': 0},
            hovermode='closest',
            title= hoverData['points'][0]['customdata']
        )
    }
    
if __name__ == '__main__':
    app.run_server(debug=False)

