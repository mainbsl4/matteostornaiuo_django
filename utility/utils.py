# calculate distance 
from geopy.distance import geodesic

def calculate_distance(lat1, lon1, lat2, lon2, radius=25):
    # Create tuples for coordinates
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    
    # Calculate distance using geodesic function
    distance = geodesic(coord1, coord2).meters
    return distance


