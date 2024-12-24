import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to initialize the WebDriver and open the URL
def initialize_driver():
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/")  # Replace with your desired URL
    return driver

# Function to perform a Google search
def search_jobs(driver, query):
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.submit()

# Function to click on the 'Jobs' tab
def click_jobs_tab(driver):
    jobs_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='YmvwI' and text()='Jobs']"))
    )
    jobs_tab.click()
    print("Clicked on the 'Jobs' tab successfully.")

# Function to filter jobs by 'Date Posted' and select 'Last Month'
def filter_by_date_posted(driver):
    wait = WebDriverWait(driver, 10)
    
    # Click on 'Date Posted'
    date_posted_filter = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Date posted']"))
    )
    date_posted_filter.click()

    # Select "Last Month" filter
    last_month_option = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Last month']"))
    )
    last_month_option.click()
    print("Successfully filtered results for the Last Month.")

# Function to extract job details
def extract_job_details(driver):
    wait = WebDriverWait(driver, 10)
    
    # Wait for job listings container to load
    jobs_container = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "eqAnXb"))
    )
    print("Job listings container loaded successfully.")

    # Find job links within the container
    job_links = jobs_container.find_elements(By.CLASS_NAME, "MQUd2b")
    job_details = []

    for index, link in enumerate(job_links):
        try:
            href = link.get_attribute("href")
            if href:  # Ensure the href exists
                print(f"Extracted job {index + 1}: {href}")
                job_details.append({"link": href})
        except Exception as e:
            print(f"Error extracting details for job {index + 1}: {e}")

    return job_details

# Function to save job details to a CSV file
def save_to_csv(job_details, file_name="job_links.csv"):
    try:
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["link"])
            writer.writeheader()
            writer.writerows(job_details)
        print(f"Job details saved to {file_name} successfully.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Main function to bring everything together
def main():
    driver = None
    try:
        # Initialize driver
        driver = initialize_driver()
        
        # Perform actions step by step
        search_jobs(driver, "Cleaner jobs in New York")
        click_jobs_tab(driver)
        filter_by_date_posted(driver)

        # Extract and display job details
        time.sleep(3)  # Allow results to load
        job_details = extract_job_details(driver)
        
        # Print job details
        print("\nExtracted Job Listings:")
        for job in job_details:
            print(job)

        # Save job details to a CSV file
        save_to_csv(job_details)

        # Optional: Keep the browser open for inspection
        input("Press Enter to close the browser...")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
