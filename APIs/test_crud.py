import requests

BASE = "http://127.0.0.1:8000"

r = requests.post(f"{BASE}/books", json={"title": "Test Book", "author": "Me"}, timeout=10)
print("POST  :", r.status_code, r.json())
new_id = r.json()["id"]

r = requests.patch(f"{BASE}/books/{new_id}", json={"title": "Renamed"}, timeout=10)
print("PATCH :", r.status_code, r.json())

r = requests.put(f"{BASE}/books/{new_id}", json={"title": "Replaced", "author": "You"}, timeout=10)
print("PUT   :", r.status_code, r.json())

r = requests.delete(f"{BASE}/books/{new_id}", timeout=10)
print("DELETE:", r.status_code)

r = requests.get(f"{BASE}/books/{new_id}", timeout=10)
print("GET after delete:", r.status_code)   # expect 404