import csv
from datetime import datetime, timedelta, time

def format_date(date):
	date_str = date
	date_obj = datetime.strptime(date_str, "%B %d, %Y")
	datetime_obj = datetime.combine(date_obj, time())
	datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
	adjusted = datetime_obj - timedelta(hours=8, minutes=0)
	return adjusted

def valid_latlng(lat,lng):
	lat = float(lat)
	lng = float(lng)
	if lat > 5 and lat < 19 and lng > 116 and lng < 127:
		return True
	return False

with open('evac_centers_1.csv') as csv_file:
	csv_reader = csv.reader(csv_file,delimiter=',')
	for row in csv_reader:
		name = row[0]
		address = row[3:]
		calamityResourceType = 'RELIEF_CENTER'
		operatingHours = 0
		latlng = row[1].split(',')
		lat = latlng[0]
		lng = latlng[1]
		if valid_latlng(lat,lng):
			updatedAt = format_date('November 12, 2020')
			createdAt = format_date('November 12, 2020')
			dbcode = ''
			dbcode = str('db.CalamityResource.create({ "name": "' + str(name) + '"},' +
			'{ $set: ' +
			    '{ "address": ' + '"' + ','.join(address) + '"' ', ' +
			    '"lat": ' + str(lat) + ', ' +
			    '"lng": ' + str(lng) + ', ' +
			    'createdAt: ISODate("' + str(createdAt).replace(' ', 'T') + '")' + ','
			    'updatedAt: ISODate("' + str(updatedAt).replace(' ', 'T') + '")}})')
			print(dbcode,  file=open('dbcode.txt', "a"))

'''
5, 116
19, 127
'''