import os
import time
import requests
import pickle
#from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, \
    ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil

### Browser and Download Setup
# List of file types to download
file_extensions = ['pdf', 'txt', 'docx', 'xlsx', 'zip', 'jpg', 'png', 'sql', 'r', 'py']
# Set up Chrome options for downloading PDFs
chrome_options = Options()
# Set the directory to save downloaded PDFs
download_dir = os.path.abspath("downloads")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
# Configure Chrome to automatically download PDFs to the specified directory
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,  # Set download directory
    "download.prompt_for_download": False,  # Disable download prompt
    "download.directory_upgrade": True,  # Automatically upgrade download directory
    "safebrowsing.enabled": True,  # Enable safe browsing (for automatic downloads)
    "plugins.always_open_pdf_externally": True,  # Automatically download PDFs
    "profile.default_content_settings.popups": 0,  # Disable popups
    "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
    "profile.default_content_setting_values.automatic_downloads": 1,
    "profile.default_content_setting_values": {
        "automatic_downloads": 1
    },
    # Force download of specific file types by MIME type
    "profile.default_content_settings": {
        "automatic_downloads": 1,
        "pdfjs.disabled": True  # Disables built-in PDF viewer for .pdf files
    },
    "plugins.always_open_pdf_externally": True,  # Download PDFs automatically
    "profile.managed_default_content_settings": {
        "automatic_downloads": 1
    }
}

# Add MIME types for files to be downloaded
mime_types_to_download = {
    "application/octet-stream": "sql",  # For .sql files
    "text/plain": "txt",  # For .txt files
    "text/x-python": "py",  # For .py files
    "text/x-r": "r"  # For .r files
}

# Attach the MIME types to the preferences
prefs["profile.default_content_settings"]["automatic_downloads"] = mime_types_to_download

#Different preferences revision
prefs2 = {
    "download.default_directory": download_dir,  # Set download directory
    "download.prompt_for_download": False,  # Disable download prompt
    "download.directory_upgrade": True,  # Automatically upgrade download directory
    "safebrowsing.enabled": True,  # Enable safe browsing (for automatic downloads)
    "profile.default_content_settings.popups": 0,  # Disable popups
    "plugins.always_open_pdf_externally": True,  # Download PDFs automatically
}

chrome_options.add_experimental_option("prefs", prefs2)

# Initialize the WebDriver with the specified options
service = Service()  # Update this to the correct path
driver = webdriver.Chrome(service=service, options=chrome_options)
# Set implicit wait for locating elements
driver.implicitly_wait(3)  # Adjust as needed for slow loading pages

# Folder Download functions
def download_folder(url):
    # Locate the button using XPath (class and partial text content)
    # Locate all buttons with the class 'btn btn-secondary'
    button = driver.find_element(By.CSS_SELECTOR, ".navitem.ml-auto button.btn.btn-secondary[type='submit']")

    # Click the button
    button.click()
    time.sleep(2)
    driver.back()


# Function to manually download file using requests
def download_file(url, file_name, cookies):
    try:
        response = requests.get(url, cookies=cookies, stream=True)
        response.raise_for_status()  # Check if the request was successful
        file_path = os.path.join(download_dir, file_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"File downloaded: {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_name}: {str(e)}")


# Login Page Popup
driver.get("https://virtuale.unibo.it/login/index.php")
input("After making sure you are logged in press Enter to continue ...")
# ClassPage to Scrape URL
target1 = 'https://virtuale.unibo.it/course/view.php?id=59542'  # stats for econ
target2 = 'https://virtuale.unibo.it/course/view.php?id=61958'  # input('Please paste the URL of the virtuale Class you want to scrape:\n")
target3 = 'https://virtuale.unibo.it/course/view.php?id=63144'  # computational stats

target = target3

driver.get(target)
time.sleep(5)

# Extract and print the text of the element
course_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-header-headings"))).text
print(f"The {course_title} is about to be scraped...")


# Find all elements with the class 'aalink stretched-link'
try:
    elements = driver.find_elements(By.CLASS_NAME, 'aalink.stretched-link')

    if not elements:
        print("No elements found with the specified class.")
        driver.quit()
        exit()

