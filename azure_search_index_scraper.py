import requests
from bs4 import BeautifulSoup
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import ComplexField, SearchIndex, SearchFieldDataType, SimpleField, edm

# Configuration
url = "https://example.com"
search_service_endpoint = "https://<your-search-service>.search.windows.net"
search_index_name = "example-index"
api_key = "<your-api-key>"

# Scrape URL
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
title = soup.title.string
body = soup.get_text()

# Index to Azure Search
search_client = SearchClient(endpoint=search_service_endpoint, index_name=search_index_name, credential=api_key)
index_client = SearchIndexClient(endpoint=search_service_endpoint, credential=api_key)

# Define the index
index = SearchIndex(
    name=search_index_name,
    fields=[
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="title", type=SearchFieldDataType.String),
        SimpleField(name="content", type=SearchFieldDataType.String)
    ]
)

# Create the index if it doesn't exist
index_client.create_or_update_index(index)

# Index the document
document = {"id": url, "title": title, "content": body}
search_client.upload_documents(documents=[document])
