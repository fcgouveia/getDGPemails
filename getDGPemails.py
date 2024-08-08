from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

def extract_emails(driver):
    emails = []
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # print("Page source for debugging:\n", driver.page_source)  # Print page source for debugging
        
        # Find all "mailto:" links
        mailtos = soup.select('a[href^="mailto:"]')
        if not mailtos:
            print("No 'mailto:' links found on the page.")
        for mailto in mailtos:
            email = mailto.get('href').split(':')[1]
            emails.append(email)
    except Exception as e:
        print(f"Error extracting emails: {e}")
    return emails

def extract_h1_content(driver):
    try:
        # Wait for the div with the h1 to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'tituloImpressao'))
        )
        
        # Extract the h1 content
        h1_element = driver.find_element(By.CSS_SELECTOR, '#tituloImpressao h1')
        return h1_element.text.strip()  # Extract and clean text
    except Exception as e:
        print(f"Error extracting h1 content: {e}")
        return ''

def search_and_scrape(search_terms, base_url, output_csv):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    service = ChromeService('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t')  # Use tab as delimiter
        csvwriter.writerow(['Search Term', 'URL', 'Group Name', 'Email'])

        for search_term in search_terms:
            try:
                driver.get(base_url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'idFormConsultaParametrizada:idTextoFiltro'))
                )
                
                search_box = driver.find_element(By.ID, 'idFormConsultaParametrizada:idTextoFiltro')
                search_box.clear()
                search_box.send_keys(search_term)
                search_box.send_keys(Keys.RETURN)
                
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@onclick, 'mojarra.jsfcljs')]"))
                )
                
                link = driver.find_element(By.XPATH, "//a[contains(@onclick, 'mojarra.jsfcljs')]")
                
                # Modify the onclick attribute to prevent opening in a new tab
                driver.execute_script("""
                    var elem = arguments[0];
                    var onclick = elem.getAttribute('onclick');
                    var newOnclick = onclick.replace(/'_blank'/g, "''");
                    elem.setAttribute('onclick', newOnclick);
                """, link)
                
                # Click the link after modification
                link.click()

                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body'))
                )

                emails = extract_emails(driver)
                h1_content = extract_h1_content(driver)  # Get the content of the <h1>
                current_url = driver.current_url  # Get the current URL
                if emails:
                    for email in emails:
                        csvwriter.writerow([search_term, current_url, h1_content, email])
                    print(f"Emails for term '{search_term}' written to {output_csv}")
                else:
                    csvwriter.writerow([search_term, current_url, h1_content, "not found"])
                    print(f"No emails found for term '{search_term}'.")
            except Exception as e:
                csvwriter.writerow([search_term, "", "Error", ""])
                print(f"Error processing search term '{search_term}': {e}")

    driver.quit()

if __name__ == "__main__":
    base_url = 'http://dgp.cnpq.br/dgp/faces/consulta/consulta_parametrizada.jsf'
    grupos_file = 'grupos.txt'
    output_csv = 'emails.tsv'  # Change file extension to .tsv for tab-delimited files
    
    with open(grupos_file, 'r', encoding='utf-8') as file:
        search_terms = file.read().splitlines()
    
    search_and_scrape(search_terms, base_url, output_csv)
