import os
import sys
import json
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username="drew-1618"):
    # Target the public contributions endpoint GitHub uses for profile tabs
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
    
    # GitHub renders the graph using <td class="ContributionCalendar-day"> blocks
    days = soup.find_all('td', class_='ContributionCalendar-day')
    
    if not days:
        print("Error: Could not parse contribution cells. GitHub's HTML structure might have changed.")
        return False
        
    contributions_data = []
    total_contributions = 0
    
    for day in days:
        date = day.get('data-date')
        level = day.get('data-level', '0')
        
        # New robust attribute parsing for counts
        count = 0
        desc = day.get_text().strip().lower() # Check text inside the element if present
        
        # If text isn't directly inside the <td>, look at its data attributes
        # GitHub often uses data-count or embedded structural text strings
        if not desc and day.get('id'):
            tool_tip = soup.find('tool-tip', for_=day.get('id'))
            if tool_tip:
                desc = tool_tip.get_text().strip().lower()
                
        if desc and "contribution" in desc and not desc.startswith("no"):
            try:
                count = int(desc.split()[0].replace(',', ''))
            except (ValueError, IndexError):
                count = 0

        if date:
            total_contributions += count
            contributions_data.append({
                "date": date,
                "count": count,
                "level": int(level)
            })
    
    # Package into clean JSON payload format
    output_payload = {
        "username": username,
        "total_past_year": total_contributions,
        "days": contributions_data
    }
    
    # Ensure the data storage directory exists
    os.makedirs("data", exist_ok=True)
    
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)
        
    print(f"Success! Cached {len(contributions_data)} days of data into data/contributions.json")
    print(f"Total contributions found: {total_contributions}")
    return True

if __name__ == "__main__":
    target_user = "drew-1618" 
    fetch_contributions(target_user)
