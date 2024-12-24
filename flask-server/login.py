import itertools
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import urllib
# from scrape import scrape_jobs
import random


# Set up the WebDriver
driver = webdriver.Chrome()

# Login to LinkedIn
driver.get("https://www.linkedin.com/login")
time.sleep(random.uniform(3, 6))

time.sleep(2)

# Enter credentials
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
time.sleep(random.uniform(3, 6))
username.send_keys("chamudimalsha@yahoo.com") # Typing text into a input field
time.sleep(random.uniform(3, 6))
password.send_keys("chamudimal176#")
time.sleep(random.uniform(3, 6))
password.send_keys(Keys.RETURN) # Press enter to submit the form
time.sleep(random.uniform(3, 6))
driver.get("https://www.linkedin.com/jobs/search/?")
time.sleep(random.uniform(3, 6))


job_roles = [
    "Customer service representative" ,
    # "AML Analyst",
    "Remittance clerk" ,
    "Credit analyst" ,
    "Compliance analyst",
    # "Internal audit operations "
]

job_locations = [
    "United States",
    "Australia"  
]

job_sectors = [

    "Banks",
    "Exchange houses ",
    "Financial institutions",
    "Corporate"
]

experience_level = [

]


# Generate all possible combinations of roles, locations, and sectors
combinations = list(itertools.product(job_roles, job_locations)) # add job_sectors later

# Base LinkedIn URL for job search
base_url = "https://www.linkedin.com/jobs/search/?"

# Function to create a LinkedIn search URL
def create_search_url(role, location):
    # Combine role, location, and sector into a single search term
    query = f"{role}"
    # Encode the query and location to be URL-friendly
    params = {
        "keywords": query,
        "location": location,
        # "f_TP": date_filter  # e.g., '1' for Past 24 hours, '1%2C2' for Past Week
    }
    return base_url + urllib.parse.urlencode(params)

# Generate URLs for each combination
urls = [create_search_url(role, location) for role, location in combinations]
for i in urls:
    print(i)

def scroll_down():
    """Scroll down the page to load more job results."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 300);")
    time.sleep(2)  # Allow time for jobs to load

def scroll_up():
    """Scroll up the page a little bit."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 300);")
    time.sleep(2)  # Allow time for any jobs to load

def scrape_companies():
    """Scrape company names, job titles, and links from the currently loaded jobs."""
    job_list = []  # List to store all jobs as tuples (company, job title, link)

    try:
        # Get all companies, job titles, and links from the loaded job cards
        postings = driver.find_elements(By.CLASS_NAME, "flex-grow-1 artdeco-entity-lockup__content ember-view")
        for posting in postings:

            company = posting.find_element(By.CLASS_NAME, "artdeco-entity-lockup__subtitle ember-view")
            link = driver.find_elements(By.CLASS_NAME, "full-width artdeco-entity-lockup__title ember-view")
            # Extract the job title from 'aria-label'
            job_title = link.get_attribute("aria-label")
            # Extract the job link from 'href'
            job_link = link.get_attribute("href")

            #job_link.click()
            # criteria_list = []
            # criterias = driver.find_elements(By.CLASS_NAME, "description__job-criteria-item")
            # for criteria in criterias:
            #     critera__name = criteria.find_element(By.CLASS_NAME, "description__job-criteria-subheader").text
            #     critera__value = criteria.find_element(By.CLASS_NAME, "description__job-criteria-text").text
            #     criteria_list.append((critera__name, critera__value))
            # timePeriod = posting.find_element(By.CLASS_NAME, "job-search-card__listdate")


            company_name = company.text.strip()
            job_title_text = job_title.text.strip()  # Get the job title

            job_list.append((company_name, job_title_text, job_link))

    except Exception as e:
        print(f"Error scraping companies: {e}")

    return job_list

def check_all_jobs_viewed():
    """Check if the 'You've viewed all jobs' message is present."""
    try:
        viewed_all_element = driver.find_element(
            By.XPATH, "//p[contains(@class, 'inline-notification__text') and contains(text(), \"You've viewed all jobs for this search\")]"
        )

        return viewed_all_element is not None
    except NoSuchElementException:
        return False
    

def scrape_jobs(target_count):
    """Main function to scrape jobs and companies."""
    total_jobs = []  # List to store all scraped jobs

    try:

        while len(total_jobs) < target_count:
            scroll_down()  # Scroll down the page to load more jobs

            # Scrape and store company names, job titles, and links
            scraped_jobs = scrape_companies()
            total_jobs.extend(scraped_jobs)  # Add new jobs to the total list

            # If we've scraped enough jobs, break the loop
            if len(total_jobs) >= target_count:
                print(f"Reached the target of {target_count} jobs.")
                break
            

    except Exception as e:
        print(f"Error: {e}")

    finally:
        print(f"Total jobs scraped: {len(total_jobs)}")

        # Create a DataFrame from the scraped job data
        df = pd.DataFrame(total_jobs, columns=["Company", "Job Title", "Time Period Posted", "Link", "Criterias"])

        df = df.drop_duplicates(subset=["Company", "Job Title"])  # Drop duplicate entries

        # Define the path to save the CSV file (change 'YOUR_USERNAME' to your actual username)
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        csv_file_path = os.path.join(desktop_path, "scraped_jobs_list.csv")

       # Write the job data to a CSV file using pandas, appending if file exists
        if os.path.exists(csv_file_path):
            df.to_csv(csv_file_path, mode="a", header=False, index=False, encoding='utf-8')
            print(f"Data appended to {csv_file_path}")
        else:
            df.to_csv(csv_file_path, index=False, encoding='utf-8')  # Create a new file with headers if it doesn’t exist
            print(f"Data saved to {csv_file_path}")

        # Do not close the driver after finishing
        input("Press Enter to close the browser...")

for url in urls:
    driver.get(url)
    time.sleep(5)
    scrape_jobs(20)
    print("Scraping done for ", url)








