import os
from app import create_app
from config import get_config

# Get the configuration based on FLASK_ENV
config_class = get_config()

# Create the Flask application instance
app = create_app(config_class)

# The following code is for local development and will not be used on Vercel
if __name__ == '__main__':
    # Ensure the videos directory exists
    videos_path = os.path.join(app.root_path, app.config['VIDEOS_FOLDER'])
    if not os.path.exists(videos_path):
        os.makedirs(videos_path)

    # Ensure the docs directory exists
    docs_path = os.path.join(app.root_path, app.config['DOCS_FOLDER'])
    if not os.path.exists(docs_path):
        os.makedirs(docs_path)

    app.run(host='0.0.0.0', port=5000)