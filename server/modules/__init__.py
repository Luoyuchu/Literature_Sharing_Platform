import os
import flask

from modules import db
from modules import auth
from modules import note
from modules import paper
from modules import rating
from modules import annotation


def create_app(test_config=None):
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    @app.route("/hello")
    def hello():
        return "Hello World"

    print(app.instance_path)

    app.register_blueprint(auth.bp)
    app.register_blueprint(paper.bp)
    app.register_blueprint(note.bp)
    app.register_blueprint(rating.bp)
    app.register_blueprint(annotation.bp)

    return app
