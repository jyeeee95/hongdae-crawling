import glob
import pandas as pd
from geo import *


file_list = []
df_list = []
path = "*.csv"

for fname in glob.glob(path):
    file_list.append(fname)

print(file_list)

for df in df_list:
    df = mapdata_refining(df)
    return df

# 저장 과정 필요(수정 해야함)
# all_mapdata_2012_4.to_csv("all_mapdata_2012_4.csv", index = False, mode='w')
# all_mapdata_2012_3.to_csv("all_mapdata_2012_3.csv", index = False, mode='w')
