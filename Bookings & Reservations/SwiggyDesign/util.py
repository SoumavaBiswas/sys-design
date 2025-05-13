from collections import namedtuple
import math


Location = namedtuple('Location', ['lat', 'lng'])

def get_distance(lat1, lat2, lng1, lng2) -> float:
    R = 6371  # Earth's radius in km

    # Convert degrees to radians
    lat1, lat2, lon1, lon2 = map(math.radians, [lat1, lat2, lon1, lon2])

    # Compute differences
    dx = (lon2 - lon1) * math.cos((lat1 + lat2) / 2)
    dy = (lat2 - lat1)

    # Apply Pythagorean theorem
    distance = R * math.sqrt(dx**2 + dy**2)
    
    return distance