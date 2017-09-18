# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import datetime
import plotly
import consumer
import analytics

app = dash.Dash(__name__)
consumer = consumer.TweetConsumer()
analytics = analytics.Analytics()

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


@app.callback(
    Output('live-update-text', 'children'),
    events=[Event('interval-component', 'interval')])
def update_tweet():
    print "trying to fetch messages"
    tweets = consumer.get_tweets(5)

    if len(tweets)>0:
        print "running sentiment analysis "
        count = analytics.run_sentiment_analysis(tweets)
        print "count: ",count

    # print single_tweet

    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span(str(count), style=style),
    ]

if __name__ == '__main__':
    app.run_server(debug=True)
