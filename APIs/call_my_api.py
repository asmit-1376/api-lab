import requests

r = requests.get("http://127.0.0.1:8000/books", timeout=10)
print(r.status_code)

for book in r.json():
    print(book["id"], book["title"], "by", book["author"])