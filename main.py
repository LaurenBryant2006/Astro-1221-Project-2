"""
main.py
-------
Entry point for the Messier Object Tourist Guide app.

- Loads data using MessierDataIngester
- Initializes analytics engine and user profile
- Optionally launches Streamlit UI
"""

from messier_data_ingester import MessierDataIngester
# from astro_analytics_engine import AstroAnalyticsEngine
# from user_profile import UserProfile
# from astro_llm_tools import AstroLLMTools
# from astro_streamlit_ui import AstroStreamlitUI

def main():
    """Main entry point for the app."""
    # 1. Ingest Messier data
    from constants import CSV_FILENAME, LOG_FILENAME
    ingester = MessierDataIngester()
    csv_path = ingester.fetch_and_save()
    objects = ingester.parse_messier_objects_to_dict(csv_path)
    ingester.log_objects_to_txt(objects)
    print(f"Downloaded and parsed {len(objects)} Messier objects. Logged to {LOG_FILENAME}.")

    
    # 2. Initialize analytics engine (to be implemented)
    # 3. Load or create user profile (to be implemented)
    # 4. (Optional) Launch Streamlit UI (to be implemented)

if __name__ == "__main__":
    main()
