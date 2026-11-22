#Seneca and Sky Final Project - ENV 859 
#This script will pull data required for further analysis of Giant Kelp suitability based on EEZ boundaries, temperature, and depth conditions.

#Package Library
import arcpy

#Import datasets
#Pull hexagon spatial analysis units from NOAA/ESRI
sde_hexview = r"V:/CA_Aquaculture_Spatial_Planning/data/OCIS.SDE.OCIS_MASTER_VIEW"
hexoutput_fc = r"V:/CA_Aquaculture_Spatial_Planning/data/OCIS_MASTER_VIEW_local"

arcpy.conversion.ExportFeatures(sde_hexview, hexoutput_fc)

#Pull temperature data from HYCOM and GFOS

#Pull US EEZ data from NOAA GeoPlatform

#Pull depth data from GEBCO
