import os
from notion_client import Client
from pydantic import Field
from langchain.tools import tool
from pprint import pprint
import typing
import json
# from tools import Tool
NOTION_TOKEN = 'secret_iGUKBFJBfRc6QLYpJ7le1JMPNsUq0VJNWFbI3RRR4Qj'

notion = Client(auth=NOTION_TOKEN)

class Notion():
    # query: str = Field(..., description="The query to search for")

    @tool("Search the Notion")
    def search_notion(query: str):
        '''Usefull when you need to seaerch Notion for a query on notion pages and databases.
        If no query param is provided, then the response contains all pages or databases that have been shared with the integration. 
        '''''
        print("Searching the Notion...")
        search_results = notion.search(query=query)
        results = search_results["results"]
        
        trimmed_results = [
        {
            "object": result["object"],
            "id": result["id"],
            "properties": result["properties"],
        }
        for result in results
        ]
        # Convert to JSON
        json_results = json.dumps(trimmed_results)

        return json_results
    @tool("Crate page in Notion")
    def crete_task(task: str):
        notion.pages.create(task=task)