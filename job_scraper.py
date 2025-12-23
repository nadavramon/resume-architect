import requests
from bs4 import BeautifulSoup

def scrape_job_description(url):
    """
    Fetches text from a URL.
    
    Args:
        url (str): The URL of the job posting.
        
    Returns:
        str: The cleaned text from the website.
    """
    try:
        # 1. Define headers to look like a real browser (avoids immediate blocking)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 2. Request the page
        print(f"Fetching: {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        
        # Check if the request was successful (Status Code 200)
        if response.status_code != 200:
            print(f"Failed to retrieve page. Status code: {response.status_code}")
            return None
            
        # 3. Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 4. Extract text (strip out HTML tags)
        # We use separator=' ' to ensure words don't get stuck together
        text = soup.get_text(separator=' ')
        
        # 5. Basic cleanup (remove extra whitespace)
        clean_text = ' '.join(text.split())
        
        return clean_text
        
    except Exception as e:
        print(f"Error scraping URL: {e}")
        return None

# --- TEST BLOCK ---
if __name__ == "__main__":
    # Test with a real URL. 
    # (We use a Y Combinator job post because they are simple and don't block scrapers)
    test_url = "https://www.ycombinator.com/companies/stripe/jobs" 
    
    # OR you can paste a specific job link you want to try:
    # test_url = input("Paste a job URL: ")
    
    result = scrape_job_description(test_url)
    
    if result:
        print("\n--- JOB DESCRIPTION START ---")
        print(result[:1000]) # Print first 1000 characters only
        print("... (text truncated)")
        print("--- JOB DESCRIPTION END ---")