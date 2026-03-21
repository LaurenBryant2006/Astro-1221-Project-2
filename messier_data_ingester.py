"""
MessierDataIngester
-------------------
Handles downloading, saving, and parsing the Messier catalog data.

Classes:
    MessierDataIngester

Methods:
    fetch_and_save():
        # Download Messier catalog from API and save as CSV
        pass
    parse_messier_objects_to_dict():
        # Read CSV and return list of dictionaries for each object
        pass

Data Structures:
    - JSON/CSV byte stream from API
    - List[dict]: Each dict represents a celestial object
"""

class MessierDataIngester:
    """Class to ingest Messier catalog data from an API and parse it for analysis."""
    import requests
    import csv
    import os
    from constants import CSV_URL, CSV_FILENAME, LOG_FILENAME

    def fetch_and_save(self, url=CSV_URL, filename=CSV_FILENAME):
        """
        Download Messier catalog from a public CSV URL and save to local CSV file.
        Args:
            url (str): URL to the Messier catalog CSV.
            filename (str): Local filename to save CSV.
        Returns:
            str: Path to saved CSV file.
        """
        response = self.requests.get(url)
        response.raise_for_status()
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename

    def parse_messier_objects_to_dict(self, filename=CSV_FILENAME):
        """
        Read CSV and return list of dictionaries for each Messier object.
        Skips comment lines and handles non-UTF-8 encoding.
        Args:
            filename (str): Path to CSV file.
        Returns:
            list[dict]: List of Messier object dictionaries.
        """
        import csv
        objects = []
        with open(filename, "r", encoding="latin1") as f:
            # Skip comment lines (start with ';')
            lines = [line for line in f if not line.strip().startswith(';') and line.strip()]
        # Use csv.DictReader on filtered lines
        reader = csv.DictReader(lines)
        for row in reader:
            objects.append(dict(row))
        return objects

    def log_objects_to_txt(self, objects, log_filename=LOG_FILENAME):
        """
        Log Messier objects to a text file for validation.
        Args:
            objects (list[dict]): List of Messier object dictionaries.
            log_filename (str): Path to log file.
        """
        with open(log_filename, "w", encoding="utf-8") as f:
            f.write("Logging Objects: \n")
            for obj in objects:
                f.write(str(obj) + "\n")
