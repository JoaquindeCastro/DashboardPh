import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time
from pytz import timezone
from os import path
import requests

api_key = 'API KEY HERE'

def geocode(address):
  params = {'address':address,'key':api_key}
  response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
  location = response.json()['results'][0]['geometry']['location']
  lat = location['lat']
  lng = location['lng']
  return lat,lng

filename = 'labcom' + datetime.now().strftime('%d %b').replace(' ', '') + '.txt'

df = pd.read_csv("labdata.csv", encoding = "ISO-8859-1")

df = df[['Type', 'LAB ID', 'LAB NAME', 'STATUS', 'CONTACT PERSON','PHONE or MOBILE', 'EMAIL','ADDRESS']]

print(df)

first = True
for index, row in df.iterrows():
    d=row.to_dict()
    try:
        lat,lng = geocode(d['ADDRESS'])
    except:
        break
    dbcode = (
        f'db.establishments.update({{'\
        f'"type": "{d["Type"]}",'\
        f'"labId": {d["LAB ID"]},'\
        f'"name": "{d["LAB NAME"]}",'\
        f'"status": "{d["STATUS"]}",'\
        f'"contactPerson": "{d["CONTACT PERSON"]}",'\
        f'"phoneNumber": "{d["PHONE or MOBILE"]}",'\
        f'"email": "{d["EMAIL"]}",'\
        f'"address": "{d["ADDRESS"]}",'\
        f'"lat": {lat},'\
        f'"lng": {lng},'\
        f'"actions": [{{"category":"{d["STATUS"]}"}},{{"category":"{d["Type"]}"}}]'\
        f'}})'
        )
    if first:
        print(dbcode,  file=open(filename, "w"))
        first = False
    else:
        print(dbcode,  file=open(filename, "a"))