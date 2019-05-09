from flask import Flask,render_template,url_for,request
import dash_html_components as html
import pandas as pd
import numpy as np
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


app = Flask(__name__)

@app.route('/')
def home():

    df_display = df[['Date', 'Home_Team', 'Away_Team', 'Home_Score', 'Away_Score', 'home_win_prob', 'predicted_scoreline']]

    return df_display.to_html(header='true', table_id='pred_table')


if __name__ == '__main__':
    app.run(debug=True)
