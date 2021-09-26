from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('visualizer', __name__, url_prefix='/visualizer')

@bp.route('/', methods=['GET'])
def visualizer():
    print("Visualizer - The traffic scores are:")
    for score in session['intersection_scores']:
      print(score)
    return render_template('visualizer/visualizer.html')
