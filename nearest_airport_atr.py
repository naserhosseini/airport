
import geopandas as gpd
import pandas as pd
import numpy as np

airportDF = pd.read_csv('./Docs/airport.csv', header=0, low_memory=False)
runwaysDF = pd.read_csv('./Docs/runways.csv', header=0, low_memory=False)

pointDf = airportDF.set_index('Site_Id').join(runwaysDF.set_index('Site_Id'), how='inner', rsuffix='_a',lsuffix='_r')
pointDf = pointDf[pointDf['State_Id']=='TX']
pointDf = pointDf.reset_index()
pointDf['airp_lat'] = (pointDf['ARP_Latitude_Sec'].str[:-1]).astype('float')/3600
pointDf['airp_lng'] = (pointDf['ARP_Longitude_Sec'].str[:-1]).astype('float')/3600
pointDf['base_lat'] = (pointDf['Base_Latitude_Seconds'].str[:-1]).astype('float')/3600
pointDf['base_lng'] = (pointDf['Base_Longitude_Seconds'].str[:-1]).astype('float')/3600
pointDf['recp_lat'] = (pointDf['Reciprocal_Latitude_Seconds'].str[:-1]).astype('float')/3600
pointDf['recp_lng'] = (pointDf['Reciprocal_Longitude_Seconds'].str[:-1]).astype('float')/3600
pointDf['angle'] = np.degrees(np.arctan(((pointDf['recp_lat']-pointDf['base_lat'])/(pointDf['recp_lng']-pointDf['base_lng'])).to_numpy()))

TX_blocks = gpd.read_file('Docs/Texas.shp')
TX_blocks[['X','Y']] = TX_blocks['Centerpoin'].str.split(',', expand=True).astype('float')

X_TX_block_np = TX_blocks[['X']].to_numpy()
X_Airports_np = pointDf[['airp_lng']].to_numpy()
Y_TX_block_np = TX_blocks[['Y']].to_numpy()
Y_Airports_np = pointDf[['airp_lat']].to_numpy()

DX = (X_TX_block_np - X_Airports_np.transpose())**2
DY = (Y_TX_block_np - Y_Airports_np.transpose())**2

distance = (DX + DY)**0.5
min_dist = np.min(distance, axis=1)
min_indx = np.argmin(distance, axis=1)
