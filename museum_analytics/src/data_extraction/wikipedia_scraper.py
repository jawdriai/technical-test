"""
Wikipedia scraper for museum data extraction.
Extracts museum information from the Wikipedia page listing most visited museums.
"""

import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WikipediaMuseumScraper:
    """Scraper for extracting museum data from Wikipedia."""
    
    def __init__(self):
        self.base_url = "https://en.wikipedia.org"
        self.museum_list_url = "https://en.wikipedia.org/wiki/List_of_most_visited_museums"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Museum Analytics Bot 1.0 (Educational Purpose)'
        })
    
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse Wikipedia page content."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_visitor_number(self, text: str) -> Optional[int]:
        """Extract visitor number from text, handling various formats."""
        if not text:
            return None
            
        # Remove common text patterns
        text = re.sub(r'\([^)]*\)', '', text)  # Remove parentheses content
        text = re.sub(r'\[[^\]]*\]', '', text)  # Remove brackets content
        
        # Look for numbers with million/billion indicators
        million_match = re.search(r'(\d+(?:\.\d+)?)\s*million', text.lower())
        if million_match:
            return int(float(million_match.group(1)) * 1_000_000)
        
        billion_match = re.search(r'(\d+(?:\.\d+)?)\s*billion', text.lower())
        if billion_match:
            return int(float(billion_match.group(1)) * 1_000_000_000)
        
        # Look for raw numbers (assuming they're in thousands or raw numbers)
        number_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)', text)
        if number_match:
            number_str = number_match.group(1).replace(',', '')
            number = float(number_str)
            # If number is less than 1000, assume it's in millions
            if number < 1000:
                return int(number * 1_000_000)
            return int(number)
        
        return None
    
    def extract_museum_data(self) -> List[Dict]:
        """Extract museum data from the Wikipedia page."""
        soup = self.get_page_content(self.museum_list_url)
        if not soup:
            return []
        
        museums = []
        
        # Find the main table containing museum data
        tables = soup.find_all('table', {'class': 'wikitable'})
        
        for table in tables:
            rows = table.find_all('tr')
            
            # Skip header row
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 3:  # Need at least museum name, city, and visitors
                    continue
                
                try:
                    # Extract museum name (usually first column)
                    museum_name_cell = cells[0]
                    museum_name = museum_name_cell.get_text(strip=True)
                    
                    # Extract city name (usually second column)
                    city_cell = cells[1]
                    city_name = city_cell.get_text(strip=True)
                    
                    # Extract visitor numbers (usually third column)
                    visitors_cell = cells[2]
                    visitors_text = visitors_cell.get_text(strip=True)
                    annual_visitors = self.extract_visitor_number(visitors_text)
                    
                    # Only include museums with more than 2,000,000 visitors
                    if annual_visitors and annual_visitors >= 2_000_000:
                        museum_data = {
                            'museum_name': museum_name,
                            'city': city_name,
                            'annual_visitors': annual_visitors,
                            'country': self._extract_country(city_cell),
                            'year': self._extract_year(visitors_cell)
                        }
                        museums.append(museum_data)
                        logger.info(f"Extracted: {museum_name} in {city_name} - {annual_visitors:,} visitors")
                
                except Exception as e:
                    logger.warning(f"Error processing row: {e}")
                    continue
        
        return museums
    
    def _extract_country(self, city_cell) -> Optional[str]:
        """Extract country information from city cell."""
        # Look for country links or text
        country_link = city_cell.find('a', title=True)
        if country_link:
            title = country_link.get('title', '')
            # Sometimes the country is in the title attribute
            if 'country' in title.lower() or len(title.split()) > 2:
                return title
        
        # Look for country text in parentheses
        text = city_cell.get_text()
        country_match = re.search(r'\(([^)]+)\)', text)
        if country_match:
            return country_match.group(1)
        
        return None
    
    def _extract_year(self, visitors_cell) -> Optional[int]:
        """Extract year information from visitors cell."""
        text = visitors_cell.get_text()
        year_match = re.search(r'(20\d{2})', text)
        if year_match:
            return int(year_match.group(1))
        return None
    
    def save_to_csv(self, museums: List[Dict], filename: str = "museum_data.csv"):
        """Save museum data to CSV file."""
        if not museums:
            logger.warning("No museum data to save")
            return
        
        df = pd.DataFrame(museums)
        df.to_csv(filename, index=False)
        logger.info(f"Saved {len(museums)} museums to {filename}")
        return df


def main():
    """Main function to run the scraper."""
    scraper = WikipediaMuseumScraper()
    museums = scraper.extract_museum_data()
    
    if museums:
        df = scraper.save_to_csv(museums, "museum_data.csv")
        print(f"Successfully extracted {len(museums)} museums")
        print("\nSample data:")
        print(df.head())
    else:
        print("No museum data extracted")


if __name__ == "__main__":
    main()