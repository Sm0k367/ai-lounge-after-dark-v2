from flask import Flask
import os

def create_app(config_class):
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), config_class.STATIC_FOLDER))
    app.config.from_object(config_class)

    # Register Blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Logging is handled by Vercel
    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    return app