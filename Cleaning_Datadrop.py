import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pytz import timezone

df = pd.read_csv("dohdata.csv", encoding = "ISO-8859-1")

codes = df['hfhudcode'].dropna().unique()

df2 = pd.DataFrame()

for code in codes:
    df3 = df[df['hfhudcode'] == code].sort_values(by = 'updateddate', ascending = False).iloc[0]
    df2 = df2.append(df3)
	
df2 = df2[['hfhudcode', 'cfname', 'updateddate', 'icu_v', 'isolbed_v', 'beds_ward_v']]

df2.to_csv("result.csv", encoding = "ISO-8859-1")

