import requests
import re
import time

def clean_founder_name(name):
    name = re.split(r'\s+(?:was|were)\s+', name)[0]
    name = re.sub(r'\b(Mr\.|Mrs\.|Ms\.|Dr\.|Sr\.|Jr\.|Prof\.|Sir|Lady|Lord)\s*', '', name)
    name = name.rstrip(',.')
    name = re.sub(r'\s*\([^)]*\)', '', name)
    name = name.replace(',', '')
    return name.strip()

def get_company_aliases(company_name):
    aliases = [company_name]
    aliases.append(re.sub(r'\s+(Inc\.?|Corp\.?|Ltd\.?|LLC|Limited|Corporation)$', '', company_name, flags=re.IGNORECASE))
    if '&' not in company_name:
        aliases.append(company_name.replace(' and ', ' & '))
    return list(set(aliases))

def make_request_with_retries(url, params, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            if attempt == max_retries - 1:
                return None
            time.sleep(2 ** attempt)

def scrape_wikipedia(company_name):
    aliases = get_company_aliases(company_name)
    
    for alias in aliases:
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": alias
        }
        
        search_data = make_request_with_retries(search_url, search_params)
        if not search_data or not search_data["query"]["search"]:
            continue
        
        page_title = search_data["query"]["search"][0]["title"]
        content_url = "https://en.wikipedia.org/w/api.php"
        content_params = {
            "action": "query",
            "format": "json",
            "titles": page_title,
            "prop": "extracts",
            "explaintext": True,
        }
        
        content_data = make_request_with_retries(content_url, content_params)
        if not content_data:
            continue
        
        page = next(iter(content_data["query"]["pages"].values()))
        
        if "extract" in page:
            extract = page["extract"]
            
            founder_patterns = [
                r"founded by ([\w\s,\.]+(?:and|&)?\s?[\w\s\.]+)",
                r"([\w\s,\.]+(?:and|&)?\s?[\w\s\.]+) founded",
                r"founder(?:s)? (?:is|are|was|were) ([\w\s,\.]+(?:and|&)?\s?[\w\s\.]+)",
                r"([\w\s,\.]+(?:and|&)?\s?[\w\s\.]+) is the founder",
                r"established by ([\w\s,\.]+(?:and|&)?\s?[\w\s\.]+)",
                r"([\w\s,\.]+(?:and|&)?\s?[\w\s\.]+) established",
                r"created by ([\w\s,\.]+(?:and|&)?\s?[\w\s\.]+)",
                r"([\w\s,\.]+(?:and|&)?\s?[\w\s\.]+) created",
                r"started by ([\w\s,\.]+(?:and|&)?\s?[\w\s\.]+)",
                r"([\w\s,\.]+(?:and|&)?\s?[\w\s\.]+) started",
                r"co-founder(?:s)? (?:is|are|was|were) ([\w\s,\.]+(?:and|&)?\s?[\w\s\.]+)",
            ]
            
            founders = []
            for pattern in founder_patterns:
                matches = re.finditer(pattern, extract, re.IGNORECASE)
                for match in matches:
                    found = match.group(1)
                    for founder in re.split(r',|\sand\s|&', found):
                        clean_name = clean_founder_name(founder)
                        if clean_name and len(clean_name.split()) > 1:
                            founders.append(clean_name)
            
            founders = list(dict.fromkeys(founders))
            founder_string = ", ".join(founders) if founders else "Not found"
            
            return {"company": company_name, "founder": founder_string}

    return {"company": company_name, "founder": "Not found"}