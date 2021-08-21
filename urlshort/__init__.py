from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'to_be_hidden_if_put_to_production'

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app
