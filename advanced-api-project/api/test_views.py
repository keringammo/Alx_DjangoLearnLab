import requests

BASE_URL = "http://localhost:8000/api/books/"
TOKEN = "your_auth_token_here"
HEADERS_AUTH = {"Authorization": f"Token {TOKEN}"}
HEADERS_NO_AUTH = {}  # No auth

# List all books (anyone)
response = requests.get(BASE_URL, headers=HEADERS_NO_AUTH)
print("List Books:", response.status_code, response.json())

# Get single book (anyone)
book_id = 1
response = requests.get(f"{BASE_URL}{book_id}/", headers=HEADERS_NO_AUTH)
print("Book Detail:", response.status_code, response.json())

# Create a book (auth required)
new_book = {"title": "New Book", "publication_year": 2025, "author": 1}
response = requests.post(f"{BASE_URL}create/", json=new_book, headers=HEADERS_AUTH)
print("Create Book:", response.status_code, response.json())

# Update a book (auth required)
update_data = {"title": "Updated Book", "publication_year": 2024, "author": 1}
response = requests.put(f"{BASE_URL}{book_id}/update/", json=update_data, headers=HEADERS_AUTH)
print("Update Book:", response.status_code, response.json())

# Delete a book (auth required)
response = requests.delete(f"{BASE_URL}{book_id}/delete/", headers=HEADERS_AUTH)
print("Delete Book:", response.status_code)
