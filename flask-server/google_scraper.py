import itertools
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Job roles and locations
jobs = ["Software Engineer", "Machine Learning Engineer", "Software Developer"]
locations = ["New York", "Sri Lanka", "Australia"]
combinations = list(itertools.product(jobs, locations))

# Initialize the WebDriver
def initialize_driver():
    chrome_options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("--headless") == False # Remove for debugging
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Perform a Google search
def search_jobs(driver, query):
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.submit()

# Click on the 'Jobs' tab
def click_jobs_tab(driver):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='YmvwI' and text()='Jobs']"))
    ).click()

# Filter by 'Last Month'
def filter_by_date_posted(driver):
    wait = WebDriverWait(driver, 10)
    date_posted_filter = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Date posted']"))
    )
    date_posted_filter.click()
    last_month_option = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Last month']"))
    )
    last_month_option.click()

# Extract job details
def extract_job_details(driver):
    wait = WebDriverWait(driver, 10)
    jobs_container = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "eqAnXb"))
    )
    job_links = jobs_container.find_elements(By.CLASS_NAME, "MQUd2b")
    return [{"link": link.get_attribute("href")} for link in job_links if link.get_attribute("href")]

# Save job details to a CSV file
def save_to_csv(job_details, file_name="job_links.csv"):
    with open(file_name, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["link"])
        if file.tell() == 0:  # Write header only if the file is new
            writer.writeheader()
        writer.writerows(job_details)

# Main function
def main():
    driver = initialize_driver()
    try:
        for role, location in combinations:
            try:
                query = f"{role} jobs in {location}"
                driver.get("https://www.google.com/")
                search_jobs(driver, query)
                click_jobs_tab(driver)
                filter_by_date_posted(driver)
                time.sleep(3)  # Wait for results to load
                job_details = extract_job_details(driver)
                save_to_csv(job_details)
                print(f"Saved jobs for {query} to CSV.")
            except Exception as e:
                print(f"Error with query {role} in {location}: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
