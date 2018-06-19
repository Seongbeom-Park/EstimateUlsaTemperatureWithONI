# EstimateUlsanTemperatureWithONI
CSE611 Weather machine learning project

Estimate Ulsan monthly average temperature with history records and Oceanic Nino Index (ONI).
The result shows that Ulsan affected by El Nino.

## dataset
ASOS of Ulsan
ONI (ONI_v5.csv)
	http://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php

## Run scripts
$ python scripts/asdf.py Meteorological_Data/ASOS.Ulsan.6hr.1980-2017.csv Meteorological_Data/ONI_v5_parsed.csv packing_F1981_C2015_L2017_100_20_ONI
