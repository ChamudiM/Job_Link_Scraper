import requests
import pandas as pd
import os

# Your Google Custom Search API key and Search Engine ID
API_KEY = "AIzaSyDjjikafdxh2L4pDeegJM9AdkvslXMiyP4"
SEARCH_ENGINE_ID = "e68878c7ed6b447c8"

# Function to search Google Custom Search API
def search_google(query, num_results=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": num_results
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

# Function to extract job title and link from the search results
def extract_results(data):
    results = []
    if "items" in data:
        for item in data["items"]:
            title = item.get("title")
            link = item.get("link")
            snippet = item.get("snippet")
            results.append([title, link, snippet])
    return results

# Function to save results to a CSV file on Desktop
def save_to_csv(results, filename="job_search_results.csv"):
    # Determine the desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, filename)
    
    # Create a DataFrame from the results
    df = pd.DataFrame(results, columns=["Job Title", "Link", "Snippet"])
    # Save to CSV
    df.to_csv(file_path, index=False)
    print(f"Results saved to {file_path}")

# Test the script
if __name__ == "__main__":
    query = "Jobs software engineer jobs in New York"
    result = search_google(query, num_results=10)
    if result:
        print("Search results retrieved successfully!")
        # Extract and save results to CSV
        results = extract_results(result)
        save_to_csv(results)
