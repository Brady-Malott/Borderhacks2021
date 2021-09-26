import os

from flask import Flask
from config import Config
from . import (form, visualizer)

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Define the blueprints
app.register_blueprint(form.bp)
app.register_blueprint(visualizer.bp)
