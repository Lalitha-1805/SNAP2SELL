import requests
BASE='http://localhost:5000/api'
# Login farmer
r = requests.post(BASE+'/auth/login', json={'email':'test_farmer@example.com','password':'secret123'})
print('LOGIN', r.status_code, r.text)
respj = r.json()
print('TOKENTYPE keys:', list(respj.keys()))
token = respj.get('access_token')
print('TOKEN LEN', len(token) if token else None)
headers={'Authorization':f'Bearer {token}'}
# Create product
prod={'name':'DebugProduct','category':'Vegetables','description':'debug','price':60,'quantity':10}
resp = requests.post(BASE+'/products', json=prod, headers=headers)
print('CREATE', resp.status_code, resp.text)
