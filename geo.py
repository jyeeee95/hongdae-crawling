import pandas as pd
from pyproj import Proj
from pyproj import transform

# https://gist.github.com/allieus/1180051/ab33229e820a5eb60f8c7971b8d1f1fc8f2cfabb

WGS84 = { 'proj':'latlong', 'datum':'WGS84', 'ellps':'WGS84', }

TM128 = { 'proj':'tmerc', 'lat_0':'38N', 'lon_0':'128E', 'ellps':'bessel',
   'x_0':'400000', 'y_0':'600000', 'k':'0.9999',
   'towgs84':'-146.43,507.89,681.46'}


def tm128_to_wgs84(x, y):
   return transform( Proj(**TM128), Proj(**WGS84), x, y )


def mapdata_refining(map_dataframe):
	for index, location in map_dataframe.iterrows():
		if location['longitude'] > 150:
			if location['latitude'] > 40:
				x, y = tm128_to_wgs84(location['longitude'], location['latitude'])
		else:
			x, y = location['longitude'], location['latitude']

		map_dataframe.at[index, 'longitude'] = x
		map_dataframe.at[index, 'latitude'] = y
	return map_dataframe


# # example
# all_mapdata_2012_4 = pd.read_csv("all_mapdata_2012_4.csv", encoding = 'utf-8')
# all_mapdata_2012_3 = pd.read_csv("all_mapdata_2012_3.csv", encoding = 'utf-8')
#
#
# all_mapdata_2012_4 = mapdata_refining(all_mapdata_2012_4)
# all_mapdata_2012_3 = mapdata_refining(all_mapdata_2012_3)
#
# all_mapdata_2012_4.to_csv("all_mapdata_2012_4.csv", index = False, mode='w')
# all_mapdata_2012_3.to_csv("all_mapdata_2012_3.csv", index = False, mode='w')
#
#
