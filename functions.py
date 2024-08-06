from geopy.geocoders import Nominatim

# Функция для получения координат по адресу с сайта OpenStreetMap
def get_location(address):
    geolocator = Nominatim(user_agent='MyGeaopyUA')
    try:
        location = geolocator.geocode(address)
    except Exception as e:
        print(e)
        location = None
    if location:
        if location.raw.get('class') == 'building':
            return location.latitude, location.longitude
        else:
            print('It is not a building')
            return None
    else:
        print('location is empty on NominAPI')
        return None
