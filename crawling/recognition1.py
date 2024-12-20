import requests
from bs4 import BeautifulSoup

def fetch_webpage_content(url: str) -> tuple:
    try:
        # Send HTTP GET requst
        headers = {
            "User-Agent": "Chrome/131.0.6778.140"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse HTML contentp
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No Title Found"
        body = soup.body.get_text(separator="\n", strip=True) if soup.body else "No Content Found"
        return body, title
    except Exception as e:
        return None, None

def main(url):
    content, title = fetch_webpage_content(url)

    if content:
        with open("webpage_text.txt", "w", encoding="utf-8") as f:
            f.write(content)


    if title:
        with open("webpage_title.txt", "w", encoding="utf-8") as f:
            f.write(title)

if __name__ == "__main__":
    main()
