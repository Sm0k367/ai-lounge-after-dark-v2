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

    # Basic logging setup (can be expanded)
    if not app.debug and not app.testing:
        import logging
        from logging.handlers import RotatingFileHandler
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/ai_lounge.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('AI Lounge After Dark startup')

    return app