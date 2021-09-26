from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# This was how we got importing the data module to work, don't change this
import sys, os
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])
from services import data

bp = Blueprint('form', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def form():
    if request.method == 'POST':

        error = None

        direction = request.form.get('direction')
        travel_date = request.form.get('date')

        if not direction:
            error = 'Please select the direction you are headed' 
        elif not travel_date:
            error = 'Please select a travel date and time'

        if error is None:
            
            # First, change the direction string from (towards / from) to (N / S)
            direction_headed = 'N' if direction == 'towards' else 'S'

            # Set the form data in the session so it can be accessed by visualizer view
            # session['direction_headed'] = direction_headed
            # session['travel_date'] = travel_date

            # Clear any flash messages above the form
            session.pop('_flashes', None)

            # Get the traffic data for the 3 intersections
            session['intersection_scores'] = data._get_traffic_score(direction_headed, travel_date)
            session['to_flag'] = direction_headed == 'N'

            # Redirect to the visualizer view
            return redirect(url_for('visualizer.visualizer'))

        flash(error)

    return render_template('form/form.html')