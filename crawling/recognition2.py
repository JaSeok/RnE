from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import time


class SeleniumFetcher:
    def __init__(self):
        # Selenium WebDriver optimize
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")  # Minimize logs
        options.add_argument("--blink-settings=imagesEnabled=false")  # Disable image loading
        options.page_load_strategy = "none"  # Fastest page load strategy
        self.driver = webdriver.Chrome(options=options)

    def fetch(self, url):
        try:
            # Open the webpage
            self.driver.get(url)

            # Wait for the body element to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Extract title
            title = self.driver.title.strip() if self.driver.title else "No Title"

            # Extract body text (first 100 lines)
            text_content = self.driver.execute_script(
                "return document.body.innerText.split('\\n').slice(0, 100).join('\\n');"
            ).strip()  # Limit to the first 100 lines for efficiency

            # Extract domain name
            domain_name = urlparse(url).netloc

            return text_content, title, domain_name

        except Exception as e:
            return f"Error: {e}", None, None

    def close(self):
        # Close the browser
        self.driver.quit()


def main(url):
    fetcher = SeleniumFetcher()

    try:
        start_time = time.time()  # Start time
        webpage_text, webpage_title, domain_name = fetcher.fetch(url)
        fetcher.close()  # Ensure the browser is closed
        end_time = time.time()  # End time

        # Save webpage text
        if webpage_text:
            with open("webpage_text.txt", "w", encoding="utf-8") as text_file:
                text_file.write(webpage_text)

        # Save webpage title and domain
        if webpage_title and domain_name:
            with open("webpage_title.txt", "w", encoding="utf-8") as title_file:
                title_file.write(f"{webpage_title} ({domain_name})")

    except Exception:
        pass
    finally:
        fetcher.close()


if __name__ == "__main__":
    url = input("Enter the URL for recognition2: ").strip()
    if url:
        main(url)
