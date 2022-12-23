import requests
import sqlite3
import random

base_url = 'http://localhost:5000'

print("Testing /")
print(20*'-')

response = requests.get(base_url)

print(response.status_code)
print(response.text)

print("\nTesting /add POST")
print(20*'-')

data = { "entry_id": random.randint(0,10), "entry_title": "test_entry_title" }

response = requests.post(base_url+'/add', data=data)
print(response.status_code)
print(response.text)

print("\nTesting /add GET")
print(20*'-')

response = requests.get(base_url+'/add')
print(response.status_code)
print(response.text)

print("\nTesting db write")
print(20*'-')

con = sqlite3.connect('mylar.db')
cur = con.cursor()
cur.execute('SELECT * FROM entries')
res = cur.fetchall()
print(res)

con.close()
