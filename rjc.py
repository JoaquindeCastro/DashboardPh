import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time
from pytz import timezone

# df = pd.read_csv("dohdata.csv", encoding = "ISO-8859-1")
#
# codes = df['hfhudcode'].dropna().unique()
#
# df2 = pd.DataFrame()
#
# for code in codes:
#     df3 = df[df['hfhudcode'] == code].sort_values(by = 'updateddate', ascending = False).iloc[0]
#     df2 = df2.append(df3)
#
# df2 = df2[['hfhudcode', 'cfname', 'updateddate', 'icu_v', 'isolbed_v', 'beds_ward_v']]

filename = 'testcom' + datetime.now().strftime('%d %b').replace(' ', '') + '.txt'

# for index, row in df2.iterrows():
# 	d=row.to_dict()
# 	date_str = d['updateddate']
# 	datetime_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
# 	datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
# 	date = datetime_obj - timedelta(hours=8, minutes=0)
# 	dbcode = ''
# 	dbcode = str('db.hospitals.update({ "healthFacilityCode": "' + str(d['hfhudcode']) + '"},' +
#     '{ $set: ' +
#         '{ "icuBedsAvailable": ' + str(d['icu_v']) + ', ' +
#         '"regularBedsAvailable":' + str(int(d['beds_ward_v']) + int(d['isolbed_v'])) + ', ' +
#         'availabilitySource: "DOH", ' +
#         'updatedAt: ISODate("' + str(date).replace(' ', 'T') + '")}})')
# 	print(dbcode,  file=open(filename, "a"))

agg = pd.read_csv('testag.csv')

hfcs = []
for _, row in agg[['Name of Health Facility/Laboratory', 'Abbrev of Health Facility']].iterrows():
    d = row.to_dict()
    abb = d['Abbrev of Health Facility']
    if type(abb) == str:
        hfcs.append('CTS-' + str(abb))
    else:
        name = d['Name of Health Facility/Laboratory']
        if name == 'Detoxicare Molecular Diagnostics Laboratory':
            hfcs.append('CTS-DMDL')
        elif name == 'V. Luna Hospital':
            hfcs.append('CTS-VLH')
        else: 
            hfcs.append('')

agg['hfcs'] = hfcs
hfcs = pd.Series(hfcs).dropna().unique()


tk_counts = pd.DataFrame()

for h in hfcs:
    tk_count = agg[agg['hfcs'] == h].sort_values(by = 'Date', ascending = False).iloc[0]
    tk_counts = tk_counts.append(tk_count)

tk_counts['tests'] = tk_counts['REMAINING AVAILABLE TESTS'].str.replace(',', '').map(int)
tk_counts = tk_counts[['hfcs', 'tests', 'Date']]
tk_counts

for _, tsite in tk_counts.iterrows():
    d = tsite.to_dict()
    date_str = d['Date']
    date_obj = datetime.strptime(date_str, "%B %d, %Y")
    datetime_obj = datetime.combine(date_obj, time())
    datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    adjusted = datetime_obj - timedelta(hours=8, minutes=0)
    dbcode = ''
    dbcode = str('db.hospitals.update({ "healthFacilityCode": "' + str(d['hfcs']) + '"},' +
    '{ $set: ' +
        '{ "regularBedsAvailable": ' + str(d['tests']) + ', ' +
        'availabilitySource: "DOH", ' +
        'updatedAt: ISODate("' + str(adjusted).replace(' ', 'T') + '")}})')
    print(dbcode,  file=open(filename, "a"))