except NoSuchElementException:
    print("Elements with the class 'aalink stretched-link' not found on the page.")
    driver.quit()
    exit()


# deprecated function
def parseAndDownload(url):
    # Parse the URL to get the file extension
    parsed_url = urlparse(url)
    file_extension = os.path.splitext(parsed_url.path)[1][1:]  # Get the extension without the dot
    # Check if the file type is in the list of supported file types
    if file_extension in file_extensions:
        print(f"Downloading file from: {url}")

        # Navigate to the file URL and trigger the download
        driver.get(url)

        # Wait for the download to complete
        time.sleep(5)  # Adjust based on your download speed

    else:
        print(f"File type {file_extension} is not in the supported list.")
        driver.get(redirected_url)
        time.sleep(2)
        final_url = driver.current_url
        parseAndDownload(final_url)

    if url.endswith(".pdf"):
        print(f"Redirected to: {url}")

        # Selenium should automatically trigger the download based on Chrome settings
        driver.get(url)

        # Wait for the download to complete
        time.sleep(5)  # Adjust based on your download speed


"""
for element in elements[1:]:
    href = element.get_attribute("href")
    print(href)
    if href:  # Check if the link is valid
        driver.get(href)
        time.sleep(2)
        redirected_url = driver.current_url
        try:
            parseAndDownload(redirected_url)
        except exceptions.StaleElementReferenceException as e:
            print('StaleElementReferenceException, trying again')
"""
cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
# Loop through the elements, extract the href, and click each link
for index, element in enumerate(elements[1:]):
    try:
        # Extract the href attribute
        href = elements[index].get_attribute('href')

        if href:
            print(f"Processing link {index + 1}: {href}")

            # First, navigate to the href link to handle redirects
            driver.get(href)
            time.sleep(2)  # Wait for the page to load and the redirect to complete

            # Get the final URL after redirection
            final_url = driver.current_url
            print(f"Final URL after redirection: {final_url}")

            # Check if the final URL is to a downloadable file (.txt, .py, .r, .sql, etc.)
            if final_url.endswith(('.txt', '.py', '.r', '.sql')):
                print(f"Link {index + 1} is a file download link. Downloading...")

                # Extract the file name and download the file
                file_name = os.path.basename(final_url)
                download_file(final_url, file_name, cookies)
            elif "folder" in final_url.lower():
                print(f"Link {index + 1} contains 'folder'. Triggering folder-specific behavior...")
                download_folder(final_url)
                # Optionally return to the previous page
                driver.get(target)
                continue
            else:
                print(
                    f"Link {index + 1} does not lead to a downloadable file or it leads directly to the download. Continuing...")

            # Return to the original page (use driver.back() to navigate back)
            try:
                driver.get(target)  # Go back to the original page
                time.sleep(2)  # Wait for the original page to load again
                elements = driver.find_elements(By.CLASS_NAME, 'aalink.stretched-link')
            except WebDriverException:
                print("Error returning to the previous page. Exiting...")
                break

        else:
            print(f"No href found for element {index + 1}. Skipping...")
            continue

    except (TimeoutException, WebDriverException) as e:
        print(f"An error occurred while handling link {index + 1}: {str(e)}. Continuing with next link...")

# Wait for all downloads to complete (optional)
time.sleep(5)  # You can adjust this time based on your needs

# Save the cookies to a file after login
cookies = driver.get_cookies()
with open("cookies.pkl", "wb") as file:
    pickle.dump(cookies, file)

# Close the browser
driver.quit()

new_folder_name = course_title.replace(" ", "_")
new_folder_path = os.path.join(download_dir, new_folder_name)

# Create the new folder if it doesn't exist
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
    print(f"Created new folder: {new_folder_path}")

# Move all files from 'downloads' to the new folder
for file_name in os.listdir(download_dir):
    # Get the full path of the file
    file_path = os.path.join(download_dir, file_name)

    # Only move files (not directories) and exclude the new folder itself
    if os.path.isfile(file_path) and file_name != new_folder_name:
        # Construct the new destination path
        new_file_path = os.path.join(new_folder_path, file_name)

        # Move the file to the new folder
        shutil.move(file_path, new_file_path)
        print(f"Moved: {file_name} -> {new_folder_name}")