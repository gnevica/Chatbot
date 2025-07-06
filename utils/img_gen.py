import requests

def generate_place_image(place):
    return f"https://via.placeholder.com/400x200.png?text=AI+Image+of+{place.replace(' ', '+')}"