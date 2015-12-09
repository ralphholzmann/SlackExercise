from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from config import config

# Extension objects
bootstrap = Bootstrap()


def create_app(configname):
    """A factory method which creates an app object from configname"""
    app = Flask(__name__)
    app.config.from_object(config[configname])
    config[configname].init_app(app)
    bootstrap.init_app(app)
    from .main  import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
