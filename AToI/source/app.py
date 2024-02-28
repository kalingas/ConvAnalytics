from flask import Flask, request
#from flask_uploads import UploadSet, configure_uploads, DATA
from werkzeug.utils import secure_filename
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import (
        TextAnalyticsClient,
        RecognizeEntitiesAction,
        RecognizeLinkedEntitiesAction,
        RecognizePiiEntitiesAction,
        ExtractKeyPhrasesAction,
        AnalyzeSentimentAction,
    )
import os
import pandas as pd
import plotly
import plotly.express as px
import json

azure_key = "846747bd36354e50a3c8ce60cd4f4626"
azure_endpoint = "https://ithackathon-openai-dev-netapp-01.openai.azure.com/"

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the AI Chat Web Application!"
def parse_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path, engine='openpyxl')
    # Perform any required operations on the dataframe
    return df

# Configuration for file uploads
# app.config['UPLOADED_DATA_DEST'] = 'uploads'  # Folder where files will be saved
# data_files = UploadSet('data', DATA)
# configure_uploads(app, data_files)

# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'data_file' in request.files:
#         file = request.files['data_file']
#         filename = data_files.save(file)
#         file_path = os.path.join(app.config['UPLOADED_DATA_DEST'], filename)
#         df = parse_excel(file_path)
#         # Here you can call any analytics functions with the dataframe `df`
#         return "File uploaded and parsed successfully!"
#     return "No file uploaded."

app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'

def analyze_data(df):
    # Example: Summarize the data, perform analysis, etc.
    summary = df.describe()
    return summary

def generate_graph(df):
    # Example: Create a simple bar chart with Plotly
    fig = px.bar(df, x='ColumnName', y='AnotherColumnName')
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json

text_analytics_client = TextAnalyticsClient(endpoint=azure_endpoint, credential=AzureKeyCredential(azure_key))

def get_ai_response(message):
    response = text_analytics_client.begin_analyze_actions(message, actions=[
            RecognizeEntitiesAction(),
            RecognizePiiEntitiesAction(),
            ExtractKeyPhrasesAction(),
            RecognizeLinkedEntitiesAction(),
            AnalyzeSentimentAction(),
        ])
    # Extract the relevant response
    return response

@app.route('/chat/message', methods=['POST'])
def chat_message():
    data = request.json
    message = data.get('message')
    if message:
        response = get_ai_response(message)
        return response
    return {"error": "No message provided."}

if __name__ == '__main__':
    app.run(debug=True)