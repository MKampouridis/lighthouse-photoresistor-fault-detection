#!/bin/bash

# Run with the raw data
./process_telemetry_data.py --input=BishopRock.xlsx --latitude=49.867285 --longitude=-6.434557
./process_telemetry_data.py --input=Eddystone.xlsx --latitude=50.168072 --longitude=-4.25156
./process_telemetry_data.py --input=Lizard.xlsx --latitude=49.95102 --longitude=-5.200213
./process_telemetry_data.py --input=WolfRock.xlsx --latitude=49.934532 --longitude=-5.800917
./process_telemetry_data.py --input=BishopRock.xlsx --latitude=49.867285 --longitude=-6.434557
./process_telemetry_data.py --input=Longships.xlsx --latitude=50.066687 --longitude=-5.734687
./process_telemetry_data.py --input=Godrevy.xlsx --latitude=50.234248 --longitude=-5.400025
./process_telemetry_data.py --input=Trevose.xlsx --latitude=50.534923 --longitude=-5.033522
#./process_telemetry_data.py --input=BullPointPre.xlsx --latitude=51.199100 --longitude=-4.201200
#./process_telemetry_data.py --input=BullPointPost.xlsx --latitude=51.199100 --longitude=-4.201200

# Run and clean the raw data
./process_telemetry_data.py --input=BishopRock.xlsx --latitude=49.867285 --longitude=-6.434557 --clean
./process_telemetry_data.py --input=Eddystone.xlsx --latitude=50.168072 --longitude=-4.25156 --clean
./process_telemetry_data.py --input=Lizard.xlsx --latitude=49.95102 --longitude=-5.200213 --clean
./process_telemetry_data.py --input=WolfRock.xlsx --latitude=49.934532 --longitude=-5.800917 --clean
./process_telemetry_data.py --input=BishopRock.xlsx --latitude=49.867285 --longitude=-6.434557 --clean
./process_telemetry_data.py --input=Longships.xlsx --latitude=50.066687 --longitude=-5.734687 --clean
./process_telemetry_data.py --input=Godrevy.xlsx --latitude=50.234248 --longitude=-5.400025 --clean
./process_telemetry_data.py --input=Trevose.xlsx --latitude=50.534923 --longitude=-5.033522 --clean
#./process_telemetry_data.py --input=BullPointPre.xlsx --latitude=51.199100 --longitude=-4.201200 --clean
#./process_telemetry_data.py --input=BullPointPost.xlsx --latitude=51.199100 --longitude=-4.201200 --clean