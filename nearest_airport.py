import geopandas as gpd
import pandas as pd
import numpy as np

TX_blocks = gpd.read_file('Docs/Texas.shp')
TX_blocks[['X','Y']] = TX_blocks['Centerpoin'].str.split(',', expand=True).astype('float')

pointDf = pd.read_csv('./Docs/all-airport-data.csv', header=0)
pointDf = pointDf[pointDf['State_Id']=='TX']
pointDf['Longitude']= pointDf['Longitude'].astype(float, errors = 'raise')
pointDf = pointDf.reset_index()

X_TX_block_np = TX_blocks[['X']].to_numpy()
X_Airports_np = pointDf[['Longitude']].to_numpy()
Y_TX_block_np = TX_blocks[['Y']].to_numpy()
Y_Airports_np = pointDf[['Latitude']].to_numpy()

DX = (X_TX_block_np - X_Airports_np.transpose())**2
DY = (Y_TX_block_np - Y_Airports_np.transpose())**2

distance = (DX + DY)**0.5
min_dist = np.min(distance, axis=1)
min_indx = np.argmin(distance, axis=1)
