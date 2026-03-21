# RA ranges best viewed at midnight during these seasons -> See this source https://in-the-sky.org/data/ra_season.php?town=4509177
# Taking Fall as an example: The source states that the RAs of 0-6 are best for Sep to Oct to Nov, so we set that range there
SEASON_RA = {
    'Spring': (12, 16),
    'Summer': (16, 0), # Wraps from 16 -> 24 -> 0
    'Fall':   (0, 6),
    'Winter': (6, 12)
}

# Mapping of RA hour to best viewing month. Again, grabbed from the above source
MONTH_MAP = {
    0: "September",
    1: "October",
    2: "November",
    3: "December",
    4: "January",
    5: "February",
    6: "March",
    7: "April",
    8: "May",
    9: "June",
    10: "July",
    11: "August"
}
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
COLUMNS = {
    'MESSIER': 'Name',
    'NGC': 'NGC',
    'CONSTELLATION': 'Constellation',
    'TYPE': 'Class',
    'RA': 'Right ascension',
    'DEC': 'Declination',
    'MAGNITUDE': 'Magnitude',
    'DIAMETER': 'Angular size',
    'BURNHAM': 'Burnham',
    'REMARKS': 'Remarks',
}

# Default telescope aperture (mm)
DEFAULT_APERTURE_MM = 114
