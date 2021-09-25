from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('visualizer', __name__, url_prefix='/visualizer')

@bp.route('/', methods=['GET'])
def visualizer():
    return render_template('visualizer/visualizer.html')
