import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_driver(link):
    driver = webdriver.Chrome()
    driver.get(link)
    driver.maximize_window()
    return driver


def scrape_details(driver, link_no, link):
    wait = WebDriverWait(driver, 10)
    job_details = {"link_no": link_no, "apply_link": "", "title": "", "company": "", "source": "", "other_info": []}

    # Locate container_2 using XPath
    try:
        container = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div'))
        )
    except Exception as e:
        print(f"Container could not be loaded for link {link_no}: {e}")
        return job_details

    # Extract job details
    try:
        title_container = container.find_element(By.CLASS_NAME, "JmvMcb")
        job_details["title"] = title_container.find_element(By.TAG_NAME, "h1").text
        job_details["company"] = container.find_element(
            By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/c-wiz[1]/c-wiz/c-wiz/div[2]/div[1]'
        ).text
        other_info = container.find_element(
            By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/c-wiz[1]/c-wiz/c-wiz/div[2]/div[2]'
        )
        info_elements = other_info.find_elements(By.CLASS_NAME, "nYym1e")
        job_details["other_info"] = [info.text for info in info_elements]
    except Exception as e:
        print(f"Failed to extract details for link {link_no}: {e}")

    # Extract source (if applicable)
    try:
        link_container = container.find_element(By.CLASS_NAME, "fQYLde")
        a_element = link_container.find_element(By.CLASS_NAME, "nNzjpf-cS4Vcb-PvZLI-Ueh9jd-LgbsSe-Jyewjb-tlSJBe")
        job_details["apply_link"] = a_element.get_attribute("href")
        job_details["source"] = a_element.get_attribute("title")
    except Exception as e:
        print(f"Failed to extract source for link {link_no}: {e}")

    return job_details


def read_links_from_csv(file_path):
    links = []
    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header
            for row in csv_reader:
                if row:  # Check if the row is not empty
                    links.append(row[0])  # Assuming links are in the first column
    except Exception as e:
        print("Error reading CSV file:", e)
    return links


def save_to_csv(results, file_path):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write header
            csv_writer.writerow(["link_no", "title", "company", "link", "source", "other_info"])
            # Write rows
            for result in results:
                csv_writer.writerow([
                    result["link_no"],
                    result["title"],
                    result["company"],
                    result["apply_link"],
                    result["source"],
                    "; ".join(result["other_info"])  # Join other info into a single string
                ])
        print(f"Results saved to {file_path}")
    except Exception as e:
        print(f"Error saving to CSV file: {e}")


def main():
    csv_file_path = "job_links.csv"  # Make sure this file is in the same directory
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_file_path = os.path.join(desktop_path, "job_details.csv")

    links = read_links_from_csv(csv_file_path)

    if not links:
        print("No links found in the CSV file.")
        return

    results = []
    for link_no, link in enumerate(links, start=1):
        print(f"Processing link {link_no}: {link}")
        driver = get_driver(link)
        job_details = scrape_details(driver, link_no, link)
        results.append(job_details)
        driver.quit()
        time.sleep(2)  # Small delay between processing links

    save_to_csv(results, output_file_path)


if __name__ == '__main__':
    main()
