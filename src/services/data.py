from typing import Match
import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, time, date

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

# Utility function for fixing # hours/minutes < 10
# eg: Start time for 3:05 is 03:05
def _get_formatted_time_string(time):
    if time < 10:
        return f"0{time}"
    return f"{time}"


def _query_traffic_data(year, month, day, start_hour, start_minute):

    # First, setup the start and end minutes (10 minutes apart) 
    end_minute = None
    if start_minute < 10:
        end_minute = start_minute + 10
    else: 
        end_minute, start_minute = start_minute, start_minute - 10

    # Fix the start_time strings
    start_hour_str = _get_formatted_time_string(start_hour)
    start_minute_str = _get_formatted_time_string(start_minute)
    end_hour_str = start_hour_str
    end_minute_str = _get_formatted_time_string(end_minute)

    # Create the finalized start and end time strings
    start_time = f"{start_hour_str}:{start_minute_str}"
    end_time = f"{end_hour_str}:{end_minute_str}"

    # Store the traffic results for the 3 intersections
    traffic_data = []
    for intersection_id in range(1, 4):
        link = f"https://opendata.citywindsor.ca/api/traffic?date={year}-{month}-{day}&intersectionId={intersection_id}&start_time={start_time}&end_time={end_time}"
        response = requests.get(link, verify=False)
        traffic_array = response.json().get('traffic')
        traffic_data.append(traffic_array)
    
    return traffic_data

def _get_traffic_score (direction_headed, date):

    date = datetime.fromisoformat(date)
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute

    traffic_data = _query_traffic_data(year, month, day, hour, minute)

    intersection_scores = []
    # Get the traffic score for each intersection, and append each score to the intersection_scores list
    i = 1
    for intersection_data in traffic_data:
        traffic_score = _get_intersection_traffic_score(intersection_data, direction_headed)
        intersection_scores.append(traffic_score)
        i += 1
        
    return intersection_scores

def _get_intersection_traffic_score(intersection_data, direction_headed):
    traffic_score = 0

    for item in intersection_data:
        # Vehicle information
        exit_direction = item['exit']
        vehicle_type = item['vehicleType']
        qty = item['qty']
        
        if exit_direction == direction_headed:
            traffic_score += traffic_score_calc(vehicle_type, qty)     
        
    return traffic_score


print(_get_traffic_score("N", '2021-09-23T17:30:00'))
