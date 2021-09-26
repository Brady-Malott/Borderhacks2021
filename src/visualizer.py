from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

bp = Blueprint('visualizer', __name__, url_prefix='/visualizer')

@bp.route('/', methods=['GET'])
def visualizer():
    print("Visualizer - The traffic scores are:")
    for score in session['intersection_scores']:
      print(score)

    intervals = [1, 4, 6]
    intervals_str = ''
    for interval in intervals:
      intervals_str += f'interval-{interval}'

    return render_template('visualizer/visualizer.html', intervals=intervals_str, to_flag=session['to_flag'])
