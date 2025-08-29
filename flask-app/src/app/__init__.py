from flask import Flask

def create_app(config_name=None):
    app = Flask(__name__)
    from app.routes.main import main_bp
    from app.routes.order import order_bp
    from app.routes.product import product_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(product_bp)
    return app