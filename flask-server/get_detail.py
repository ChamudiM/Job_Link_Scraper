import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link = 'https://www.google.com/search?sca_esv=fe9a7d66c1ab6f77&biw=1036&bih=651&q=Cleaner+jobs+in+New+York+in+the+last+month&uds=ADvngMhyIGZqzcYKCwp-CUjq2KinkiBqbPdKyAJrhSeu5zgddE3Icp-Z2tRUz9-xLTtvSb74RWKbtBdg2qhQqItvnpOjncpPbQNb66CX-9YhgrAso-LcZagENyrpUo7AT4KJ57CiYLXE7RFnHAyfUOmaDtNDtK6DvUkZ3GBjfeULCyCDrq8klANSyRcjvUPCPmc594NCg-_zWcLVsXaWTz1pTW-1ol1v0H6dPiXJmWZGEJM-WCTKyoXh2s3SFSRefH-mSfP_Elksiz0rNi5dDVHoCxnz9lrnKpqHYJow3n0Asec484rBQGYxH_K3Kq8nG4d2lHfpBNsA0VHVljQk_Hlzc3NJET7M2Q&udm=8&sa=X#vhid=vt%3D20/docid%3DnTyFB4qPgENkELrdAAAAAA%3D%3D&vssid=jobs-detail-viewer'

def get_driver(link):
    driver = webdriver.Chrome()
    driver.get(link)
    driver.maximize_window()
    return driver

def scrape_details(driver):
    wait = WebDriverWait(driver, 10)

    
    # Locate container_2 using XPath
    try:
        container = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div'))
        )
        print("container_2 loaded successfully.")
    except Exception as e:
        print("container_2 could not be loaded:", e)
    
    # find title container
    try:
        title_container = container.find_element(By.CLASS_NAME, "JmvMcb")
        title = title_container.find_element(By.TAG_NAME, "h1").text
        company = title_container.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/c-wiz[1]/c-wiz/c-wiz/div[2]/div[1]').text
        other_info = title_container.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/c-wiz[1]/c-wiz/c-wiz/div[2]/div[2]')
        info = other_info.find_elements(By.CLASS_NAME, "nYym1e")

        
        print("Title:", title)
        print("Company:", company)
        for index, i in enumerate(info):
            print(f"Element {index + 1}: {i.text}")
        

    except Exception as e:
        print("Title could not be found:", e)

def link_scrape(driver):
    wait = WebDriverWait(driver, 10)

    # Locate container_2 using XPath
    try:
        link_container = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="sjsuid_0"]/div[1]/div'))
        )
        print("link_container loaded successfully.")
    except Exception as e:
        print("link_container could not be loaded:", e)

    # find links 
    try:
        link_button = link_container.find_element(By.CLASS_NAME, "fQYLde") 
        print("Link button found:")
        a_element = link_button.find_element(By.CLASS_NAME, "nNzjpf-cS4Vcb-PvZLI-Ueh9jd-LgbsSe-Jyewjb-tlSJBe")
        link = a_element.get_attribute("href")
        source = a_element.get_attribute("title")
        print("Link:", link)
        print("Source:", source)   

    except Exception as e:  
        print("Link could not be found:", e)

    
    

def main():
    driver = get_driver(link)
    scrape_details(driver)
    link_scrape(driver)
    time.sleep(5000000)  # Replace this with a smaller wait if needed
    driver.quit()

if __name__ == '__main__':
    main()
