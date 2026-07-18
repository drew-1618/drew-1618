import os
import sys
import json
import re
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username="drew-1618"):
    url = f"https://github.com/users/{username}/contributions"
    print(f"Fetching contribution data from: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Failed to fetch data from GitHub (Status Code: {response.status_code})")
        return False
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. Map all tooltip elements by their target cell ID
    tooltip_map = {}
    tooltips = soup.find_all('tool-tip')
    for tt in tooltips:
        target_id = tt.get('for')
        if target_id:
            tooltip_map[target_id] = tt.get_text(" ", strip=True).lower()
            
    # 2. Grab the grid day cells
    days = soup.find_all('td', class_='ContributionCalendar-day')
    
    if not days:
        print("Error: Could not parse contribution cells. GitHub's HTML structure might have changed.")
        return False
        
    contributions_data = []
    total_contributions = 0
    
    for day in days:
        date = day.get('data-date')
        level = int(day.get('data-level', '0'))
        cell_id = day.get('id')
        
        # Check standard text, fallback to mapped tooltip text, or read explicit count attributes
        cell_text = day.get_text(" ", strip=True).lower()
        if not cell_text and cell_id in tooltip_map:
            cell_text = tooltip_map[cell_id]
            
        count = 0
        
        # Method A: Parse via matching mapped text strings
        if cell_text and "contribution" in cell_text:
            if "no contribution" not in cell_text:
                match = re.search(r'([\d,]+)\s+contribution', cell_text)
                if match:
                    try:
                        count = int(match.group(1).replace(',', ''))
                    except ValueError:
                        count = 0
        
        # Method B: Direct attribute scrape if standard attributes are injected
        elif day.get('data-count'):
            try:
                count = int(day.get('data-count'))
            except ValueError:
                pass
                
        # Method C: Fail-Safe Level Density Multiplier 
        if count == 0 and level > 0:
            level_multipliers = {1: 1, 2: 3, 3: 6, 4: 11}
            count = level_multipliers.get(level, 1)

        if date:
            total_contributions += count
            contributions_data.append({
                "date": date,
                "count": count,
                "level": level
            })
            
    output_payload = {
        "username": username,
        "total_past_year": total_contributions,
        "days": contributions_data
    }
    
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)
        
    print(f"Success! Cached {len(contributions_data)} days of data into data/contributions.json")
    print(f"Total contributions found: {total_contributions}")
    return True

if __name__ == "__main__":
    target_user = "drew-1618" 
    fetch_contributions(target_user)