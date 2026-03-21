"""
constants.py
------------
Centralized constants for the project
"""

#CSV_URL = "https://raw.githubusercontent.com/masterhit/CeuProfundo/master/MessierObjects.csv"
CSV_URL = "https://raw.githubusercontent.com/7468696e6b/fourmilab-hplanet/master/Messier.csv"
CSV_FILENAME = "messier_catalog.csv"
LOG_FILENAME = "messier_objects_log.txt"

# Column names for Messier catalog CSV
# COLUMNS = {
# 	'MAGNITUDE': 'Magnitude',
# 	'RA': 'RA',
# 	'TYPE': 'Type',
# 	'DIAMETER': 'Diameter',
# }

COLUMNS = {
    'MESSIER': 'Messier',
    'NGC': 'NGC',
    'CONSTELLATION': 'Constellation',
    'TYPE': 'Class',
    'RA': 'RA',
    'DEC': 'Dec',
    'MAGNITUDE': 'Mag',
    'DIAMETER': 'Diameter',
    'BURNHAM': 'Burnham',
    'REMARKS': 'Remarks',
}

# Default telescope aperture (mm)
DEFAULT_APERTURE_MM = 114
