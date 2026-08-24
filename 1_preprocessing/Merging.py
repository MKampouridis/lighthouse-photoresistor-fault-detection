####################################################################################################################
####################################################################################################################
####################################################################################################################
#############################  Pre-processing: Merges telemetry and climate data into a single file. ################
#############################  Climate data are hourly and thus the exact time found in telemetry is interpolated ###
####################################################################################################################
####################################################################################################################
import numpy as np
import pandas as pd
import sys
import datetime
import pvlib
from pvlib import location


def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError("Cannot convert {} to a bool".format(s))


nlb = str_to_bool(sys.argv[1])
clean = str_to_bool(sys.argv[2])
drifted = str_to_bool(sys.argv[3])
path = './NLB/' if nlb is True else './TH/'
station_filename = path + 'Telemetry Data-UTC/' if drifted is False else path + 'Telemetry Data-UTC/drifted/'
climate_filename = path + 'Climate Data/1-min/'

output_path = ''
if drifted is True:  # we only use CL for drifted, hence I don't differentiate between CL and non-CL folders
    output_path = path + 'drifted/1-min/'
else:
    output_path = path + 'input-utc/1-min/' if clean is False else path + 'input-utc-cl/1-min/'

filenames_dict = {}

if nlb is True and clean is False:
    filenames_dict['Balta'] = ['Balta_Sound', 'BaltaSound', 60.741, -0.795]
    filenames_dict['Dunnet'] = ['Dunnet_Head', 'DunnetHead', 58.672, -3.377]
    filenames_dict['Flotta'] = ['Flotta_Grinds_Buoy', 'FlottaGrinds', 58.85, -3.014]
    filenames_dict['Mousa'] = ['Mousa', 'Mousa', 59.998, -1.159]
    # There's no difference between raw and clean data for Mousa drifted, as the drifted data are already cleaned. So
    # the merging happens below in the CL section and no need to re-happen here.
    filenames_dict['NorthRona'] = ['North_Rona', 'NorthRona', 59.122, -5.816]
    filenames_dict['NorthRonald'] = ['North_RonaldSay', 'NorthRonaldSay', 59.39, -2.382]
    filenames_dict['Sule'] = ['Sule_Skerry', 'SuleSkerry', 59.086, -4.407]
    filenames_dict['Sumburgh'] = ['Sumburgh_Head', 'SumburghHead', 59.854, -1.276]
