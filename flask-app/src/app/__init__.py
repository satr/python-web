from flask import Flask

app = Flask(__name__)

def create_app(config_name=None):
    from .routes import bp as routex_bp
    app.register_blueprint(routex_bp)
    return app