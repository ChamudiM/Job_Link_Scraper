import time
import os
import pandas as pd
import itertools
import urllib.parse
# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

linkedinAPI_url = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/"

# Setup the WebDriver (assuming Chrome here)
driver = webdriver.Chrome()
driver.maximize_window()

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
    # "Banking field",
    # "Customer service", 
    # "Compliance",
    # "Credit operations", 
    # "Any Front office",
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


# Function to check for presence of filter tab
# This checks if we are on searcch page or not
def check_element_presence(driver, css_selector):
    """Check if a specific element is present on the page.
    
    Args:
        driver: The WebDriver instance.
        css_selector (str): The CSS selector of the element to locate.

    Returns:
        int: 1 if the element is present, 0 otherwise.
    """
    try:
        # Attempt to find the element
        driver.find_element(By.CSS_SELECTOR, css_selector)
        return 1  # Element found
    except NoSuchElementException:
        return 0  # Element not found
    
def apply_date_filter():
    """Apply the 'Past Month' filter under 'Date Posted'."""
    try:
        # Locate and click the 'Date Posted' filter button
        date_filter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Date posted filter')]"))
        )
        date_filter_button.click()
        print("Opened 'Date Posted' filter dropdown.")

        # Wait and select the 'Past Month' option in the dropdown
        past_month_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='f_TPR-1']/following-sibling::label"))
        )
        past_month_option.click()
        print("Selected 'Past Month' option.")

        # Locate and click the 'Done' button to apply the filter
        done_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='filter__submit-button' and @type='submit']"))
        )
        done_button.click()
        print("Clicked 'Done' to apply the date filter.")

    except Exception as e:
        print(f"Error applying date filter: {e}")
    

def close_any_modal():
    try:
    # Click on the parent button of the SVG icon
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "modal__dismiss"))
        )
        print("Modal detected")
        button.click()
        print("Modal closed")
        
        button.click()
    
    except TimeoutException:
        # If button click fails, try clicking the SVG element directly
        try:
            svg_icon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[local-name()='svg' and contains(@class, 'artdeco-icon')]"))
            )
            svg_icon.click()
        except TimeoutException:
            print("SVG icon not clickable.")
    except Exception as e:  
        print(f"Error closing modal: {e}")

def scroll_down():
    """Scroll down the page to load more job results."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 300);")
    time.sleep(2)  # Allow time for jobs to load

def scroll_up():
    """Scroll up the page a little bit."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 300);")
    time.sleep(2)  # Allow time for any jobs to load

def click_see_more_button():
    """Click the 'See more jobs' button if available and wait for the content to load."""
    try:
        see_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='See more jobs' and contains(@class, 'infinite-scroller__show-more-button')]")
            )
        )
        see_more_button.click()
        print("Clicked 'See more jobs' button.")
        time.sleep(5)  # Wait for new jobs to load
        return True
    except (TimeoutException, NoSuchElementException) as e:
        print(f"No 'See more jobs' button found. Error: {e}")
        return False

# def validate_url(expected_substring):
#     """Validate if the current URL contains the expected filter substring."""
#     current_url = driver.current_url
#     return expected_substring in current_url

# def reload_until_correct_url(expected_substring, max_retries=5):
#     """Reload the page until the URL contains the expected filter substring."""
#     retries = 0
#     while retries < max_retries:
#         if validate_url(expected_substring):
#             print("Correct URL detected.")
#             return True
#         print(f"URL validation failed. Retrying... ({retries + 1}/{max_retries})")
#         driver.refresh()
#         time.sleep(5)  # Allow time for the page to load
#         retries += 1
#     print("Max retries reached. Correct URL not detected.")
#     return False

# def verify_filter_applied(filter_name):
#     """Verify if the specified filter is applied by checking the UI."""
#     try:
#         # Look for the active filter button or label
#         active_filter = WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.XPATH, f"//button[contains(text(), '{filter_name}') and contains(@class, 'active')]"))
#         )
#         print(f"Filter '{filter_name}' is correctly applied.")
#         return True
#     except TimeoutException:
#         print(f"Filter '{filter_name}' is not applied.")
#         return False


def scrape_companies():
    """Scrape company names, job titles, and links from the currently loaded jobs."""
    job_list = []  # List to store all jobs as tuples (company, job title, link)

    try:
        # Get all companies, job titles, and links from the loaded job cards
        postings = driver.find_elements(By.CLASS_NAME, "base-card")
        for posting in postings:

            company = posting.find_element(By.CLASS_NAME, "base-search-card__subtitle")
            job_title = posting.find_element(By.CLASS_NAME, "base-search-card__title")
            job_link = posting.find_element(By.CLASS_NAME, "base-card__full-link")
            job_link.click()
            criteria_list = []
            criterias = driver.find_elements(By.CLASS_NAME, "description__job-criteria-item")
            for criteria in criterias:
                critera__name = criteria.find_element(By.CLASS_NAME, "description__job-criteria-subheader").text
                critera__value = criteria.find_element(By.CLASS_NAME, "description__job-criteria-text").text
                criteria_list.append((critera__name, critera__value))
            timePeriod = posting.find_element(By.CLASS_NAME, "job-search-card__listdate")


            company_name = company.text.strip()
            job_title_text = job_title.text.strip()  # Get the job title
            job_link = job_link.get_attribute("href")  # Get the job link
            timePeriod_posted = timePeriod.text.strip()

            job_list.append((company_name, job_title_text, timePeriod_posted, job_link, criteria_list))

    except Exception as e:
        print(f"Error scraping companies: {e}")

    return job_list  # Return the list to process outside

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
        close_any_modal()  # Close any modal popup that may block the content
        apply_date_filter()  # Apply the 'Past Month' date filter

        # Reload the page until the correct filter is applied
        # if not reload_until_correct_url("f_TPR-1"):
        #     print("Failed to reload the page with the correct filter.")
        #     return

        # # Check if the filter is correctly applied
        # if not verify_filter_applied("Past Month"):
        #     print("Filter 'Past Month' is not applied. Exiting.")
        #     return

        while len(total_jobs) < target_count:
            scroll_down()  # Scroll down the page to load more jobs

            # Scrape and store company names, job titles, and links
            scraped_jobs = scrape_companies()
            total_jobs.extend(scraped_jobs)  # Add new jobs to the total list

            # If we've scraped enough jobs, break the loop
            if len(total_jobs) >= target_count:
                print(f"Reached the target of {target_count} jobs.")
                break

            # Check if the "See more jobs" button appears and click it if available
            if not click_see_more_button():
                
                print("No more jobs to load. Trying to scroll up and then down again...")
                scroll_up()  # Scroll up a bit
                scroll_down()  # Try to scroll down again

                # If no "See more jobs" button is found, check for the "You've viewed all jobs" message
                if check_all_jobs_viewed():
                    print("All jobs have been loaded.")
                    break  # Exit the loop if all jobs are loaded

                continue  # Continue the loop

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

# Call the main scrape_jobs function to start the process
for url in urls:
    result = 0

    while result == 0:
        driver.get(url)
        time.sleep(5)
        result = check_element_presence(driver, "body > div.base-serp-page > section.base-serp-page__filters-bar")
        print("testing ", result)  # Will print 1 if the element is present, 0 otherwise
        
    scrape_jobs(20)
    print("Scraping done for ", url)

