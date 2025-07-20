import os
from flask import current_app, send_from_directory
from app.main import bp

@bp.route('/')
def serve_index():
    """Serves the main HTML page."""
    return send_from_directory(current_app.static_folder, 'index.html')

@bp.route('/videos/<filename>')
def serve_video(filename):
    """Serves the generated video files."""
    videos_dir = os.path.join(current_app.root_path, current_app.config['VIDEOS_FOLDER'])
    return send_from_directory(videos_dir, filename)

@bp.route('/docs/<filename>')
def serve_doc(filename):
    """Serves documentation files (whitepapers)."""
    docs_dir = os.path.join(current_app.root_path, current_app.config['DOCS_FOLDER'])
    return send_from_directory(docs_dir, filename)