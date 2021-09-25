from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('form', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def form():
    if request.method == 'POST':
        # username = request.form['username']
        # password = request.form['password']
        error = None

        # if not username:
        #     error = 'Username is required.'
        # elif not password:
        #     error = 'Password is required.'

        if error is None:
            # Submit form data
            pass

        flash(error)

    return render_template('form/form.html')