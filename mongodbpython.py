import pandas
import pandas as pd

df=pd.read_csv('datadoh.txt')
dbarray = []
for index, row in df.iterrows():
	dbdict = {}
	d=row.to_dict()
	dbdict['healthFacilityCode'] = str(d['hfhudcode'])
	dbdict['icuBedsAvailable'] = d['icu_v']
	dbdict['regularBedsAvailable'] = d['beds_ward_v']
	dbdict['availabilitySource'] = "DOH"
	dbdict['updatedAt'] = str(d['updateddate'])
	dbarray.append(dbdict)
dbdf = pandas.DataFrame(dbarray)
dbdf.to_csv('results.csv', index=False)
print(dbdf)
