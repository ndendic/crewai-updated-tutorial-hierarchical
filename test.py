import os
from notion_client import Client
import instructor
from pydantic import BaseModel
from openai import OpenAI


# Define your desired output structure
class SearchResult(BaseModel):
    name: str
    content: str
    type: str


# Patch the OpenAI client
client = instructor.from_openai(OpenAI()) 
query = input("Query:")

# Extract structured data from natural language

#> 30

token = os.environ['NOTION_TOKEN']
notion = Client(auth=token)

# print(notion.search(query=query)) https://www.notion.so/ndendic/836f08249dcc4e16ab64a98f8d42abb0?v=a6d1ba45f1c1478592c73db9473f83f3&pvs=4
result = notion.databases.query(database_id="836f08249dcc4e16ab64a98f8d42abb0",query=query)
print(result)

# search_result = client.chat.completions.create(
#     model="gpt-4-1106-vision-preview",
#     response_model=SearchResult,
#     messages=[{"role": "system","content": "sort notion query result into meaningfull data"},
#               {"role": "user", "content": result.__str__()}],
# )

# print(search_result.name)
# #> John Doe
# print(search_result.content)
# print(search_result.type)