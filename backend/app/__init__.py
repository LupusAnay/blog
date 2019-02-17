from flask import Flask


class ConfigNames:
    development = 'app.config.DevelopmentConfig'
    testing = 'app.config.TestingConfig'
    default = 'app.config.DefaultConfig'


def create_app(config_name: ConfigNames = ConfigNames.default) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_name)
    app.config.from_pyfile('config.cfg', silent=True)

    from app.models import db
    db.init_app(app)

    from app.views import posts_blueprint
    app.register_blueprint(posts_blueprint)

    return app
