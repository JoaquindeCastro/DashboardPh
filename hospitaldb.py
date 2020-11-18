import pandas
import pandas as pd

df=pd.read_csv('nodupl.csv')
dbarray = []
for index, row in df.iterrows():
	dbdict = {}
	d=row.to_dict()
	dbdict['healthFacilityCode'] = str(d['healthFacilityCode'])
	dbdict['icuBedsAvailable'] = d['icuBedsAvailable']
	dbdict['regularBedsAvailable'] = d['regularBedsAvailable']
	dbdict['availabilitySource'] = "DOH"
	dbdict['updatedAt'] = {'$date': str(d['updatedAt'])}
	dbarray.append(dbdict)
dbdf = pandas.DataFrame(dbarray)
dbdf.to_csv('finalresults.csv', index=False)
print(dbdf)
