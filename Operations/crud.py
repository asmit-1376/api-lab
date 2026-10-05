import requests

BASE = "https://jsonplaceholder.typicode.com"

# CREATE (POST)
new_post = {"title": "Hello", "body": "From Python", "userId": 1}
r = requests.post(f"{BASE}/posts", json=new_post, timeout=10)
print("POST  :", r.status_code, r.json())

# REPLACE (PUT)
full_post = {"id": 1, "title": "New title", "body": "New body", "userId": 1}
r = requests.put(f"{BASE}/posts/1", json=full_post, timeout=10)
print("PUT   :", r.status_code, r.json())

# PARTIAL UPDATE (PATCH)
r = requests.patch(f"{BASE}/posts/1", json={"title": "Patched"}, timeout=10)
print("PATCH :", r.status_code, r.json())

# DELETE
r = requests.delete(f"{BASE}/posts/1", timeout=10)
print("DELETE:", r.status_code, r.json())