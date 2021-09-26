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

def traffic_score_calc(vehicle, quantity):
    """Takes in a vehicle type and quantity, and returns the corresponding traffic score"""

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

def _get_formatted_time_string(time):
    """
    Utility function for fixing # hours/minutes < 10
    e.g. If hours are 3 and minutes are 5, call this function twice to get "03" and "05".
    Otherwise, the finalized time string will be "3:5" instead of "03:05"
    """

    if time < 10:
        return f"0{time}"
    return f"{time}"

def _query_traffic_data(year, month, day, start_hour, start_minute):
    """Takes in the query date and time and queries the traffic data API"""

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
    """Entry point called from form.py. Takes in the direction and date, and returns the traffic score at each intersection"""

    date = datetime.fromisoformat(date)
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute

    # traffic_data is a list of 3 lists: 1 list for the traffic records at each intersection
    traffic_data = _query_traffic_data(year, month, day, hour, minute)

    intersection_scores = []
    # Calculate the traffic score for each intersection, and append each score to the intersection_scores list
    i = 1
    for intersection_data in traffic_data:
        # Calculate the score for this intersection, and add it to the list
        traffic_score = _calculate_intersection_traffic_score(intersection_data, direction_headed)
        intersection_scores.append(traffic_score)
        i += 1
        
    return intersection_scores

def _calculate_intersection_traffic_score(intersection_data, direction_headed):
    """Takes in the traffic data for an intersection and calculates its score"""

    traffic_score = 0

    # intersection_data is a list of the traffic entries
    for item in intersection_data:
        # Vehicle information
        exit_direction = item['exit']
        vehicle_type = item['vehicleType']
        qty = item['qty']
        
        # If the vehicle is in the same direction as where the user is headed, add to the total traffic score
        if exit_direction == direction_headed:
            traffic_score += traffic_score_calc(vehicle_type, qty)     
        
    return traffic_score

# For testing from the command line
if __name__ == "__main__":
    print(_get_traffic_score("N", '2021-09-23T17:30:00'))
