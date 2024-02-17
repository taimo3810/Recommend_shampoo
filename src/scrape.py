import re
import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import uuid
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction, SentenceTransformerEmbeddingFunction
import os
import tqdm
import dotenv
dotenv.load_dotenv()

client = chromadb.HttpClient(host='localhost', port=8000)
embedding_func = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization_id=os.getenv("OPENAI_ORG_KEY")
)
#if not client.get_collection("amazon_db"):
client.delete_collection("amazon_db")
chroma_collection = client.get_or_create_collection(
    name="amazon_db",
    metadata={"hnsw:space": "cosine"},
    #embedding_function=embedding_func
)

def scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = 'https://www.amazon.co.jp/s?k=%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=G2N6VL4GS15F&sprefix=%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC%2Caps%2C218&ref=nb_sb_noss_1'

    curr_page = 1
    max_page = 5

    while True:
        print('page: {}, max_page: {}, url: {}'.format(curr_page, max_page, url))
        response = requests.get(url, headers=headers)
        main_soup = BeautifulSoup(response.content, 'html.parser')
        items_h2 = main_soup.find_all('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        ids = []
        documents = []
        meta_datas = []
        for item in tqdm.tqdm(items_h2, total=len(items_h2)):
            try:
                link = item.get('href')
                link = 'https://www.amazon.co.jp' + link
                soup = BeautifulSoup(requests.get(link, headers=headers).content, 'html.parser')

                title = soup.find('span', {'id': 'productTitle'}).text.strip()
                price = soup.find('span', {'class': 'a-offscreen'}).text.strip()
                descriptions = []

                description = soup.find('div', {'id': 'productDescription'})
                if description:
                    description = description.text.strip()
                    descriptions.append(description)

                description2 = soup.find('div', {'id': 'feature-bullets'})
                if description2:
                    description2 = description2.text.strip()
                    descriptions.append(description2)

                description3 = soup.find('table', {"id": "productDetails_techSpec_section_1"})
                if description3:
                    description3 = description3.text.strip()
                    descriptions.append(description3)

                description4 = soup.find('div', {"id": "aplus3p_feature_div"})
                if description4:
                    description4 = description4.text.strip()
                    descriptions.append(description4)
                if link is None:
                    continue
                text = f"""
                title: {title}
                price: {price}
                description: {" ".join(descriptions)}
                link: {link}
                """
                if title not in ids:
                    documents.append(text)
                    meta_datas.append({"title": title, "link": link, "price": price})
                    ids.append(title)
                time.sleep(1)
            except Exception as e:
                print(e)
                continue

        next_page_link = main_soup.find_all('span', {'class': 's-pagination-strip'})[0]
        next_page_link = next_page_link.find_all('a', {'class': 's-pagination-item s-pagination-button'})[-1]
        next_page_link = next_page_link.get('href')
        url = 'https://www.amazon.co.jp' + next_page_link

        curr_page += 1
        print("num of documents: {}".format(len(documents)))
        chroma_collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=meta_datas
        )
        if curr_page > max_page:
            break

from playwright.sync_api import sync_playwright
def run(playwright):
    browser = playwright.chromium.launch(
        headless=False, args=[
            "--disable-blink-features=AutomationControlled",
        ]
    )
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = 'https://www.amazon.co.jp/s?k=%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=G2N6VL4GS15F&sprefix=%E3%82%B7%E3%83%A3%E3%83%B3%E3%83%97%E3%83%BC%2Caps%2C218&ref=nb_sb_noss_1'
    page = browser.new_page(extra_http_headers=headers)

    page.goto(url)  # Navigate to Amazon
    page.wait_for_load_state()  # Wait for the page to finish loading

    result = page.click(
        'a.a-link-normal >> text=LUX(ラックス) バイオフュージョン ダメージディフェンス シャンプー&コンディショナー'
    )
    page.wait_for_load_state()  # Wait for the page to finish loading
    print(result)

    # Click on the search bar
    page.close()

    raise Exception('stop')
    # Scroll down the page (adjust the number of iterations as needed)
    for _ in range(3):
        page.evaluate("window.scrollBy(0, window.innerHeight)")
        page.wait_for_timeout(500)

    # Click on a specific item (adjust the selector as needed)
    page.click('.s-result-item:nth-of-type(3)')  # Click the 3rd item in the results

    # Add additional actions here if needed
    browser.close()

if __name__ == '__main__':
    scrape()
