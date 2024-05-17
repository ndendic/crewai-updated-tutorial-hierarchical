import os
from notion_client import Client
from notion_client import helpers
import instructor
from pydantic import BaseModel
from openai import OpenAI

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    print("Could not load .env because python-dotenv not found.")
else:
    load_dotenv()
# Define your desired output structure
class SearchResult(BaseModel):
    name: str
    content: str
    type: str


# Patch the OpenAI client
# client = instructor.from_openai(OpenAI()) 
# query = input("Query:")

# Extract structured data from natural language

token = os.environ['NOTION_TOKEN']
# token = 'secret_iGUKBFJBfRc6QLYpJ7le1JMPNsUq0VJNWFbI3RRR4Qj'
notion = Client(auth=token)

# # print(notion.search(query=query)) 
# result = 'Done'
# task_name = input("Enter task name: ")
# start_date = input("Enter start date (YYYY-MM-DD): ")
# new_page = {
#     "Name": {"title": [{"text": {"content": task_name}}]},
#     "Do Date": {"date": {"start": start_date}},
#     "Done": {"checkbox": False},
#     "Status": {"status": {"name": "Not Planned"}},
#     "Priority": {"select": {"name": "Low"}}
# }
# created_page = notion.pages.create(parent={"database_id": "836f0824-9dcc-4e16-ab64-a98f8d42abb0"}, properties=new_page)
# print(f"Task '{task_name}' created successfully with ID: {created_page['id']}")
# https://www.notion.so/ndendic/71524950fd7b47f9a005445749018b0c?v=0ad9c3fa17cd46219f0c3f8fcb95d459&pvs=4

# database_id = "836f08249dcc4e16ab64a98f8d42abb0"
database_id = "71524950fd7b47f9a005445749018b0c"

# notion.pages.create(parent={"database_id": "836f08249dcc4e16ab64a98f8d42abb0"}, properties={"Name": {"title": [{"text": {"content": "Task"}}]}})
result = notion.search(query = "Projects", filter = {"property": "object", "value": "database"})
print(result)

def create_notion_task(database_id, notion_token = token):
    # Get the database schema
    response = notion.databases.retrieve(database_id)
    database = response
    
    properties = database['properties']
    new_page_properties = {}

    for prop_name, prop_info in properties.items():
        prop_type = prop_info['type']
        if prop_type == 'title':
            content = input(f"Enter {prop_name}: ")
            if content != "" : new_page_properties[prop_name] = {"title": [{"text": {"content": content}}]}
        elif prop_type == 'date':
            content = input(f"Enter {prop_name} (YYYY-MM-DD): ")
            if content != "" : new_page_properties[prop_name] = {"date": {"start": content}}
        elif prop_type == 'checkbox':
            content = input(f"Is {prop_name} true or false? ").lower() == 'true'
            if content != "" : new_page_properties[prop_name] = {"checkbox": content}
        elif prop_type == 'status':
            content = input(f"Enter {prop_name} (Not Planned, Planned, Done, Archived): ")
            if content != "" : new_page_properties[prop_name] = {"status": {"name": content}}
        elif prop_type == 'select':
            content = input(f"Enter {prop_name}: ")
            if content != "" : new_page_properties[prop_name] = {"select": {"name": content}}
        elif prop_type == 'multi_select':
            content = input(f"Enter {prop_name} (comma separated): ").split(',')
            if content != [""] : new_page_properties[prop_name] = {"multi_select": [{"name": item.strip()} for item in content]}
        elif prop_type == 'relation':
            content = input(f"Enter {prop_name} (related record ID): ")
            if content != "" : new_page_properties[prop_name] = {"relation": [{"id": content}]}
        elif prop_type == 'people':
            content = input(f"Enter {prop_name} (user ID): ")
            if content != "" : new_page_properties[prop_name] = {"people": [{"id": content}]}
        elif prop_type == 'rich_text':
            content = input(f"Enter {prop_name}: ")
            if content != "" : new_page_properties[prop_name] = {"rich_text": [{"text": {"content": content}}]}
        elif prop_type == 'number':
            content = input(f"Enter {prop_name}: ")
            if content != "" : new_page_properties[prop_name] = {"number": float(content)}
        elif prop_type == 'url':
            content = input(f"Enter {prop_name} URL: ")
            if content != "" : new_page_properties[prop_name] = {"url": content}
        elif prop_type == 'email':
            content = input(f"Enter {prop_name} Email: ")
            if content != "" : new_page_properties[prop_name] = {"email": content}
        elif prop_type == 'phone_number':
            content = input(f"Enter {prop_name} Phone Number: ")
            if content != "" : new_page_properties[prop_name] = {"phone_number": content}
        elif prop_type == 'formula':
            print(f"Skipping {prop_name} (formula) as it is automatically computed.")
        elif prop_type == 'created_time':
            print(f"Skipping {prop_name} (created_time) as it is automatically set.")
        elif prop_type == 'created_by':
            print(f"Skipping {prop_name} (created_by) as it is automatically set.")
        elif prop_type == 'last_edited_time':
            print(f"Skipping {prop_name} (last_edited_time) as it is automatically set.")
        elif prop_type == 'last_edited_by':
            print(f"Skipping {prop_name} (last_edited_by) as it is automatically set.")

    # Create the new page
    print(f"DATABASE ID: {database_id}")

    response = notion.pages.create(parent={"database_id": database_id}, properties=new_page_properties) #, headers=headers)
    created_page = response

    print(f"Task created successfully with ID: {created_page['id']}")

# Usage
create_notion_task(database_id)

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