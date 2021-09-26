from typing import Match
import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas

BICYCLE_SCORE = 1
LIGHT_SCORE = 2
SINGLE_UNIT_SCORE = 3
BUS_SCORE = 4
ARTICILATED_TRUCKS = 5

warnings.simplefilter('ignore', InsecureRequestWarning)  # ignore that stupid stinky smelling warning


to_bridge = True
bridge_dir = 'N'

#Calculating the traffic score function
def traffic_score_calc(vehicle, quantity):
    if vehicle == 'Bicycle':
        return (BICYCLE_SCORE * quantity)
    if vehicle == 'MotorizedVehicle':
        return (BICYCLE_SCORE * quantity)        
    elif vehicle == 'Light':
        return (LIGHT_SCORE* quantity)
    elif vehicle == 'WorkVan':
        return (LIGHT_SCORE* quantity)        
    elif vehicle == 'SingleUnitTruck':
        return (SINGLE_UNIT_SCORE* quantity)
    elif vehicle == 'Bus':
        return (BUS_SCORE * quantity)
    elif vehicle == 'ArticulatedTruck':
        return (ARTICILATED_TRUCKS * quantity)
    else:   
        print(f'!!!vehicleType: {vehicle} was not listed!!!')

# RETRIEVE FORM INFORMATION + PROCESSING 

from flask import Flask, request, render_template 
app = Flask(__name__)

def _set_date_and_time():
    #Variables for time the api request
    form_info = dict
    @app.route('/form_input', methods=['GET','POST'])
    def form_in():
        form_info = request.form["/post_field"]
    year = 2021
    month = 9
    day = 24
    intersectionId = 1
    start_hour = 14  # uses 24 hour time
    start_minute = 28 # should be user input, not static
    end_hour = 14  # uses 24 hour time
    if (start_minute < 10):
        end_minute = start_minute + 10
    else: 
        end_minute, start_minute = start_minute, start_minute - 10

    link = f"https://opendata.citywindsor.ca/api/traffic?date={year}-{month}-{day}&intersectionId={intersectionId}&start_time={start_hour}%3A{start_minute}&end_time={end_hour}%3A{end_minute}"
    response = requests.get(link, verify=False)
    temp_response = response.json()
    print(f"This is the data for {temp_response['intersectionDescription']}:")
    return temp_response

def _get_traffic_score (intersectionId):  
    temp_response = _set_date_and_time()
    traffic_score = 0
    score = 0  
    for value in temp_response["traffic"]:
        #Vehicle information
         
        exit = value['exit']
        vehicleType = value['vehicleType']
        qty = value['qty']
        
        if exit == 'N':
                 score = traffic_score_calc(vehicleType, qty)
        elif exit == 'W':
                 score = traffic_score_calc(vehicleType, qty)
        elif exit == 'S':
                 score = traffic_score_calc(vehicleType, qty)
        elif exit == 'E':
                 score = traffic_score_calc(vehicleType, qty)
        traffic_score += score
        
        
    return traffic_score

print(_get_traffic_score(1))
