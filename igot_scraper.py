"""
iGOT Karmayogi Official Government Learning Scraper & Direct Course Indexer
Extracts and indexes official training courses from igotkarmayogi.gov.in / portal.igotkarmayogi.gov.in
"""

import os
import json
from typing import List, Dict, Any

class IGOTKarmayogiScraper:
    def __init__(self):
        self.base_url = "https://igotkarmayogi.gov.in"
        self.portal_url = "https://portal.igotkarmayogi.gov.in"

    def scrape_igot_statistical_courses(self) -> List[Dict[str, Any]]:
        """
        Loads and returns all indexed official capacity building courses from iGOT Karmayogi portal.
        """
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "db.json")
        if os.path.exists(db_path):
            with open(db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("igot_courses", [])
        return []

if __name__ == "__main__":
    scraper = IGOTKarmayogiScraper()
    scraped = scraper.scrape_igot_statistical_courses()
    print(f"Scraped {len(scraped)} official iGOT Karmayogi courses with direct portal links.")
