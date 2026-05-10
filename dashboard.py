import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("C:/Users/rushabh/Desktop/threat-hunting-project/DDoS-Friday.csv")

app = dash.Dash(__name__)

# Count attacks
total = len(df)
attacks = len(df[df['Label'] == 'DDoS'])
benign = len(df[df['Label'] == 'Benign'])

# Static charts
fig1 = px.pie(df, names='Label', title='DDoS vs Benign Traffic',
              color_discrete_map={'DDoS':'red','Benign':'green'})

fig_protocol = px.histogram(df, x='Protocol', color='Label',
                    title='Protocol Usage: DDoS vs Benign',
                    color_discrete_map={'DDoS':'red','Benign':'green'},
                    barmode='group')

app.layout = html.Div(style={'backgroundColor':'#0a0a0a','minHeight':'100vh','padding':'20px','fontFamily':'Arial'}, children=[

    html.H1("🔍 Threat Hunting Dashboard", style={'color':'#00ff88','textAlign':'center'}),
    html.P("CICIDS 2017 — Friday DDoS Dataset", style={'color':'#888','textAlign':'center'}),

    # Summary boxes
    html.Div(style={'display':'flex','justifyContent':'center','gap':'20px','marginBottom':'30px'}, children=[
        html.Div(style={'backgroundColor':'#1a1a1a','border':'1px solid #333','borderRadius':'10px','padding':'20px','textAlign':'center','width':'200px'}, children=[
            html.H2(f"{total:,}", style={'color':'#00ff88','margin':'0'}),
            html.P("Total Connections", style={'color':'#888','margin':'0'})
        ]),
        html.Div(style={'backgroundColor':'#1a1a1a','border':'1px solid red','borderRadius':'10px','padding':'20px','textAlign':'center','width':'200px'}, children=[
            html.H2(f"{attacks:,}", style={'color':'red','margin':'0'}),
            html.P("DDoS Attacks Detected", style={'color':'#888','margin':'0'})
        ]),
        html.Div(style={'backgroundColor':'#1a1a1a','border':'1px solid green','borderRadius':'10px','padding':'20px','textAlign':'center','width':'200px'}, children=[
            html.H2(f"{benign:,}", style={'color':'green','margin':'0'}),
            html.P("Benign Connections", style={'color':'#888','margin':'0'})
        ]),
        html.Div(style={'backgroundColor':'#1a1a1a','border':'1px solid orange','borderRadius':'10px','padding':'20px','textAlign':'center','width':'200px'}, children=[
            html.H2(f"{round(attacks/total*100, 1)}%", style={'color':'orange','margin':'0'}),
            html.P("Attack Rate", style={'color':'#888','margin':'0'})
        ]),
    ]),

    # Filter dropdown
    html.Div(style={'marginBottom':'20px','textAlign':'center'}, children=[
        html.Label("Filter Traffic Type:", style={'color':'#00ff88','marginRight':'10px'}),
        dcc.Dropdown(
            id='traffic-filter',
            options=[
                {'label':'All Traffic','value':'All'},
                {'label':'DDoS Only','value':'DDoS'},
                {'label':'Benign Only','value':'Benign'}
            ],
            value='All',
            style={'width':'300px','display':'inline-block','color':'black'}
        )
    ]),

    # Row 1 - Pie + Protocol
    html.Div(style={'display':'flex','gap':'20px','marginBottom':'20px'}, children=[
        html.Div(dcc.Graph(figure=fig1), style={'flex':'1','backgroundColor':'#1a1a1a','borderRadius':'10px'}),
        html.Div(dcc.Graph(figure=fig_protocol), style={'flex':'2','backgroundColor':'#1a1a1a','borderRadius':'10px'}),
    ]),

    # Row 2 - Dynamic histogram
    html.Div(dcc.Graph(id='packet-hist'), style={'backgroundColor':'#1a1a1a','borderRadius':'10px','marginBottom':'20px'}),

    # Row 3 - Scatter plot
    html.Div(dcc.Graph(id='scatter-plot'), style={'backgroundColor':'#1a1a1a','borderRadius':'10px'}),

])

# Callback for dynamic charts
@app.callback(
    Output('packet-hist', 'figure'),
    Output('scatter-plot', 'figure'),
    Input('traffic-filter', 'value')
)
def update_charts(selected):
    filtered = df if selected == 'All' else df[df['Label'] == selected]

    hist = px.histogram(filtered, x='Packet Length Mean', color='Label',
                        title=f'Packet Size Distribution ({selected})',
                        color_discrete_map={'DDoS':'red','Benign':'green'},
                        barmode='overlay', nbins=50)
    hist.update_layout(paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a',
                       font_color='white')

    scatter = px.scatter(filtered.sample(min(5000, len(filtered))),
                         x='Flow Duration', y='Packet Length Mean',
                         color='Label', title=f'Flow Duration vs Packet Size ({selected})',
                         color_discrete_map={'DDoS':'red','Benign':'green'},
                         opacity=0.5)
    scatter.update_layout(paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a',
                          font_color='white')

    return hist, scatter

if __name__ == '__main__':
    app.run(debug=True)