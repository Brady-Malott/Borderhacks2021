from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

bp = Blueprint('visualizer', __name__, url_prefix='/visualizer')

@bp.route('/', methods=['GET'])
def visualizer():
    flash('C')
    print('Visualizer - The traffic scores are:')
    for score in session['intersection_scores']:
        print(score)
    print(f'Direction: {"to" if session["to_flag"] else "from"} the bridge')

    intervals_str = ''
    for score in session['intersection_scores']:
        interval = _get_interval(score)
        intervals_str += f'interval-{interval}'

    return render_template('visualizer/visualizer.html', intervals=intervals_str, to_flag=session['to_flag'])

def _get_interval(score):
    if score < 150:
        return 0
    elif score < 300:
        return 9
    elif score < 450:
        return 8
    elif score < 600:
        return 7
    elif score < 750:
        return 6
    elif score < 900:
        return 5
    elif score < 1050:
        return 4
    elif score < 1200:
        return 3
    elif score < 1350:
        return 2
    return 1
