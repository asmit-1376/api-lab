import requests

# Query parameter: same as ?userId=1 in the URL
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params={"userId": 1},
    timeout=10,
)

if response.status_code == 200:
    posts = response.json()
    print("User 1 wrote", len(posts), "posts")
    print("First title:", posts[0]["title"])
else:
    print("Something went wrong:", response.status_code)