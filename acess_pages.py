import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

# Access environment variables
DATABASE_ID = os.getenv('DATABASE_ID')
NOTION_API_KEY = os.getenv('NOTION_API_KEY')


headers = {
    "Authorization" : "Bearer " + NOTION_API_KEY,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {"page_size": 100}
    response = requests.post(url , json = payload, headers = headers)
    data = response.json()
    results = []
    with open('db.json','w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    results = data['results']
    return results


pages = get_pages()
