import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

url = "https://quotes.toscrape.com/"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('div', class_='quote')

    data = []
    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = ', '.join(tag.text for tag in quote.find_all('a', class_='tag'))
        data.append([text, author, tags])

    df = pd.DataFrame(data, columns=['Quote', 'Author', 'Tags'])
    df = df.drop_duplicates() 
    df.to_csv('quotes.csv', index=False)
    print(f'Successfully saved {len(df)} quotes to quotes.csv')
else:
    print(f'Failed to retrieve page. Status code: {response.status_code}')
