import requests

api_key = '' #YOUR_API_KEY

def geocode(address):
  params = {'address':address,'key':api_key}
  response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
  return response.text
  location = response['results'][0]['geometry']['location']
  lat = location['lat']
  lng = location['lng']
  delimiter = ','
  return delimiter.join([lat,lng])

def rgeocode(lat,lng):
  response = {}
  address = response['results'][0].formatted_address
  return address