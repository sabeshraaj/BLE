# the webpage which will be created at the end of this process, will not be a native html file
# the following code uses "dash" a python library to create dashboards and webpages etc

import speech_recognition as sr
import threading
import webbrowser
import os
from gtts import gTTS
import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
from pymongo import MongoClient
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Connect to MongoDB
# these connections might change accordingly to your own mongo db instance which you run on your computer
client = MongoClient("your_local_mongodb_connection")
db = client["your_own_database"]
collection = db["your_own_collection"]

def listen_for_apollo():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("Voice listener active. Say 'Hey Apollo' to launch the dashboard...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print("Heard:", command)
                if "hey apollo" in command:
                    tts = gTTS("Launching Mezoi Dashboard", lang='en')
                    tts.save("launch.mp3")
                    os.system("start launch.mp3" if os.name == "nt" else "afplay launch.mp3" if os.name == "darwin" else "mpg123 launch.mp3")
                    webbrowser.open("http://0.0.0.0:8051")
            except sr.UnknownValueError:
                pass  # Ignore unrecognized speech
            except Exception as e:
                print("Error:", e)

# Blue color palette - following the provided color scheme
COLORS = {
    'darkest': '#003A6B',      # Dark blue for text and primary elements
    'dark': '#1B5886',        # Medium dark blue
    'medium': '#3776A1',      # Medium blue
    'light': '#5293B8',       # Light blue
    'lighter': '#6EBDD6',     # Lighter blue
    'lightest': '#89CFF1',    # Lightest blue for backgrounds
    'background': '#f8f9fa',  # Light grey background
    'card_bg': '#ffffff',     # White card background
    'text': '#003A6B',        # Dark blue for text
    'border': '#e9ecef'       # Light border color
}

# Custom CSS
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Your-app-or-dashboard-name"

# Custom styles
card_style = {
    'border-radius': '12px',
    'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
    'border': 'none',
    'margin-bottom': '20px',
    'background-color': COLORS['card_bg']
}

metric_card_style = {
    'border-radius': '8px',
    'color': 'white',
    'text-align': 'center',
    'padding': '20px 15px',
    'margin': '5px',
    'font-weight': '500',
    'cursor': 'pointer',
    'transition': 'all 0.3s ease',
    'min-height': '80px',
    'display': 'flex',
    'align-items': 'center',
    'justify-content': 'center'
}

# Layout
app.layout = dbc.Container(fluid=True, style={'backgroundColor': COLORS['background'], 'min-height': '100vh'}, children=[
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("MEZOI", className="text-center", 
                   style={'color': COLORS['darkest'], 'font-weight': '600', 'margin': '20px 0', 'font-size': '2.5rem'})
        ])
    ]),
    
    # Patient Info and Diagnosis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.I(className="fas fa-user-injured", style={'font-size': '24px', 'color': COLORS['medium']}),
                                ], style={'width': '50px', 'height': '50px', 'background': COLORS['lightest'], 
                                         'border-radius': '50%', 'display': 'flex', 'align-items': 'center', 
                                         'justify-content': 'center', 'margin-right': '15px'}),
                                html.Div([
                                    html.H5("Smart Room 101 - Mary Queen Schedule", 
                                           style={'color': COLORS['text'], 'margin': '0', 'font-weight': '600'}),
                                    html.P("PATIENT DATA", style={'color': COLORS['medium'], 'margin': '0', 'font-size': '12px'})
                                ])
                            ], style={'display': 'flex', 'align-items': 'center'})
                        ], width=6),
                        dbc.Col([
                            html.Div([
                                html.P("Diagnoses: Dengue Fever", style={'margin': '0', 'font-weight': '600', 'color': COLORS['text']}),
                                html.P("Date Of Admission: 22/02/2025", style={'margin': '0', 'color': COLORS['medium'], 'font-size': '14px'})
                            ], style={'text-align': 'center'})
                        ], width=6)
                    ])
                ])
            ], style=card_style)
        ], width=12)
    ]),
    
    # Main Content Row
    dbc.Row([
        # Patient Details Sidebar
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.Img(src='/assets/patient_photo.jpg',
                                     style={'width': '100%', 'height': '100%', 'object-fit': 'cover', 'border-radius': '50%'}),
                        ], style={'width': '100px', 'height': '100px', 'background': COLORS['lightest'],
                                 'border-radius': '50%', 'display': 'flex', 'align-items': 'center',
                                 'justify-content': 'center', 'margin': '0 auto 20px auto', 'overflow': 'hidden'}),
                        html.Hr(style={'border-color': COLORS['border']}),
                        html.Div([
                            html.P("Name: Patient 1", style={'margin': '8px 0', 'color': COLORS['text']}),
                            html.P("Blood: B+", style={'margin': '8px 0', 'color': COLORS['text']}),
                            html.P("Height: 177cm", style={'margin': '8px 0', 'color': COLORS['text']}),
                            html.P("Weight: 96kg", style={'margin': '8px 0', 'color': COLORS['text']}),
                            html.P("Join Date: 22-02-2025", style={'margin': '8px 0', 'color': COLORS['text']}),
                            html.P("Doctor: Albert", style={'margin': '8px 0', 'color': COLORS['text']}),
                            html.P("Diagnosis: Dengue Fever", style={'margin': '8px 0', 'color': COLORS['text']}),

                            # Add a gap using an empty div or a div with padding-top
                            html.Div(style={'margin-top': '180px'}), # Adjust '20px' for desired gap size

                            html.P("Email: patient1@example.com", style={'margin': '8px 0', 'color': COLORS['text']}),
                            html.P("Contact: +91 98765 43210", style={'margin': '8px 0', 'color': COLORS['text']})
                        ])
                    ], style={'text-align': 'left'})
                ])
            ], style={'height': '79.5%', **card_style})
        ], width=2, style={'height': '800px'}),
        
        # Main Dashboard
        dbc.Col([
            # Metric Cards Row
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-heartbeat", style={'font-size': '20px', 'margin-bottom': '8px'}),
                        html.Div("Pulse Pressure", style={'font-size': '14px'})
                    ], id="pulse-pressure-btn", style={**metric_card_style, 'background': COLORS['darkest']})
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-thermometer-half", style={'font-size': '20px', 'margin-bottom': '8px'}),
                        html.Div("Temperature", style={'font-size': '14px'})
                    ], id="temperature-btn", style={**metric_card_style, 'background': COLORS['darkest']})
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-lungs", style={'font-size': '20px', 'margin-bottom': '8px'}),
                        html.Div("SpO2", style={'font-size': '14px'})
                    ], id="spo2-btn", style={**metric_card_style, 'background': COLORS['darkest']})
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-wind", style={'font-size': '20px', 'margin-bottom': '8px'}),
                        html.Div("Respiratory Rate", style={'font-size': '14px'})
                    ], id="respiratory-btn", style={**metric_card_style, 'background': COLORS['darkest']})
                ], width=3)
            ], className="mb-4"),
            
            # Charts Section
            html.Div(id="charts-container")
        ], width=10)
    ]),
    
    dcc.Interval(id="interval", interval=5000, n_intervals=0),
    dcc.Store(id="selected-chart", data="pulse-pressure")
])

