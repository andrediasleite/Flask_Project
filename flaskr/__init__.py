# To run:
# . venv_for_flask/bin/activate  - gets you virtual environment
#$ export FLASK_APP=flaskr
#$ export FLASK_ENV=development   - turns on debug / dev mode
#$ flask run

import os
import io
import base64
import matplotlib.pyplot as plt


from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
        

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import home
    app.register_blueprint(home.bp)
    #app.add_url_rule('/', endpoint='index')

    from . import plot
    app.register_blueprint(plot.bp)

    return app
