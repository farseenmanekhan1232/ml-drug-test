from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.Config")

    with app.app_context():
        # Include our Routes
        from . import routes

        # Register Blueprints
        app.register_blueprint(routes.bp)

        return app
