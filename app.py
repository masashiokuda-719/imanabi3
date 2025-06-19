import pandas as pd
import dash
from dash import html, dcc
import plotly.graph_objs as go
import dash_auth
import os

# 外部スタイルシート（Bootstrapなど）を指定
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# データ読み込みと前処理
df = pd.read_csv("imanabitestgraph.csv", encoding="utf-8")

# AB列: 年・新規
ab = df.iloc[:, [0, 1]].dropna()
ab.columns = ["年", "新規"]

# DE列: 売上X・売上
de = df.iloc[:, [3, 4]].dropna()
de.columns = ["売上X", "売上"]

VALID_USERNAME_PASSWORD_PAIRS = {
    os.environ.get("DASH_AUTH_USERNAME"): os.environ.get("DASH_AUTH_PASSWORD")
}

# Dashアプリ作成
app = dash.Dash(__name__)
server = app.server  # サーバー変数を追加
app.title = "imanabi KPI Dash" 


auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
app.title = "グラフダッシュボード"

app.layout = html.Div([
    html.H2("新規（棒グラフ）と売上（折れ線グラフ）ダッシュボード", style={'textAlign': 'center'}),
    html.Div([
        # 左：折れ線グラフ
        html.Div([
            dcc.Graph(
                id='line-de',
                figure={
                    'data': [
                        go.Scatter(
                            x=de["売上X"],
                            y=de["売上"],
                            mode='lines+markers',
                            name='売上',
                            line=dict(color='orange')
                        )
                    ],
                    'layout': go.Layout(
                        title='売上推移（折れ線グラフ）',
                        xaxis={'title': 'X'},
                        yaxis={'title': '売上'},
                        margin={'l': 50, 'r': 10, 't': 50, 'b': 50},
                        height=400
                    )
                }
            )
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        # 右：棒グラフ
        html.Div([
            dcc.Graph(
                id='bar-ab',
                figure={
                    'data': [
                        go.Bar(
                            x=ab["年"].astype(str),
                            y=ab["新規"],
                            name='新規',
                            marker_color='skyblue'
                        )
                    ],
                    'layout': go.Layout(
                        title='年ごとの新規（棒グラフ）',
                        xaxis={'title': '年'},
                        yaxis={'title': '新規'},
                        margin={'l': 50, 'r': 10, 't': 50, 'b': 50},
                        height=400
                    )
                }
            )
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'float': 'right'}),
    ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-between'}),
    html.Div([
        html.P("左に売上（DE列折れ線グラフ）、右に新規（AB列棒グラフ）を表示しています。", style={'textAlign': 'center'})
    ])
])

if __name__ == '__main__':
    app.run(debug=True)