# Callback for chart selection
@app.callback(
    Output("selected-chart", "data"),
    [Input("pulse-pressure-btn", "n_clicks"),
     Input("temperature-btn", "n_clicks"),
     Input("spo2-btn", "n_clicks"),
     Input("respiratory-btn", "n_clicks")]
)
def update_selected_chart(pp_clicks, temp_clicks, spo2_clicks, resp_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "pulse-pressure"
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    chart_map = {
        "pulse-pressure-btn": "pulse-pressure",
        "temperature-btn": "temperature",
        "spo2-btn": "spo2",
        "respiratory-btn": "respiratory"
    }
    return chart_map.get(button_id, "pulse-pressure")

# Main callback for updating charts
@app.callback(
    Output("charts-container", "children"),
    [Input("interval", "n_intervals"),
     Input("selected-chart", "data")]
)
def update_charts(n, selected_chart):
    # Fetch data from MongoDB
    data = list(collection.find().sort("timestamp", -1).limit(100))
    df = pd.DataFrame(data)
    
    if df.empty:
        return html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H5("No Data Available", style={'color': COLORS['text'], 'text-align': 'center'}),
                    html.P("Please check your MongoDB connection and data.", 
                          style={'color': COLORS['medium'], 'text-align': 'center'})
                ])
            ], style=card_style)
        ])
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")
    
    # Create summary statistics function
    def create_summary_cards(values, unit, param_name):
        if len(values) > 0:
            avg_val = np.mean(values)
            min_val = np.min(values)
            max_val = np.max(values)
            current_val = values.iloc[-1] if len(values) > 0 else 0
            
            return dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P("Average", style={'margin': '0', 'font-size': '12px', 'color': COLORS['medium']}),
                        html.P(f"{avg_val:.1f} {unit}", style={'margin': '0', 'font-weight': '600', 'color': COLORS['text']})
                    ], style={'text-align': 'center', 'padding': '15px', 'background': COLORS['lightest'], 'border-radius': '8px'})
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.P("Minimum", style={'margin': '0', 'font-size': '12px', 'color': COLORS['medium']}),
                        html.P(f"{min_val:.1f} {unit}", style={'margin': '0', 'font-weight': '600', 'color': COLORS['text']})
                    ], style={'text-align': 'center', 'padding': '15px', 'background': COLORS['lightest'], 'border-radius': '8px'})
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.P("Maximum", style={'margin': '0', 'font-size': '12px', 'color': COLORS['medium']}),
                        html.P(f"{max_val:.1f} {unit}", style={'margin': '0', 'font-weight': '600', 'color': COLORS['text']})
                    ], style={'text-align': 'center', 'padding': '15px', 'background': COLORS['lightest'], 'border-radius': '8px'})
                ], width=3),
                dbc.Col([
                    html.Div([
                        html.P("Current", style={'margin': '0', 'font-size': '12px', 'color': COLORS['medium']}),
                        html.P(f"{current_val:.1f} {unit}", style={'margin': '0', 'font-weight': '600', 'color': COLORS['text']})
                    ], style={'text-align': 'center', 'padding': '15px', 'background': COLORS['lightest'], 
                             'border-radius': '8px'})
                ], width=3)
            ], className="mb-3")
        return html.P("No data available", style={'color': COLORS['medium'], 'text-align': 'center'})
    
    # Generate chart based on selection
    if selected_chart == "pulse-pressure":
        if 'pulse_pressure' in df.columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["timestamp"], 
                y=df["pulse_pressure"],
                mode="lines+markers", 
                name="Pulse Pressure",
                line=dict(color=COLORS['darkest'], width=3),
                marker=dict(size=6, color=COLORS['darkest']),
                fill='tozeroy', 
                fillcolor=f'rgba(0, 58, 107, 0.1)'
            ))
            
            fig.update_layout(
                title="Pulse Pressure Monitor",
                xaxis_title="Time",
                yaxis_title="mmHg",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Inter, sans-serif", color=COLORS['text']),
                xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                height=400,
                margin=dict(l=40, r=40, t=60, b=40)
            )
            
            summary = create_summary_cards(df["pulse_pressure"], "mmHg", "Pulse Pressure")
        else:
            fig = go.Figure()
            fig.update_layout(title="Pulse Pressure data not available", height=400)
            summary = html.P("No pulse pressure data available", style={'color': COLORS['medium']})
    
    elif selected_chart == "temperature":
        if 'temperature' in df.columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["timestamp"], 
                y=df["temperature"],
                mode="lines+markers", 
                name="Temperature",
                line=dict(color=COLORS['darkest'], width=3),
                marker=dict(size=6, color=COLORS['darkest'])
            ))
            
            # Add fever threshold line
            fig.add_hline(y=37.5, line_dash="dash", line_color='red', 
                         annotation_text="Fever Threshold (37.5°C)")
            
            fig.update_layout(
                title="Temperature Monitor",
                xaxis_title="Time",
                yaxis_title="°C",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Inter, sans-serif", color=COLORS['text']),
                xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                height=400,
                margin=dict(l=40, r=40, t=60, b=40)
            )
            
            summary = create_summary_cards(df["temperature"], "°C", "Temperature")
        else:
            fig = go.Figure()
            fig.update_layout(title="Temperature data not available", height=400)
            summary = html.P("No temperature data available", style={'color': COLORS['medium']})
    
    elif selected_chart == "spo2":
        if 'spo2' in df.columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["timestamp"], 
                y=df["spo2"],
                mode="lines+markers", 
                name="SpO2",
                line=dict(color=COLORS['darkest'], width=3),
                marker=dict(size=6, color=COLORS['darkest']),
                fill='tozeroy', 
                fillcolor=f'rgba(55, 118, 161, 0.1)'
            ))
            
            # Add normal SpO2 threshold line
            fig.add_hline(y=95, line_dash="dash", line_color='green', 
                         annotation_text="Normal SpO2 (95%+)")
            
            fig.update_layout(
                title="SpO2 Monitor",
                xaxis_title="Time",
                yaxis_title="%",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Inter, sans-serif", color=COLORS['text']),
                xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                height=400,
                margin=dict(l=40, r=40, t=60, b=40)
            )
            
            summary = create_summary_cards(df["spo2"], "%", "SpO2")
        else:
            fig = go.Figure()
            fig.update_layout(title="SpO2 data not available", height=400)
            summary = html.P("No SpO2 data available", style={'color': COLORS['medium']})
    
    elif selected_chart == "respiratory":
        if 'respiratory_rate' in df.columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["timestamp"], 
                y=df["respiratory_rate"],
                mode="lines+markers", 
                name="Respiratory Rate",
                line=dict(color=COLORS['darkest'], width=3),
                marker=dict(size=6, color=COLORS['darkest']),
                fill='tozeroy', 
                fillcolor=f'rgba(82, 147, 184, 0.1)'
            ))
            
            fig.update_layout(
                title="Respiratory Rate Monitor",
                xaxis_title="Time",
                yaxis_title="breaths/min",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Inter, sans-serif", color=COLORS['text']),
                xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                height=400,
                margin=dict(l=40, r=40, t=60, b=40)
            )
            
            summary = create_summary_cards(df["respiratory_rate"], "breaths/min", "Respiratory Rate")
        else:
            fig = go.Figure()
            fig.update_layout(title="Respiratory rate data not available", height=400)
            summary = html.P("No respiratory rate data available", style={'color': COLORS['medium']})
    
    return dbc.Card([
        dbc.CardBody([
            summary,
            dcc.Graph(figure=fig, style={'height': '400px'})
        ])
    ], style=card_style)

if __name__ == "__main__":
    listener_thread = threading.Thread(target=listen_for_apollo)
    listener_thread.daemon = True
    listener_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=8051) #change the port numbers and host accordingly to your own requirements
