import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link = 'https://www.google.com/search?sca_esv=fe9a7d66c1ab6f77&biw=1036&bih=651&q=Cleaner+jobs+in+New+York+in+the+last+month&uds=ADvngMhyIGZqzcYKCwp-CUjq2KinkiBqbPdKyAJrhSeu5zgddE3Icp-Z2tRUz9-xLTtvSb74RWKbtBdg2qhQqItvnpOjncpPbQNb66CX-9YhgrAso-LcZagENyrpUo7AT4KJ57CiYLXE7RFnHAyfUOmaDtNDtK6DvUkZ3GBjfeULCyCDrq8klANSyRcjvUPCPmc594NCg-_zWcLVsXaWTz1pTW-1ol1v0H6dPiXJmWZGEJM-WCTKyoXh2s3SFSRefH-mSfP_Elksiz0rNi5dDVHoCxnz9lrnKpqHYJow3n0Asec484rBQGYxH_K3Kq8nG4d2lHfpBNsA0VHVljQk_Hlzc3NJET7M2Q&udm=8&sa=X#vhid=vt%3D20/docid%3DnTyFB4qPgENkELrdAAAAAA%3D%3D&vssid=jobs-detail-viewer'
driver = webdriver.Chrome()
def get_driver(link):
    driver.get(link)
    driver.maximize_window()
    return driver

def scrape_details(driver):
    container = EC.presence_of_element_located((By.CLASS_NAME, "hh1Ztf ip4nvd k4o2Hc"))
    wait = WebDriverWait(driver, 10)
    wait.until(container)
    details = driver.find_elements(By.CLASS_NAME, "hh1Ztf ip4nvd k4o2Hc")
    return details




def main():
    driver = get_driver(link)
    time.sleep(5000000)
    driver.quit()


if __name__ == '__main__':
    main()