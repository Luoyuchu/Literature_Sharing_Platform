
import json
import jwt
import requests
from requests.api import head


# r = requests.get("http://localhost:5000/hello")


scret = "asdgqer4yhadfert243557u1fasdfhj56qdgdgsjhsfgasgsdf"
headers = {'Content-Type': "application/json"}
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFhYUBxcS5jb20iLCJpYXQiOjE2MzAzNzYyOTQsImV4cCI6MTYzMDM5MDY5NH0.NijxZ3JzAj1ix7g2v4g42iRjffbH4mf9t7zPYz8TYUE"
headers['Authorization'] = "Bearer " + token

# data = json.dumps({
#     "username": "abc",
#     "passwd": "bbb",
#     "email": "aaa@qq.com"
# })
# r = requests.post("http://127.0.0.1:5000/auth/signup", data=data, headers = headers)


# data = json.dumps({
#     "username": "abc",
#     "passwd": "UUU",
#     "email": "aaa@qq.com"
# })
# r = requests.post("http://127.0.0.1:5000/auth/login", data=data, headers = headers)


# data = json.dumps({
#     "new_passwd": "UUU",
#     "old_passwd": "UUU",
#     "email": "aaa@qq.com"
# })
# r = requests.post("http://127.0.0.1:5000/auth/changepasswd", data=data, headers = headers)


# data = json.dumps({
#     "paper_id": "6128cf22261db5c81b66c01b",
#     "user_id": "612ca9cccf134b2d864c6ea9",
#     "rating": 10
# })
# r = requests.post("http://127.0.0.1:5000/rating/update", data = data, headers=headers)


# data = json.dumps({
#     "_id": "",
#     "paper_id": "6128cf22261db5c81b66c01b",
#     "user_id": "612ca9cccf134b2d864c6ea9",
#     "content": '''asdfasdf \n asdfasdf \n asdfasdfasdfasdf###<he>\asdfasdgas''',
#     "public": False
# })
# r = requests.post("http://127.0.0.1:5000/note/update",
#                   data=data, headers=headers)

r = requests.get(
    "http://127.0.0.1:5000/note/query?paper_id=6128cf22261db5c81b66c01b&user_id=612ca9cccf134b2d864c6ea9")

# r = requests.get("http://127.0.0.1:5000/rating/query?paper_id=6128cf22261db81b66c01b", headers=headers)
print(r)
print(r.content)


# print(jwt.decode(token, key=scret, algorithms=["HS256"]))
