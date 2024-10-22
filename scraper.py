import requests
from bs4 import BeautifulSoup

cookies = {
    # Your cookies here
}

def check_cloudflare_blocking(url):
    try:
        response = requests.get(url)
        
        # Check HTTP status code
        if response.status_code == 403:
            print("Request blocked by Cloudflare (403 Forbidden)")

        # Inspect HTTP headers
        if 'Server' in response.headers and 'cloudflare' in response.headers['Server'].lower():
            print("Response indicates Cloudflare server")

        if 'CF-RAY' in response.headers:
            print("CF-RAY header found:", response.headers['CF-RAY'])

        if 'CF-Cache-Status' in response.headers:
            print("CF-Cache-Status:", response.headers['CF-Cache-Status'])

    except requests.RequestException as e:
        print("Error:", e)

# URL of the website you want to scrape
url = 'https://nextjs.org/docs'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send a GET request to the website with cookies
response = requests.get(url, headers=headers, cookies=cookies)

# Check if Cloudflare is blocking the request
check_cloudflare_blocking(url)

# Ensure the request was successful
if response.status_code == 200:
    # Initialize BeautifulSoup with the content of the fetched page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example of extracting data: Print all headers from h1 to h6
    for i in range(1, 7):
        headers = soup.find_all(f'h{i}')
        for header in headers:
            print(header.text.strip())  # Using .text to get the text content of each header tag
    
    # Extract and print all <a> tags along with their href attributes
    links = soup.find_all('a')
    for link in links:
        print(link.get('href'))

else:
    print(f"Failed to retrieve content, status code {response.status_code}")