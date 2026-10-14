from flask import Flask


def create_app():
    application = Flask(__name__)
    from src.routes import orders_bp

    application.register_blueprint(orders_bp)
    return application


app = create_app()
