import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from superugby import cleanup
from model import fit_predict

print('loading data from GitHub...')
raw = pd.read_csv(
    'https://raw.githubusercontent.com/kieranbd/superrugby-predictor/master/' +
    'super_rugby_oddsportal.csv').drop('Play-off Game?', axis=1).dropna()

print('cleaning data...')
df = cleanup(raw, dummies=False)

print('fitting model...')
predictions = fit_predict(raw)

df['predicted_scoreline'] = predictions


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# initialize Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#000000',
    'text': '#111111'
}

intro_text = '''
## Super Rugby Dashboard
Work in progress making a super rugby score prediction dashboard. I have been following the dash tutorials found [here](https://dash.plot.ly/)
'''

app.layout = html.Div(children=[

    dcc.Markdown(children=intro_text),

    dcc.Graph(id='margin-vs-odds'),

    # wrapping slider in Div element allows us to add the 'style' property
    html.Div([
        dcc.Slider(
            id='year-slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=df['Year'].max(),
            marks={str(year): str(year) for year in df['Year'].unique()},
            step=None
        )],
        style={'marginLeft': '3em',
               'marginRight': '3em',
               'marginBottom': '3em'}
    ),

    dcc.Markdown('#### Last 10 fixtures:'),

    generate_table(df[['Date', 'Home_Team', 'Away_Team', 'Home_Score', 'Away_Score', 'home_win_prob', 'predicted_scoreline']])
])

@app.callback(
    Output('margin-vs-odds', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.Year <= selected_year]
    traces = []
    for i in filtered_df['home_nationality'].unique():
        df_by_country = filtered_df[filtered_df['home_nationality'] == i]
        traces.append(go.Scatter(
            x=df[df['home_nationality'] == i]['home_win_prob'],
            y=df[df['home_nationality'] == i]['home_margin'],
            text=df[df['home_nationality'] == i]['home_nationality'],
            mode='markers',
            opacity=0.8,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Predicted Home Win Probability'},
            yaxis={'title': 'Observed Home Score Difference'},
            margin={'l': 75, 'b': 75, 't': 50, 'r': 20},
            legend={'x': 1, 'y': 0},
            hovermode='closest',
            title='Bookmakers\' odds vs actual scoreline'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
