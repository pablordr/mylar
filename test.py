import requests

print("Testing /")
print(20*'-')

response = requests.get('http://localhost:5000')

print(response.status_code)
print(response.text)

print("\nTesting /filewrite")
print(20*'-')

response = requests.get('http://localhost:5000/filewrite')

print(response.status_code)
print(response.text)

print("\nTesting /fileread")
print(20*'-')

response = requests.get('http://localhost:5000/fileread')

print(response.status_code)
print(response.text)


