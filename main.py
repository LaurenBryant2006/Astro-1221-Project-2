"""
Entry point for the Messier Object Tourist Guide app.
"""

from messier_data_ingester import MessierDataIngester
from constants import CSV_FILENAME, LOG_FILENAME, DEFAULT_APERTURE_MM
from astro_analytics_engine import AstroAnalyticsEngine
# from user_profile import UserProfile
# from astro_llm_tools import AstroLLMTools
# from astro_streamlit_ui import AstroStreamlitUI

def main():
    """Main entry point for the app."""
    # 1. Ingest Messier data
    ingester = MessierDataIngester()
    csv_path = ingester.fetch_and_save()
    objects = ingester.parse_messier_objects_to_dict(csv_path)
    ingester.log_objects_to_txt(objects)
    print(f"Downloaded and parsed {len(objects)} Messier objects. Logged to {LOG_FILENAME}.")

    # 2. Initialize analytics engine
    analytics = AstroAnalyticsEngine(objects)
    analytics.clean_data()

    # Test with default aperture
    filtered_df_default = analytics.filter_by_aperture_and_brightness()
    analytics.log_filtered_objects(
        filtered_df_default, 
        log_filename="filtered_objects_default_aperture.txt"
    )
    print(f"Default Aperture ({DEFAULT_APERTURE_MM}mm): {len(filtered_df_default)} objects found.")

    # Test with custom aperture, just check the created file and associated logs
    custom_aperture = 10
    filtered_df_custom = analytics.filter_by_aperture_and_brightness(custom_aperture)
    analytics.log_filtered_objects(
        filtered_df_custom, 
        log_filename="filtered_objects_custom_aperture.txt"
    )
    print(f"Custom Aperture ({custom_aperture}mm): {len(filtered_df_custom)} objects found.")

    # 3. Load or create user profile (to be implemented)
    # 4. Launch the LLM class to be used by Streamlit UI (to be implemented)
    # 5. Launch Streamlit UI (to be implemented)

if __name__ == "__main__":
    main()
