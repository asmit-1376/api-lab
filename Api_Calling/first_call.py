import requests

response = requests.get("https://jsonplaceholder.typicode.com/users/1")

print("Status code:", response.status_code)
print("Raw text:", response.text)