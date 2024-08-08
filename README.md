# getDGPemail

Python 3 script to scrape the emails from CNPq Diretório de Grupos de Pesquisa based on their names

This project is a Python script that uses Selenium and BeautifulSoup to extract email addresses and relevant information from the web page of Diretório de Grupos de Pesquisa based on search terms. The script interacts with a specific webpage to perform searches, navigate through results, and scrape data.

# Features

Search and Scrape: Automatically performs searches on a web page and scrapes email addresses from the results.
Extract H1 Content: Captures the content of the h1 tag from a specific div for each search result which represents the name of the Group.
Tab-Delimited Output: Saves the extracted information in a tab-delimited file.

# Requirements

Python 3.x
Selenium
BeautifulSoup4
ChromeDriver (compatible with your version of Chrome)

# Installation

Clone the Repository:

bash
Copiar código
git clone https://github.com/fcgouveia/getDGPemail.git
cd repository-name

# Install Dependencies:

You need to have Python installed. Then, install the required Python packages using pip:

bash
Copiar código
pip install selenium beautifulsoup4
Download ChromeDriver:

Download the ChromeDriver executable from ChromeDriver Download.
Ensure that chromedriver.exe is available in your system path or specify its path directly in the script.
Usage
Prepare Input File:

Create a text file named grupos.txt in the same directory as the script. Add each search term on a new line.

Run the Script:

Ensure you have chromedriver.exe in the same directory as the script or specify its path in the ChromeService line. Then, run the script:

bash
Copiar código
python get-emails2.py
The script will read search terms from grupos.txt, perform searches, and save the results in emails.tsv.

# Script Details

Functions

extract_emails(driver): Extracts email addresses from the page source using BeautifulSoup.
extract_h1_content(driver): Extracts the content of the h1 tag within the div id="tituloImpressao".
search_and_scrape(search_terms, base_url, output_csv): Performs searches, modifies the page behaviour to avoid opening new tabs, and writes results to a tab-delimited file.

Output

File: emails.tsv

Columns:

Search Term: The term used for searching.
URL: The URL of the page where emails were found.
Group Name: Content of the h1 tag.
Email: Extracted email address or "not found" if no emails were found.

# Troubleshooting

ChromeDriver Issues: Ensure ChromeDriver is compatible with your version of Google Chrome.
Encoding Errors: Ensure all files are encoded in UTF-8 to avoid encoding-related issues.
Element Not Found: If elements are not found, verify that the webpage structure has not changed or adjust the selectors.

# License

This project is licensed under the MIT License - see the LICENSE file for details.
