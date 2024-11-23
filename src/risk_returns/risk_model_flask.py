import os
import pandas as pd
import logging
from flask import Flask, render_template
from src.common.hydra_config_loader import load_config
from pathlib import Path

# Initialize Flask app
app = Flask(__name__)
logger = logging.getLogger(__name__)

# Load the configuration for risk models
config = load_config("risk_returns")


# Helper function to load .pkl files
def load_pkl_files(directory):
    pkl_files = []
    try:
        for file in Path(directory).glob("*.pkl"):
            df = pd.read_pickle(file)
            pkl_files.append((file.name, df))
    except Exception as e:
        logger.error(f"Error loading pkl files from {directory}: {e}")
    return pkl_files


# Helper function to convert DataFrame to HTML
def df_to_html(df):
    return df.to_html(classes='table table-striped', header="true", index=False)


# Endpoint for Risk Model
@app.route('/risk_model', methods=['GET'])
def risk_model():
    target_directory = config.get("target_data_directory", "data/risk_model")
    pkl_files = load_pkl_files(target_directory)

    if pkl_files:
        rendered_tables = []
        for filename, df in pkl_files:
            rendered_tables.append((filename, df_to_html(df)))
        return render_template('data_view.html', tables=rendered_tables, title="Risk Model Data")
    else:
        return "No Risk Model data found in target directory."


if __name__ == '__main__':
    # Run Flask app on specified port from config.yaml
    port = config.get('flask_port', 5002)
    app.run(debug=True, port=port)
