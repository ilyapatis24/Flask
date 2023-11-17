import requests


# data = requests.post(f"http://127.0.0.1:5000/adverts/", json={
#     "title": "Golden Gate Bridge in San Francisco",
#     "description": "Very huge and beautiful bridge",
#     "owner": "Ivan"
# })
# print(data.status_code)
# print(data.json())

data = requests.get(f"http://127.0.0.1:5000/adverts/1/")
print(data.status_code)
print(data.json())

# data = requests.delete(f"http://127.0.0.1:5000/adverts/1/")
# print(data.status_code)
# print(data.json())