elif nlb is True and clean is True:
    if drifted is False:
        filenames_dict['Balta'] = ['Balta_Sound_CL', 'BaltaSound', 60.741, -0.795]
        filenames_dict['Dunnet'] = ['Dunnet_Head_CL', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Flotta'] = ['Flotta_Grinds_Buoy_CL', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Mousa'] = ['Mousa_CL', 'Mousa', 59.998, -1.159]
        filenames_dict['NorthRona'] = ['North_Rona_CL', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRonald'] = ['North_RonaldSay_CL', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['Sule'] = ['Sule_Skerry_CL', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sumburgh'] = ['Sumburgh_Head_CL', 'SumburghHead', 59.854, -1.276]
    else:
        filenames_dict['Balta-1'] = ['Balta_Sound_Drifted-1', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta1'] = ['Balta_Sound_Drifted1', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta-5'] = ['Balta_Sound_Drifted-5', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta5'] = ['Balta_Sound_Drifted5', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta-10'] = ['Balta_Sound_Drifted-10', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta10'] = ['Balta_Sound_Drifted10', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta-15'] = ['Balta_Sound_Drifted-15', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta15'] = ['Balta_Sound_Drifted15', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta-20'] = ['Balta_Sound_Drifted-20', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta20'] = ['Balta_Sound_Drifted20', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta-25'] = ['Balta_Sound_Drifted-25', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta25'] = ['Balta_Sound_Drifted25', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta-30'] = ['Balta_Sound_Drifted-30', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Balta30'] = ['Balta_Sound_Drifted30', 'BaltaSound', 60.741,	-0.795]
        filenames_dict['Dunnet-1'] = ['Dunnet_Head_Drifted-1', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet1'] = ['Dunnet_Head_Drifted1', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet-5'] = ['Dunnet_Head_Drifted-5', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet5'] = ['Dunnet_Head_Drifted5', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet-10'] = ['Dunnet_Head_Drifted-10', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet10'] = ['Dunnet_Head_Drifted10', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet-15'] = ['Dunnet_Head_Drifted-15', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet15'] = ['Dunnet_Head_Drifted15', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet-20'] = ['Dunnet_Head_Drifted-20', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet20'] = ['Dunnet_Head_Drifted20', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet-25'] = ['Dunnet_Head_Drifted-25', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet25'] = ['Dunnet_Head_Drifted25', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet-30'] = ['Dunnet_Head_Drifted-30', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Dunnet30'] = ['Dunnet_Head_Drifted30', 'DunnetHead', 58.672, -3.377]
        filenames_dict['Flotta-1'] = ['Flotta_Grinds_Buoy_Drifted-1', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta1'] = ['Flotta_Grinds_Buoy_Drifted1', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta-5'] = ['Flotta_Grinds_Buoy_Drifted-5', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta5'] = ['Flotta_Grinds_Buoy_Drifted5', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta-10'] = ['Flotta_Grinds_Buoy_Drifted-10', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta10'] = ['Flotta_Grinds_Buoy_Drifted10', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta-15'] = ['Flotta_Grinds_Buoy_Drifted-15', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta15'] = ['Flotta_Grinds_Buoy_Drifted15', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta-20'] = ['Flotta_Grinds_Buoy_Drifted-20', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta20'] = ['Flotta_Grinds_Buoy_Drifted20', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta-25'] = ['Flotta_Grinds_Buoy_Drifted-25', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta25'] = ['Flotta_Grinds_Buoy_Drifted25', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta-30'] = ['Flotta_Grinds_Buoy_Drifted-30', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['Flotta30'] = ['Flotta_Grinds_Buoy_Drifted30', 'FlottaGrinds', 58.85, -3.014]
        filenames_dict['MousaDrifted-1'] = ['Mousa_Drifted-1', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted-5'] = ['Mousa_Drifted-5', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted-10'] = ['Mousa_Drifted-10', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted-15'] = ['Mousa_Drifted-15', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted-20'] = ['Mousa_Drifted-20', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted-25'] = ['Mousa_Drifted-25', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted-30'] = ['Mousa_Drifted-30', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted1'] = ['Mousa_Drifted1', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted5'] = ['Mousa_Drifted5', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted10'] = ['Mousa_Drifted10', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted15'] = ['Mousa_Drifted15', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted20'] = ['Mousa_Drifted20', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted25'] = ['Mousa_Drifted25', 'Mousa', 59.998, -1.159]
        filenames_dict['MousaDrifted30'] = ['Mousa_Drifted30', 'Mousa', 59.998, -1.159]
        filenames_dict['NorthRona-1'] = ['North_Rona_Drifted-1', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona1'] = ['North_Rona_Drifted1', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona-5'] = ['North_Rona_Drifted-5', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona5'] = ['North_Rona_Drifted5', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona-10'] = ['North_Rona_Drifted-10', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona10'] = ['North_Rona_Drifted10', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona-15'] = ['North_Rona_Drifted-15', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona15'] = ['North_Rona_Drifted15', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona-20'] = ['North_Rona_Drifted-20', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona20'] = ['North_Rona_Drifted20', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona-25'] = ['North_Rona_Drifted-25', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona25'] = ['North_Rona_Drifted25', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona-30'] = ['North_Rona_Drifted-30', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRona30'] = ['North_Rona_Drifted30', 'NorthRona', 59.122, -5.816]
        filenames_dict['NorthRonald-1'] = ['North_RonaldSay_Drifted-1', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald1'] = ['North_RonaldSay_Drifted1', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald-5'] = ['North_RonaldSay_Drifted-5', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald5'] = ['North_RonaldSay_Drifted5', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald-10'] = ['North_RonaldSay_Drifted-10', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald10'] = ['North_RonaldSay_Drifted10', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald-15'] = ['North_RonaldSay_Drifted-15', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald15'] = ['North_RonaldSay_Drifted15', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald-20'] = ['North_RonaldSay_Drifted-20', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald20'] = ['North_RonaldSay_Drifted20', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald-25'] = ['North_RonaldSay_Drifted-25', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald25'] = ['North_RonaldSay_Drifted25', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald-30'] = ['North_RonaldSay_Drifted-30', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['NorthRonald30'] = ['North_RonaldSay_Drifted30', 'NorthRonaldSay', 59.39, -2.382]
        filenames_dict['Sule-1'] = ['Sule_Skerry_Drifted-1', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule1'] = ['Sule_Skerry_Drifted1', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule-5'] = ['Sule_Skerry_Drifted-5', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule5'] = ['Sule_Skerry_Drifted5', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule-10'] = ['Sule_Skerry_Drifted-10', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule10'] = ['Sule_Skerry_Drifted10', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule-15'] = ['Sule_Skerry_Drifted-15', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule15'] = ['Sule_Skerry_Drifted15', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule-20'] = ['Sule_Skerry_Drifted-20', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule20'] = ['Sule_Skerry_Drifted20', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule-25'] = ['Sule_Skerry_Drifted-25', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule25'] = ['Sule_Skerry_Drifted25', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule-30'] = ['Sule_Skerry_Drifted-30', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sule30'] = ['Sule_Skerry_Drifted30', 'SuleSkerry', 59.086, -4.407]
        filenames_dict['Sumburgh-1'] = ['Sumburgh_Head_Drifted-1', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh1'] = ['Sumburgh_Head_Drifted1', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh-5'] = ['Sumburgh_Head_Drifted-5', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh5'] = ['Sumburgh_Head_Drifted5', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh-10'] = ['Sumburgh_Head_Drifted-10', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh10'] = ['Sumburgh_Head_Drifted10', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh-15'] = ['Sumburgh_Head_Drifted-15', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh15'] = ['Sumburgh_Head_Drifted15', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh-20'] = ['Sumburgh_Head_Drifted-20', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh20'] = ['Sumburgh_Head_Drifted20', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh-25'] = ['Sumburgh_Head_Drifted-25', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh25'] = ['Sumburgh_Head_Drifted25', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh-30'] = ['Sumburgh_Head_Drifted-30', 'SumburghHead', 59.854, -1.276]
        filenames_dict['Sumburgh30'] = ['Sumburgh_Head_Drifted30', 'SumburghHead', 59.854, -1.276]

elif nlb is False and clean is True:
    if drifted is False:
        filenames_dict['Bishop'] = ['BishopRock_CL', 'BishopRock', 49.868, -6.435]
        # filenames_dict['BullPost'] = ['BullPointPost_CL', 'BullPointPost', 51.2, -4.202]
        # filenames_dict['BullPre'] = ['BullPointPre_CL', 'BullPointPre', 51.2, -4.202]
        filenames_dict['Eddy'] = ['Eddystone_CL', 'Eddystone', 50.184, -4.268]
        filenames_dict['Godrevy'] = ['Godrevy_CL', 'Godrevy', 50.235, -5.401]
        filenames_dict['Lizard'] = ['Lizard_CL', 'Lizard', 49.961, -5.203]
        filenames_dict['Longships'] = ['Longships_CL', 'Longships', 50.067, -5.735]
        filenames_dict['Trevose'] = ['Trevose_CL', 'Trevose', 50.535, -5.034]
        filenames_dict['WolfRock'] = ['WolfRock_CL', 'WolfRock', 49.935, -5.801]
    else:
        filenames_dict['Bishop-1'] = ['BishopRock_Drifted-1', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop1'] = ['BishopRock_Drifted1', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop-5'] = ['BishopRock_Drifted-5', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop5'] = ['BishopRock_Drifted5', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop-10'] = ['BishopRock_Drifted-10', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop10'] = ['BishopRock_Drifted10', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop-15'] = ['BishopRock_Drifted-15', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop15'] = ['BishopRock_Drifted15', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop-20'] = ['BishopRock_Drifted-20', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop20'] = ['BishopRock_Drifted20', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop-25'] = ['BishopRock_Drifted-25', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop25'] = ['BishopRock_Drifted25', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop-30'] = ['BishopRock_Drifted-30', 'BishopRock', 49.868, -6.435]
        filenames_dict['Bishop30'] = ['BishopRock_Drifted30', 'BishopRock', 49.868, -6.435]
        filenames_dict['Eddy-1'] = ['Eddystone_Drifted-1', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy1'] = ['Eddystone_Drifted1', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy-5'] = ['Eddystone_Drifted-5', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy5'] = ['Eddystone_Drifted5', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy-10'] = ['Eddystone_Drifted-10', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy10'] = ['Eddystone_Drifted10', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy-15'] = ['Eddystone_Drifted-15', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy15'] = ['Eddystone_Drifted15', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy-20'] = ['Eddystone_Drifted-20', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy20'] = ['Eddystone_Drifted20', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy-25'] = ['Eddystone_Drifted-25', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy25'] = ['Eddystone_Drifted25', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy-30'] = ['Eddystone_Drifted-30', 'Eddystone', 50.184, -4.268]
        filenames_dict['Eddy30'] = ['Eddystone_Drifted30', 'Eddystone', 50.184, -4.268]
        filenames_dict['Godrevy-1'] = ['Godrevy_Drifted-1', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy1'] = ['Godrevy_Drifted1', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy-5'] = ['Godrevy_Drifted-5', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy5'] = ['Godrevy_Drifted5', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy-10'] = ['Godrevy_Drifted-10', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy10'] = ['Godrevy_Drifted10', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy-15'] = ['Godrevy_Drifted-15', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy15'] = ['Godrevy_Drifted15', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy-20'] = ['Godrevy_Drifted-20', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy20'] = ['Godrevy_Drifted20', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy-25'] = ['Godrevy_Drifted-25', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy25'] = ['Godrevy_Drifted25', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy-30'] = ['Godrevy_Drifted-30', 'Godrevy', 50.235, -5.401]
        filenames_dict['Godrevy30'] = ['Godrevy_Drifted30', 'Godrevy', 50.235, -5.401]
        filenames_dict['Lizard-1'] = ['Lizard_Drifted-1', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard1'] = ['Lizard_Drifted1', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard-5'] = ['Lizard_Drifted-5', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard5'] = ['Lizard_Drifted5', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard-10'] = ['Lizard_Drifted-10', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard10'] = ['Lizard_Drifted10', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard-15'] = ['Lizard_Drifted-15', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard15'] = ['Lizard_Drifted15', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard-20'] = ['Lizard_Drifted-20', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard20'] = ['Lizard_Drifted20', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard-25'] = ['Lizard_Drifted-25', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard25'] = ['Lizard_Drifted25', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard-30'] = ['Lizard_Drifted-30', 'Lizard', 49.961, -5.203]
        filenames_dict['Lizard30'] = ['Lizard_Drifted30', 'Lizard', 49.961, -5.203]
        filenames_dict['Longships-1'] = ['Longships_Drifted-1', 'Longships', 50.067, -5.735]
        filenames_dict['Longships1'] = ['Longships_Drifted1', 'Longships', 50.067, -5.735]
        filenames_dict['Longships-5'] = ['Longships_Drifted-5', 'Longships', 50.067, -5.735]
        filenames_dict['Longships5'] = ['Longships_Drifted5', 'Longships', 50.067, -5.735]
        filenames_dict['Longships-10'] = ['Longships_Drifted-10', 'Longships', 50.067, -5.735]
        filenames_dict['Longships10'] = ['Longships_Drifted10', 'Longships', 50.067, -5.735]
        filenames_dict['Longships-15'] = ['Longships_Drifted-15', 'Longships', 50.067, -5.735]
        filenames_dict['Longships15'] = ['Longships_Drifted15', 'Longships', 50.067, -5.735]
        filenames_dict['Longships-20'] = ['Longships_Drifted-20', 'Longships', 50.067, -5.735]
        filenames_dict['Longships20'] = ['Longships_Drifted20', 'Longships', 50.067, -5.735]
        filenames_dict['Longships-25'] = ['Longships_Drifted-25', 'Longships', 50.067, -5.735]
        filenames_dict['Longships25'] = ['Longships_Drifted25', 'Longships', 50.067, -5.735]
        filenames_dict['Longships-30'] = ['Longships_Drifted-30', 'Longships', 50.067, -5.735]
        filenames_dict['Longships30'] = ['Longships_Drifted30', 'Longships', 50.067, -5.735]
        filenames_dict['Trevose-1'] = ['Trevose_Drifted-1', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose1'] = ['Trevose_Drifted1', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose-5'] = ['Trevose_Drifted-5', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose5'] = ['Trevose_Drifted5', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose-10'] = ['Trevose_Drifted-10', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose10'] = ['Trevose_Drifted10', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose-15'] = ['Trevose_Drifted-15', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose15'] = ['Trevose_Drifted15', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose-20'] = ['Trevose_Drifted-20', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose20'] = ['Trevose_Drifted20', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose-25'] = ['Trevose_Drifted-25', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose25'] = ['Trevose_Drifted25', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose-30'] = ['Trevose_Drifted-30', 'Trevose', 50.535, -5.034]
        filenames_dict['Trevose30'] = ['Trevose_Drifted30', 'Trevose', 50.535, -5.034]
        filenames_dict['WolfRock-1'] = ['WolfRock_Drifted-1', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock1'] = ['WolfRock_Drifted1', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock-5'] = ['WolfRock_Drifted-5', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock5'] = ['WolfRock_Drifted5', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock-10'] = ['WolfRock_Drifted-10', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock10'] = ['WolfRock_Drifted10', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock-15'] = ['WolfRock_Drifted-15', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock15'] = ['WolfRock_Drifted15', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock-20'] = ['WolfRock_Drifted-20', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock20'] = ['WolfRock_Drifted20', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock-25'] = ['WolfRock_Drifted-25', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock25'] = ['WolfRock_Drifted25', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock-30'] = ['WolfRock_Drifted-30', 'WolfRock', 49.935, -5.801]
        filenames_dict['WolfRock30'] = ['WolfRock_Drifted30', 'WolfRock', 49.935, -5.801]
else:
    filenames_dict['Bishop'] = ['BishopRock', 'BishopRock', 49.868, -6.435]
    # filenames_dict['BullPost'] = ['BullPointPost', 'BullPointPost', 51.2, -4.202]
    # filenames_dict['BullPre'] = ['BullPointPre', 'BullPointPre', 51.2, -4.202]
    filenames_dict['Eddy'] = ['Eddystone', 'Eddystone', 50.184, -4.268]
    filenames_dict['Godrevy'] = ['Godrevy', 'Godrevy', 50.235, -5.401]
    filenames_dict['Lizard'] = ['Lizard', 'Lizard', 49.961, -5.203]
    filenames_dict['Longships'] = ['Longships', 'Longships', 50.067, -5.735]
    filenames_dict['Trevose'] = ['Trevose', 'Trevose', 50.535, -5.034]
    filenames_dict['WolfRock'] = ['WolfRock', 'WolfRock', 49.935, -5.801]

INTERPOLATION_POINTS = 5  # Number of points to interpolate within an hourly timeframe
MULTIPLIER = 60 / (INTERPOLATION_POINTS + 1)  # converts dataframe indices to be within range of 0-60 minutes


# Function to insert row in the dataframe. Source:
# https://www.geeksforgeeks.org/insert-row-at-given-position-in-pandas-dataframe/
def insert_row(row_number, df, row_value):
    start_upper = 0  # Starting value of upper half
    end_upper = row_number  # End value of upper half
    start_lower = row_number  # Start value of lower half
    end_lower = df.shape[0]  # End value of lower half
    upper_half = [*range(start_upper, end_upper, 1)]  # Create a list of upper_half index
    lower_half = [*range(start_lower, end_lower, 1)]  # Create a list of lower_half index
    lower_half = [x.__add__(1) for x in lower_half]  # Increment the value of lower half by 1
    index_ = upper_half + lower_half  # Combine the two lists
    df.index = index_  # Update the index of the dataframe
    df.loc[row_number] = row_value  # Insert a row at the end
    df = df.sort_index()  # Sort the index labels

    return df


# Finds the closest value of a target number from a source of numbers
# Adapted from: https://stackoverflow.com/questions/30112202/how-do-i-find-the-closest-values-in-a-pandas-series-to
# -an-input-number
def find_closest_values(target, source, k_matches=1):
    k_above = source[source >= target].nsmallest(k_matches)
    k_below = source[source < target].nlargest(k_matches)

    if len(k_below) == 0:
        k_below = k_above

    if np.absolute(target - k_above.values) < np.absolute(target - k_below.values):
        return k_above.values
    else:
        return k_below.values


# Identifies the upper and lower bound of an event within an hourly range. E.g., if event time is 12:14, then the
# upper bound is 12:00 and the lower bound is 13:00.
#
# Returns the climate measurements for the upper and lower bounds.
def get_bounds(station, climate, index):
    # Match the date in the station dataframe to the respected entry in the climate dataframe
    current_date = climate.loc[pd.to_datetime(climate.Date).dt.date == station.Date.dt.date[index]]
    # Find the upper bound of event time, e.g. if event is at 12:14, then the upper bound is 12:00
    upper = current_date.loc[
        pd.to_datetime(current_date.Date).dt.time == datetime.time(station.Date.dt.time[index].hour, 00, 00)]
    # Find the lower bound, e.g. if event is at 12:14, then the lower bound is 13:00. If event time is after 23:00, then
    # the lower bound is set to the following day's date at 00:00 hour (else part of the if-else statement)
    if station.Date.dt.time[index].hour + 1 <= 23:
        lower = current_date.loc[
            pd.to_datetime(current_date.Date).dt.time == datetime.time(station.Date.dt.time[index].hour + 1, 00, 00)]
    else:
        current_date = climate.loc[pd.to_datetime(climate.Date).dt.date == station.Date.dt.date[index + 1]]
        lower = current_date.loc[
            pd.to_datetime(current_date.Date).dt.time == datetime.time(00, 00, 00)]

    return [upper, lower]


# Interpolates climate values between an upper and lower bound of time.
# Inputs: the upper and lower bounds (in terms of time) that contain the climate values, and the number of
# elements/points to be created between the upper and lower bounds, which will be then interpolated.
def interpolate_values(upper, lower, elements):
    to_interpolate = pd.merge(upper, lower, how="outer")  # merge upper and lower entries into a single dataframe
    to_interpolate = to_interpolate.drop(['Date', 'Latitude', 'Longitude'], axis=1)  # delete columns that do not need
    # interpolation

    row_value = [np.nan] * len(to_interpolate.columns)  # Create NaN values that will then be interpolated

    for j in range(elements):
        to_interpolate = insert_row(j + 1, to_interpolate, row_value)  # Place those NaN values between upper and lower
        # bound entries

    # interpolate values (linear interpolation) and return dataframe
    return to_interpolate.interpolate(method='linear', limit_direction='forward', axis=0)


def get_solar_data(latitude, longitude):
    tz = 'UTC'  # Timezone
    loc = location.Location(latitude, longitude, tz=tz)

    # Define time range
    start = pd.Timestamp('2017-01-01 00:00:00', tz=tz)
    end = pd.Timestamp('2021-12-31 23:59:00', tz=tz)
    times = pd.date_range(start, end, freq='1min')

    # Calculate solar position
    solar_position = pvlib.solarposition.get_solarposition(times, latitude, longitude)

    # Calculate clear-sky GHI, DNI, and DHI
    clearsky = loc.get_clearsky(times, model='ineichen', solar_position=solar_position)

    # Combine the solar position and irradiance data
    combined = pd.concat([solar_position, clearsky], axis=1)

    # Reset the index
    combined = combined.reset_index()

    # Rename the new column
    combined = combined.rename(columns={'index': 'Date'})

    return combined


# Process is as follows:
# 1. Read csv files for telemetry station and climate
# 2. Rename columns to attain uniformity and sort data by date
# 3. For each entry in the station, identify the upper and lower bound of an event within an hourly range. E.g.,
# if event time is 12:14, then the upper bound is 12:00 and the lower bound is 13:00. Obtain the climate measurements
# for the upper and lower bounds.
# 4. Interpolate the values between bounds in a given granularity. E.g. if granularity is 10 minutes, then there's five
# entries between upper and lower bound that are being interpolated (linear interpolation).
# 5. Identify closest interpolated entry to event time. E.g. if event time is 12:14, there's interpolated values
# for 12:10 and 12:20. The closest one is the entry with climate values at 12:10.
# 6. Repeat process from Step 3 for each element/event from the telemetry station csv file.
# 7. Merge these interpolated climate values with the telemetry station data, so that we have one single dataframe
# holding both.
if __name__ == '__main__':
    for value in filenames_dict.values():
        # Step 1. Read csv files for telemetry station and climate
        station = pd.read_csv(station_filename + value[0] + '.csv')
        climate = pd.read_csv(climate_filename + value[1] + '.csv')

        # station2 = pd.read_csv(station_filename + value[0] + '_I.csv')

        print('=============' + value[0] + '==============')

        # Step 2. Rename columns to attain uniformity and sort data by date
        station.columns = ['Tagname', 'Date', 'Sunangle', 'Value']
        climate.columns = ['Date', 'Latitude', 'Longitude', 'Temp2m', 'Dewpoint2m', 'Pressure', 'Precipitation', 'GHI',
                           'DHI', 'BNI']

        # in this particular case the daytime in the provided file had different format
        if nlb is True and drifted is False:
            station['Date'] = pd.to_datetime(station['Date'],
                                             format="%Y-%m-%d %H:%M:%S")  # convert time column to datetime type
        else:
            station['Date'] = pd.to_datetime(station['Date'],
                                             format="%Y-%m-%dT%H:%M:%S%z")  # convert time column to datetime type
        station = station.sort_values(by="Date")  # sort values by time
        climate['Date'] = pd.to_datetime(climate['Date'], format="%Y-%m-%dT%H:%M:%S")
        climate = climate.sort_values(by='Date')

        # In Phase 3, I'm also obtaining solar data to add more features
        solar_data = get_solar_data(value[2], value[3])
        solar_data['Date'] = pd.to_datetime(solar_data['Date'], format="%Y-%m-%dT%H:%M:%S%z")

        list = []
        for i in range(len(station)):
            # Step 3. For each entry in the station, identify the upper and lower bound of an event within an hourly
            # range. E.g., if event time is 12:14, then the upper bound is 12:00 and the lower bound is 13:00. Obtain
            # the climate measurements for the upper and lower bounds.
            [start_time, end_time] = get_bounds(station, climate, i)

            # 4. Interpolate the values between bounds in a given granularity. E.g. if granularity is 10 minutes, then
            # there's five entries between upper and lower bound that are being interpolated (linear interpolation).
            interpolated = interpolate_values(start_time, end_time, INTERPOLATION_POINTS)

            # 5. Identify closest interpolated entry to event time. E.g. if event time is 12:14, there's interpolated
            # values for 12:10 and 12:20. The closest one is the entry with climate values at 12:10.
            target = station.Date.dt.time[i].minute
            source = pd.Series(interpolated.index * MULTIPLIER)

            closest_index = find_closest_values(target, source, k_matches=1)[
                                0] / MULTIPLIER  # divide by multiplier to convert back to dataframe indices

            # Save the interpolated values into a list
            list.append(interpolated.loc[closest_index])

        # 6. Merge these interpolated climate values with the telemetry station data, so that we have one single
        # dataframe holding both.
        final = pd.DataFrame(list)  # convert list to dataframe
        complete = pd.concat([station.reset_index(drop=True), final.reset_index(drop=True)], axis=1)  # merge them
        complete = complete[
            ['Tagname', 'Date', 'Sunangle', 'Temp2m', 'Dewpoint2m', 'Pressure', 'Precipitation', 'GHI', 'DHI', 'BNI',
             'Value']]  # Re-arrange order to have target value in the last column

        # Reset the index (since merge_asof operates on columns, not indices)
        complete.reset_index(inplace=True)
        solar_data.reset_index(inplace=True)

        # # in this particular case the daytime in the provided file had different format
        if nlb is True and drifted is False:
            complete['Date'] = complete['Date'].dt.tz_localize('UTC')
        merged_df = pd.merge_asof(complete, solar_data, left_on='Date', right_on='Date', direction='nearest')

        merged_df = merged_df[
            ['index_x', 'Tagname', 'Date', 'Sunangle', 'Temp2m', 'Dewpoint2m', 'Pressure', 'Precipitation', 'GHI',
             'DHI', 'BNI', 'apparent_zenith', 'zenith', 'apparent_elevation', 'elevation', 'azimuth', 'equation_of_time', 'ghi',
             'dhi', 'dni', 'Value']].rename(columns={'index_x': 'index', 'GHI': 'GHI_N', 'DHI': 'DHI_N', 'BNI': 'BNI_N',
                                                     'ghi': 'ghi_M', 'dhi': 'dhi_M', 'dni': 'dni_M'})
        merged_df = merged_df.drop('index', axis=1)

        output_filename = value[0].replace('_', '') + '.csv'
        merged_df.to_csv(output_path + output_filename, index=False)
