#!/bin/bash

# Run with the raw data
./process_telemetry_data.py --input=North_Rona_Part2.xlsx,North_Rona_Part1.xlsx --latitude=59.389317 --longitude=-2.381500
./process_telemetry_data.py --input=Sumburgh_Head_Part2.xlsx,Sumburgh_Head_Part1.xlsx --latitude=59.853850 --longitude=-1.275250
./process_telemetry_data.py --input=Mousa_Part2.xlsx,Mousa_Part1.xlsx --latitude=59.997567 --longitude=-1.158433
./process_telemetry_data.py --input=Dunnet_Head_Part2.xlsx,Dunnet_Head_Part1.xlsx --latitude=58.671450 --longitude=-3.376567
./process_telemetry_data.py --input=Sule_Skerry_Part2.xlsx,Sule_Skerry_Part1.xlsx --latitude=59.085167 --longitude=-4.406617
./process_telemetry_data.py --input=North_Rona_Part2.xlsx,North_Rona_Part1.xlsx --latitude=59.121267 --longitude=-5.815033
./process_telemetry_data.py --input=North_Ronaldsay_Part2.xlsx,North_Ronaldsay_Part1.xlsx --latitude=59.389317 --longitude=-2.381500
./process_telemetry_data.py --input=Flotta_Grinds_Buoy_Part2.xlsx,Flotta_Grinds_Buoy_Part1.xlsx --latitude=58.849550 --longitude=-3.013050
./process_telemetry_data.py --input=Balta_Sound_Part2.xlsx,Balta_Sound_Part1.xlsx --latitude=60.740867 --longitude=-0.7946

# Run and clean the raw data
./process_telemetry_data.py --input=North_Rona_Part2.xlsx,North_Rona_Part1.xlsx --latitude=59.389317 --longitude=-2.381500 --clean
./process_telemetry_data.py --input=Sumburgh_Head_Part2.xlsx,Sumburgh_Head_Part1.xlsx --latitude=59.853850 --longitude=-1.275250 --clean
./process_telemetry_data.py --input=Mousa_Part2.xlsx,Mousa_Part1.xlsx --latitude=59.997567 --longitude=-1.158433 --clean
./process_telemetry_data.py --input=Dunnet_Head_Part2.xlsx,Dunnet_Head_Part1.xlsx --latitude=58.671450 --longitude=-3.376567 --clean
./process_telemetry_data.py --input=Sule_Skerry_Part2.xlsx,Sule_Skerry_Part1.xlsx --latitude=59.085167 --longitude=-4.406617 --clean
./process_telemetry_data.py --input=North_Rona_Part2.xlsx,North_Rona_Part1.xlsx --latitude=59.121267 --longitude=-5.815033 --clean
./process_telemetry_data.py --input=North_Ronaldsay_Part2.xlsx,North_Ronaldsay_Part1.xlsx --latitude=59.389317 --longitude=-2.381500 --clean
./process_telemetry_data.py --input=Flotta_Grinds_Buoy_Part2.xlsx,Flotta_Grinds_Buoy_Part1.xlsx --latitude=58.849550 --longitude=-3.013050 --clean
./process_telemetry_data.py --input=Balta_Sound_Part2.xlsx,Balta_Sound_Part1.xlsx --latitude=60.740867 --longitude=-0.7946 --clean

# Drifted
./process_telemetry_data_drifted.py --input=Mousa_Drifted1_Part2.xlsx,Mousa_Drifted1_Part1.xlsx --latitude=59.997567 --longitude=-1.158433
./process_telemetry_data_drifted.py --input=Mousa_Drifted5_Part2.xlsx,Mousa_Drifted5_Part1.xlsx --latitude=59.997567 --longitude=-1.158433
./process_telemetry_data_drifted.py --input=Mousa_Drifted10_Part2.xlsx,Mousa_Drifted10_Part1.xlsx --latitude=59.997567 --longitude=-1.158433
./process_telemetry_data_drifted.py --input=Mousa_Drifted15_Part2.xlsx,Mousa_Drifted15_Part1.xlsx --latitude=59.997567 --longitude=-1.158433
./process_telemetry_data_drifted.py --input=Mousa_Drifted20_Part2.xlsx,Mousa_Drifted20_Part1.xlsx --latitude=59.997567 --longitude=-1.158433
./process_telemetry_data_drifted.py --input=Mousa_Drifted25_Part2.xlsx,Mousa_Drifted25_Part1.xlsx --latitude=59.997567 --longitude=-1.158433
./process_telemetry_data_drifted.py --input=Mousa_Drifted30_Part2.xlsx,Mousa_Drifted30_Part1.xlsx --latitude=59.997567 --longitude=-1.158433

# Drifted Clean
./process_telemetry_data_drifted.py --input=Mousa_Drifted1_Part2.xlsx,Mousa_Drifted1_Part1.xlsx --latitude=59.997567 --longitude=-1.158433 --clean
./process_telemetry_data_drifted.py --input=Mousa_Drifted5_Part2.xlsx,Mousa_Drifted5_Part1.xlsx --latitude=59.997567 --longitude=-1.158433 --clean
./process_telemetry_data_drifted.py --input=Mousa_Drifted10_Part2.xlsx,Mousa_Drifted10_Part1.xlsx --latitude=59.997567 --longitude=-1.158433 --clean
./process_telemetry_data_drifted.py --input=Mousa_Drifted15_Part2.xlsx,Mousa_Drifted15_Part1.xlsx --latitude=59.997567 --longitude=-1.158433 --clean
./process_telemetry_data_drifted.py --input=Mousa_Drifted20_Part2.xlsx,Mousa_Drifted20_Part1.xlsx --latitude=59.997567 --longitude=-1.158433 --clean
./process_telemetry_data_drifted.py --input=Mousa_Drifted25_Part2.xlsx,Mousa_Drifted25_Part1.xlsx --latitude=59.997567 --longitude=-1.158433 --clean
./process_telemetry_data_drifted.py --input=Mousa_Drifted30_Part2.xlsx,Mousa_Drifted30_Part1.xlsx --latitude=59.997567 --longitude=-1.158433 --clean