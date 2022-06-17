import requests
url = "http://127.0.0.1:5002/tasks"
# headers={'x-api-key':'09ba90f6-dcd0-42c0-8c13-5baa6f2377d0'}
resp = requests.get(url)
posts = requests.post(url)
print(resp.content)
print(posts.content)


