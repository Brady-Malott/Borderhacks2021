from flask import (
  Blueprint, redirect, render_template, request, session, url_for
)

bp = Blueprint('visualizer', __name__, url_prefix='/visualizer')


@bp.route('/', methods=('GET', 'POST'))
def visualizer():
    if request.method == 'POST':
        return redirect(url_for('form.form'))
        
    intervals_str = ''
    for score in session['intersection_scores']:
        interval = _get_interval(score)
        intervals_str += f'interval-{interval}'

    return render_template('visualizer/visualizer.html', intervals=intervals_str, to_flag=session['to_flag'])


def _get_interval(score):
    if score < 100:
        return 0
    elif score < 200:
        return 9
    elif score < 300:
        return 8
    elif score < 400:
        return 7
    elif score < 500:
        return 6
    elif score < 600:
        return 5
    elif score < 700:
        return 4
    elif score < 800:
        return 3
    elif score < 900:
        return 2
    return 1
