# Automated File Scraper and Downloader for Virtuale(VirtualeUniBOt)
This Python script uses Selenium to automate the login onto the virtuale website and scrape all downloadable files and folders from a specific class. It handles the downloading of files of various types and moves them into a well-organized folder structure based on the course title.

!!! _This script is made by a student and is in no way affiliated to UniBo. It requires valid student credential for each run._!!!

## Features
- Manual login process: requires manual login on each run. Support for session recovery and automated login to come soon. 
- File Downloads: Automatically downloads common file types such as .pdf, .docx, .xlsx, .txt, .py, etc.
- Folder Downloads: Handles the detection and downloading of folders.

- Organized Structure: Creates a new folder named after the course and moves all downloaded files into that folder.

- Error Handling: Robust error handling for failed downloads or navigation issues.

## Prerequisites
- Python 3.6+
- Selenium WebDriver: Ensure that you have the Chrome WebDriver installed on your machine. You can download it here.

## Installation
Clone this repository or download the script.

Install the required Python packages:
`
pip install -r requirements.txt`

Ensure you have Chrome installed and WebDriver configured on your system.

## Usage
- Login Process:
Run the script and manually log in to the website. The script will pause at the login page, and once you are logged in, you can press Enter to proceed.

- Class URL:
You will be prompted to enter the URL of the class page you want to scrape. Paste the URL and press Enter.
File and Folder Downloading:

The script will automatically scrape the page for all downloadable files and folders.
It handles various file formats (.pdf, .docx, .xlsx, .txt, etc.).
It also moves the downloaded files into a folder named after the course title.

- Saving Files:
The files will be saved in a downloads directory, and further organized into a sub-folder named after the course.
## Example
`

python scraper.py`
You will be prompted to:

- Login manually: The script opens the browser and pauses for you to complete login.

- Enter the URL of the course page: This is the page from which files will be scraped.

### Customization
- File Types: You can modify the list of downloadable file types by editing the downloadable_files tuple in the script.
- Waiting Time: Adjust the waiting times (time.sleep()) to optimize for your network speed.
### Error Handling
The script includes error handling for:

- Missing or unreachable elements

- Failed downloads

- Timeout issues during navigation
## Contributing
Feel free to fork this repository and make your improvements. Pull requests are welcome!