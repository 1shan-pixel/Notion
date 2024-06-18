import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
PAGE_ID = os.getenv('NOTION_PAGE_ID')

notion = Client(auth=NOTION_API_KEY)

def retrieve_block_children(page_id):
    print("Retrieving blocks (async)...")
    blocks = []
    start_cursor = None

    while True:
        response = notion.blocks.children.list(block_id=page_id, start_cursor=start_cursor)
        blocks.extend(response['results'])
        if not response.get('has_more'):
            break
        start_cursor = response['next_cursor']

    return blocks

def print_block_details(blocks):
    print("Displaying specific block content:")
    for block in blocks:
        if block['type'] == 'paragraph':
            for text in block.get('paragraph', {}).get('rich_text', []):
                print(text.get('text', {}).get('content', ''))
    print("-" * 40)

def create_new_block(page_id, content):
    new_block = notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content
                            }
                        }
                    ]
                }
            }
        ]
    )
    return new_block
def main():
    blocks = retrieve_block_children(PAGE_ID)
    print_block_details(blocks)

    # Add a new block with specific content
    new_content = "Inserted text …."
    new_block = create_new_block(PAGE_ID, new_content)
    print("New block added successfully with content:", new_content)

if __name__ == "__main__":
    main()
