from flask import (
  Blueprint, flash, redirect, render_template, request, session, url_for
)
from matplotlib import pyplot as plt

# This was how we got importing the data module to work, don't change this
import sys, os
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])
from services import data

bp = Blueprint('form', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def form():
    if request.method == 'POST':
        error = None

        # Form validation
        direction = request.form.get('direction')
        travel_date = request.form.get('date')

        if not direction:
            error = 'Please select the direction you are headed' 
        elif not travel_date:
            error = 'Please select a travel date and time'

        # If the form is validated, get the traffic scores and set them in the session object
        if error is None:
            
            # First, change the direction string from (towards / from) to (N / S)
            direction_headed = 'N' if direction == 'towards' else 'S'

            # Clear any flash messages above the form
            session.pop('_flashes', None)

            # Get the traffic data
            results = data._get_traffic_data_results(direction_headed, travel_date)

            # Store the data for the visualizer view in session
            session['intersection_scores'] = results['intersection_scores']
            session['to_flag'] = direction_headed == 'N'

            _create_pie_chart(results['vehicle_counts'])

            # Redirect to the visualizer view
            return redirect(url_for('visualizer.visualizer'))

        # Else, flash the error above the form and stay on this page
        flash(error)
    else:
        return render_template('form/form.html')

def _create_pie_chart(vehicle_counts):

    colors_dict = {
        'Bicycle': 'red',
        'MotorizedVehicle': 'purple',
        'Light': 'blue',
        'WorkVan': 'grey',
        'SingleUnitTruck': 'green',
        'Bus': 'yellow',
        'ArticulatedTruck': 'orange'
    }

    # Creating dataset
    labels = []
    values = []
    colors = []
    for vehicle_type, quantity in vehicle_counts.items():
        if quantity > 0:
            labels.append(vehicle_type)
            values.append(quantity)
            colors.append(colors_dict[vehicle_type])
        
        # Creating plot
        fig = plt.figure(figsize =(15, 15))
        plt.pie(values, colors=colors, startangle=90)
        plt.legend(labels, loc='upper right', fontsize='xx-large')
        
        # Save the image to the static folder before being redirected to the visualizer view
        plt.savefig('src/static/pie_chart.png', facecolor='#f4f4f4')