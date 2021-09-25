import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas

LIGHT_SCORE = 1
SINGLE_UNIT_SCORE = 2
BUS_SCORE = 3

warnings.simplefilter('ignore', InsecureRequestWarning)  # ignore that stupid stinky smelling warning

year = 2021
month = 9
day = 24
intersectionId = 1
start_hour = 14  # uses 24 hour time
start_minute = 20
end_hour = 14  # uses 24 hour time
end_minute = 21
to_bridge = True
bridge_dir = 'N'
traffic_score = 0

light_total = 0
single_unit_total = 0
bus_total = 0

link = f"https://opendata.citywindsor.ca/api/traffic?date={year}-{month}-{day}&intersectionId={intersectionId}&start_time={start_hour}%3A{start_minute}&end_time={end_hour}%3A{end_minute}"
response = requests.get(link, verify=False)
temp_response = response.json()

print(f"This is the data for {temp_response['intersectionDescription']}:")

for value in temp_response["traffic"]:
    entrance = value['entrance']
    exit = value['exit']
    vehicleType = value['vehicleType']
    qty = value['qty']
    if entrance == 'N' or exit == 'N':
        if vehicleType == 'Light' or vehicleType == 'Bicycle':
            traffic_score += LIGHT_SCORE * qty
            light_total += qty
        elif vehicleType == 'SingleUnitTruck':
            traffic_score += SINGLE_UNIT_SCORE * qty
            single_unit_total += qty
        elif vehicleType == 'Bus' or vehicleType == 'ArticulatedTruck':
            traffic_score += BUS_SCORE * qty
            bus_total += qty
        else:
            print(f'!!!vehicleType: {vehicleType} was not listed!!!')
    #print(f"At {value['timeStamp']}, {value['qty']} vehicles of type {value['vehicleType']} crossed from {value['entrance']} to {value['exit']}")

print(f"There were {light_total} light vehicle(s), {single_unit_total} single unit vehicle(s), and {bus_total} articulated truck(s)")
print(f"The traffic score is {traffic_score}")