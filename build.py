import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil


# File to store the username and password
secrets_file = 'secrets.txt'

# Check if secrets.txt exists
if not os.path.exists(secrets_file):
    # If not, ask the user for input
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Save the username and password to secrets.txt
    with open(secrets_file, 'w') as f:
        f.write(f"{username}\n{password}")
else:
    # If the file exists, read username and password from it
    with open(secrets_file, 'r') as f:
        username, password = f.read().splitlines()


### Browser and Download Setup
# Set up Chrome options for downloading PDFs
# Set the directory to save downloaded PDFs(creates it if not present)
download_dir = os.path.abspath("downloads")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
# Initializing chrome options object
chrome_options = Options()
# Chrome Preferences Setup
prefs = {
    "download.default_directory": download_dir,  # Set download directory
    "download.prompt_for_download": False,  # Disable download prompt
    "download.directory_upgrade": True,  # Automatically upgrade download directory
    "safebrowsing.enabled": True,  # Enable safe browsing (for automatic downloads)
    "profile.default_content_settings.popups": 0,  # Disable popups
    "plugins.always_open_pdf_externally": True,  # Download PDFs automatically
}

chrome_options.add_experimental_option("prefs", prefs)

# Initialize the WebDriver with the specified options
service = Service()  # Update this to the correct path if getting errors about webdriver missing
driver = webdriver.Chrome(service=service, options=chrome_options)
# Set implicit wait for locating elements
driver.implicitly_wait(3)  # Adjust as needed for slow loading pages or slower connections


# Folder Download functions
def download_folder():
    # Locate the button using XPath (class and partial text content)
    # Locate all buttons with the class 'btn btn-secondary'
    button = driver.find_element(By.CSS_SELECTOR, ".navitem.ml-auto button.btn.btn-secondary[type='submit']")
    # Click the button
    button.click()
    # Wait for the download
    time.sleep(2)


# File formats to download using alternative binary method, modify to add formats if needed
downloadable_files = ('.docx', '.xlsx', '.pptx', '.txt', '.csv', '.zip', '.rar',
                      '.py', '.r', '.sql', '.ipynb', '.java', '.cpp', '.c', '.html', '.css',
                      '.js', '.json', '.xml', '.md', '.tex', '.jpg', '.png', '.gif', '.mp4',
                      '.mp3', '.wav', '.xls', '.doc', '.ppt', '.sav', '.dta', '.m', '.sas',
                      '.ps', '.ai', '.indd', '.svg', '.epub', '.mobi', '.rtf', '.phe', '.map','.fam','bim')


# Function to manually download file using requests
def download_file(url, file_name, cookies):
    try:
        response = requests.get(url, cookies=cookies, stream=True)
        response.raise_for_status()  # Check if the request was successful
        downloads_path = os.path.join(download_dir, file_name)  # Get the correct downloads directory
        # Download the file by iterating through the bin content
        with open(downloads_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"File downloaded: {file_name}")
    except requests.exceptions.RequestException as e:  # Error handling
        print(f"Failed to download {file_name}: {str(e)}")


# Login Page Popup
driver.get("https://virtuale.unibo.it/login/index.php")
# input("After making sure you are logged in press Enter to continue ...")


# Automated Login Process - WiP
login_btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".idp.btnUnibo")))

login_btn.click()
# Wait until the username input field is present
username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'userNameInput'))
)
# Fill in the username and password
username_field.send_keys(username)
password_field = driver.find_element(By.ID, 'passwordInput')
password_field.send_keys(password)
time.sleep(1)
# Wait for the submit button (by id) to be clickable and click it
submit_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'submitButton'))
)
submit_button.click()

# ClassPage to Scrape URL
target = input("Please paste the URL of the virtuale Class you want to scrape and press Enter:\n")
# Load desired virtuale page
driver.get(target)
# Wait for loading
time.sleep(5)

# Extract and print the title of the class
course_title = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "page-header-headings"))).text
print(f"The {course_title} is about to be scraped...")

# Find all elements with the class 'aalink stretched-link' (download links)
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

# Save browser cookies for later use in file download function
cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}

# Loop through the elements, extract the href, and handle each link appropriately
for index, element in enumerate(elements[1:]):  # Skip element 1, usually announcements page
    try:
        # Extract the href attribute
        href = elements[index].get_attribute('href')
        # Verify that href is not null
        if href:
            print(f"Processing link {index + 1}: {href}")
            # First, navigate to the href link to handle redirects
            driver.get(href)
            time.sleep(2)  # Wait for the page to load and the redirect to complete
            # Get the final URL after redirection and print it
            final_url = driver.current_url
            print(f"Final URL after redirection: {final_url}")

            # Check if the final URL is to a downloadable file (.txt, .py, .r, .sql, etc.)
            if final_url.lower().endswith(downloadable_files):
                print(f"Link {index + 1} is a file download link. Downloading...")

                # Extract the file name and download the file
                file_name = os.path.basename(final_url)
                # Use download file function to download the file to downloads directory
                download_file(final_url, file_name, cookies)
            elif "folder" in final_url.lower():
                print(f"Link {index + 1} contains 'folder'. Attempting to download the folder...")
                # Use download folder function to get the linked folder
                download_folder()
                # Optionally return to the previous page
                driver.get(target)
                time.sleep(2)  # Wait to load main target page
                elements = driver.find_elements(By.CLASS_NAME,
                                                'aalink.stretched-link')  # Reload href containing elements
                continue
            else:
                print(
                    f"Link {index + 1} does not lead to a downloadable file or it leads directly to the download. Continuing...")

            # Return to the original page (use driver.back() to navigate back)
            try:
                driver.get(target)  # Go back to the original page
                time.sleep(2)  # Wait for the original page to load again
                elements = driver.find_elements(By.CLASS_NAME,
                                                'aalink.stretched-link')  # Reload href containing elements
            except WebDriverException:
                print("Error returning to the previous page. Exiting...")
                break

        else:
            print(f"No href found for element {index + 1}. Skipping...")
            continue

    except (TimeoutException, WebDriverException) as e:
        print(f"An error occurred while handling link {index + 1}: {str(e)}. Continuing with next link...")

# Close the browser after waiting for all downloads to be completed
time.sleep(5)
driver.quit()

# Moving all downloaded files to appropriately named folder
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

