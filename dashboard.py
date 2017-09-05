import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import datetime
import plotly
from consumer import TweetConsumer

app = dash.Dash(__name__)
consumer = TweetConsumer()

app.layout = html.Div(
    html.Div([
        html.H4('Live Tweet Monitoring'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*3000 # in milliseconds
        )
    ])
)

@app.callback(Output('live-update-text', 'children'),
              events=[Event('interval-component', 'interval')])
def update_tweet():
    tweets = consumer.get_tweets(1)
    print tweets
    single_tweet = tweets[0] if len(tweets)>0 else ""
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span(single_tweet['text'], style=style),
    ]

if __name__ == '__main__':
    app.run_server(debug=True)
