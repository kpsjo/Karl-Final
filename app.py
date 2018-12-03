
# coding: utf-8

# In[ ]:


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

df.head()

available_indicators = df['NA_ITEM'].unique()
available_units = df['UNIT'].unique()
available_countries = df['GEO'].unique()

# scatterplot starts here
app.layout = html.Div([
    html.H2('Figure 1: Scatterplot', style={'textAlign': 'center'}),
    html.Div([

        html.Div([
            html.Label('Select Indicator 1'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Acquisitions less disposals of valuables'
            ),

            dcc.RadioItems(
        id='unit-selection',
        options=[{'label': i, 'value': i} for i in available_units],
        value='Current prices, million euro',
        labelStyle={'display': 'block'})
        ],
        style={'width': '45%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label('Select Indicator 2'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Actual individual consumption')
        ],
        style={'width': '45%', 'display': 'inline-block', 'float': 'right'})
    ]),
    
    
    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='TIME--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
    
    # Line Chart starts here
    html.Div(style={'height':50, 'display': 'inline-block'}),
    html.H2('Figure 2: Line Chart', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Label('Select Country'),
            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Norway'
            ),

            dcc.RadioItems(
        id='unit-selection2',
        options=[{'label': i, 'value': i} for i in available_units],
        value='Current prices, million euro',
        labelStyle={'display': 'block'})
        ],
        style={'width': '45%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label('Select Indicator'),
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices')
        ],
        style={'width': '45%', 'display': 'inline-block', 'float': 'right'})
    ]),

    dcc.Graph(id='country-graphic')])



@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('unit-selection', 'value'),
     dash.dependencies.Input('TIME--slider', 'value')])

def update_scatter(xaxis_column_name, yaxis_column_name,
                 unit_selection, TIME_value):
    df2 = df[df['TIME'] == TIME_value]
    df3 = df2[df2['UNIT'] == unit_selection]
    
    return {
        'data': [go.Scatter(
            x=df3[df3['NA_ITEM'] == xaxis_column_name]['Value'],
            y=df3[df3['NA_ITEM'] == yaxis_column_name]['Value'],
            text=df3[df3['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )]
    }

@app.callback(
    dash.dependencies.Output('country-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value'),
     dash.dependencies.Input('unit-selection2', 'value')])

def update_linechart(xaxis_column_name2, yaxis_column_name2, unit_selection2):
    df2 = df[df['GEO'] == xaxis_column_name2]
    df3 = df2[df2['UNIT'] == unit_selection2]
    
    return {
        'data': [go.Scatter(
            y=df3[df3['NA_ITEM'] == yaxis_column_name2]['Value'],
            x=df3['TIME'].unique(),
        )],
        'layout': go.Layout(
            xaxis={
                'title': "years"},
            yaxis={
                'title': yaxis_column_name2},
            margin={'l': 90, 'b': 15, 't': 65, 'r': 90},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()

