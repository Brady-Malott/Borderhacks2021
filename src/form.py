from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('form', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def form():
    if request.method == 'POST':

        error = None

        direction_headed = request.form.get('direction')
        travel_date = request.form.get('date')

        if not direction_headed:
            error = 'Please select the direction you are headed' 
        elif not travel_date:
            error = 'Please select a travel date and time'

        if error is None:
            # Set the form data in the session so it can be accessed by visualizer view
            session['direction_headed'] = direction_headed
            session['travel_date'] = travel_date
            # Clear any flash messages above the form
            session.pop('_flashes', None)
            # Redirect to the visualizer view
            return redirect(url_for('visualizer.visualizer'))

        flash(error)

    return render_template('form/form.html')