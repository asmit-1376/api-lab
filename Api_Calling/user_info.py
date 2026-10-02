import requests

response = requests.get("https://jsonplaceholder.typicode.com/users/1")
user = response.json()

print("Name:", user["name"])
print("Email:", user["email"])
print("City:", user["address"]["city"])
print("Company:", user["company"]["name"])
