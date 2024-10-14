import os
import pandas as pd
import logging
from flask import Flask, render_template
from plugIn.common.hydra_config_loader import load_config
from pathlib import Path

# Initialize Flask app
app = Flask(__name__)
logger = logging.getLogger(__name__)

# Load the configuration for expected return
module_name = os.path.basename(os.path.dirname(__file__))
config = load_config(module_name)


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


# Endpoint for Expected Return
@app.route('/optimization', methods=['GET'])
def expected_return():
    pkl_files = load_pkl_files(config.target_data_directory)

    if pkl_files:
        rendered_tables = []
        for filename, df in pkl_files:
            rendered_tables.append((filename, df_to_html(df)))
        return render_template(config.data_view_html_file, tables=rendered_tables, title="Expected Return Data")
    else:
        return "No Expected Return data found in target directory."


if __name__ == '__main__':
    # Run Flask app on specified port from config.yaml
    port = config.get('flask_port', 5001)
    app.run(debug=True, port=port)
