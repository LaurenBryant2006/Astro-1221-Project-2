import pandas as pd
import numpy as np
import logging
from constants import (
    MONTH_MAP, COLUMNS, DEFAULT_APERTURE_MM,
    RA_MIN_HOUR, RA_MAX_HOUR, MONTHS_IN_YEAR,
    MAG_BASE_CONSTANT, MAG_LOG_COEFFICIENT, NAKED_EYE_BRIGHT_URBAN_VISIBILITY_THRESHOLD,
    NAKED_EYE_SUBURBAN_RURAL_DARK_VISIBILITY_THRESHOLD, BINOCULAR_VISIBILITY_THRESHOLD,
    RA_TO_MONTH_BUCKET_SIZE
)

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class AstroAnalyticsEngine:
    def __init__(self, data_list):
        self.df = pd.DataFrame(data_list)
        self.columns = COLUMNS
        self.default_aperture = DEFAULT_APERTURE_MM

    def clean_data(self):
        """Clean and type-cast data. Done for RA string parsing."""
        mag_col = self.columns['MAGNITUDE']
        ra_col = self.columns['RA']
        type_col = self.columns['TYPE']

        if mag_col in self.df.columns:
            self.df[mag_col] = pd.to_numeric(self.df[mag_col], errors='coerce')
        
        # The data from the CSV we download can vary a bit, but follows the format of "5h 34.5m" with an hour and minute to the decimal.
        # This doesn't translate well with just basic type conversion, so we parse to decimal BEFORE any numeric coercion to preserve '5h 34m'
        if ra_col in self.df.columns:
            self.df['RA_Decimal'] = self.df[ra_col].apply(self.parse_ra_to_decimal)
            self.df['BestViewingMonths'] = self.df[ra_col].apply(self.ra_to_month)
            logger.info(f"PAYLOAD_CLEANSE: Processed RA into decimals. Samples: {self.df['RA_Decimal'].head(2).tolist()}")

        if type_col in self.df.columns:
            self.df[type_col] = pd.Categorical(self.df[type_col])

        self.df.fillna(np.nan, inplace=True)

    def parse_ra_to_decimal(self, ra_value):
        """Converts RA strings (e.g., '5h 34.5m') to a float."""
        if pd.isna(ra_value) or str(ra_value).lower() == 'unknown':
            return np.nan
        try:
            ra_substrings = str(ra_value).lower().replace('h', ' ').replace('m', ' ').split()
            hours = float(ra_substrings[0])
            minutes = float(ra_substrings[1]) if len(ra_substrings) >= 2 else 0.0
            return hours + (minutes / 60.0)
        except (ValueError, IndexError):
            return np.nan

    def ra_to_month(self, ra):
        """Maps RA decimal to its corresponding month."""
        ra_decimal = self.parse_ra_to_decimal(ra)
        if pd.isna(ra_decimal):
            return "Unknown"
            
        month_idx = int(ra_decimal / RA_TO_MONTH_BUCKET_SIZE) % MONTHS_IN_YEAR
        return MONTH_MAP.get(month_idx, "Unknown")

    def aperture_mag_limit(self, aperture_mm):
        """Standard formula: 2.7 + 5 * log10(D): https://www.rocketmime.com/astronomy/Telescope/MagnitudeGain.html"""
        if aperture_mm <= 0:
            return 0
        return MAG_BASE_CONSTANT + MAG_LOG_COEFFICIENT * np.log10(aperture_mm)

    def filter_by_aperture_and_brightness(self, aperture_mm=None):
        """Filters objects and assigns ratings."""
        target_ap = aperture_mm if aperture_mm is not None else self.default_aperture
        limit = self.aperture_mag_limit(target_ap)
        mag_col = self.columns['MAGNITUDE']

        logger.info(f"CALCULATING_VISIBILITY: Aperture {target_ap}mm | Limit {limit:.2f}")

        # Filter out anything physically impossible to see
        visible_mask = self.df[mag_col] <= limit
        filtered_df = self.df[visible_mask].copy()
        
        # Pass the 'limit' to the rating helper for dynamic calculation using a nifty lambda function!
        filtered_df['VisibilityRating'] = filtered_df[mag_col].apply(
            lambda m: self._assign_dynamic_rating(m, limit)
        )
        
        return filtered_df.sort_values(by=mag_col)

    def _assign_dynamic_rating(self, mag, mag_limit):
        """
        Assigns visibility advice based on scientific hardware thresholds.
        Reflects the 'Minimum Tool' required for successful observation!
        """
        if pd.isna(mag):
            return "Unknown Visibility"

        # 1. Naked Eye Thresholds (Urban vs Rural)
        if mag <= NAKED_EYE_BRIGHT_URBAN_VISIBILITY_THRESHOLD:
            return "Naked Eye: Visible even from bright urban areas."
        if mag <= NAKED_EYE_SUBURBAN_RURAL_DARK_VISIBILITY_THRESHOLD:
            return "Naked Eye: Visible from suburban/rural dark skies."

        # 2. Binocular Threshold (Standard 50mm aperture)
        if mag <= BINOCULAR_VISIBILITY_THRESHOLD:
            return "Binoculars: Bright in suburbs; small telescope needed in cities."

        # 3. Telescope Thresholds (Using the calculated limit of the user's specific scope)
        # If the object is within 0.5 of the hardware limit, it's 'Challenging'
        if mag > mag_limit:
            return f"Impossible: Exceeds scope limit ({mag_limit:.1f}). Needs larger aperture."
        
        if mag > (mag_limit - 1.0):
            return "Challenging: Faint/Diffuse; requires averted vision and dark skies."
        
        # 4. Standard Telescope Viewing
        return "Telescope: Clearly visible with your current aperture."

    def get_seasonal_targets(self, season_name):
        ra_min, ra_max = SEASON_RA[season_name]
        
        if ra_min > ra_max:
            return self.df[(self.df['RA_Decimal'] >= ra_min) | (self.df['RA_Decimal'] < ra_max)]
        
        return self.df[(self.df['RA_Decimal'] >= ra_min) & (self.df['RA_Decimal'] < ra_max)]

    def log_filtered_objects(self, df, log_filename): #Helpful for debugging during implementation, but also helpful to make sure nothing broke with future implementations. 
        with open(log_filename, "w", encoding="utf-8") as f:
            f.write(f"=== Visibility Report | Count: {len(df)} ===\n\n")
            f.write(df.to_string(index=False))
        logger.info(f"LOG_SUCCESS: Results written to {log_filename}")