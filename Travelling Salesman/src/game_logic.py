import random
import itertools
import time

CITIES = ["A","B","C","D","E","F","G","H","I","J"]

def generate_distance_matrix():
    """Random distance matrix between cities (50-100 km)"""
    matrix = {city:{} for city in CITIES}
    for i in range(len(CITIES)):
        for j in range(i+1, len(CITIES)):
            distance = random.randint(50, 100)
            matrix[CITIES[i]][CITIES[j]] = distance
            matrix[CITIES[j]][CITIES[i]] = distance
        matrix[CITIES[i]][CITIES[i]] = 0
    return matrix

def choose_home_city():
    return random.choice(CITIES)
