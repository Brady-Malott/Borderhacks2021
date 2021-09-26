import os

from flask import Flask
from config import Config

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Define the blueprints
from . import (form, visualizer)
app.register_blueprint(form.bp)
app.register_blueprint(visualizer.bp)