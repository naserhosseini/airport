import geopandas as gpd
import numpy
import numpy as np
import pandas as pd
from datetime import datetime

print(0, datetime.now())
TX_blocks = gpd.read_file('Docs/st99_d00_shp/Texas.shp')
TX_blocks[['X', 'Y']] = TX_blocks['Centerpoin'].str.split(',', expand=True).astype('float')

print(1, datetime.now())
pointDf = pd.read_csv('Docs/all-airport-data.csv', header=0)
pointDf = pointDf[pointDf['State_Id'] == 'TX']
pointDf['Longitude'] = pointDf['Longitude'].astype(float, errors='raise')
pointDf = pointDf.reset_index()

print(2, datetime.now())
X_TX_block_np = TX_blocks[['X']].to_numpy()
X_Airports_np = pointDf[['Longitude']].to_numpy()
Y_TX_block_np = TX_blocks[['Y']].to_numpy()
Y_Airports_np = pointDf[['Latitude']].to_numpy()

print(3, datetime.now())
DX = (X_TX_block_np - X_Airports_np.transpose())**2
DY = (Y_TX_block_np - Y_Airports_np.transpose())**2

print(4, datetime.now())
distance = (DX + DY)**0.5

print(5, datetime.now())
print(distance.shape)
min_dist = np.min(distance, axis=1)
min_indx = np.argmin(distance, axis=1)
print(min_dist, '\n', min_indx)
print(len(min_dist), '\n', len(min_indx))
print(6, datetime.now())
