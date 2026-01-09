import requests, sys, time
BASE='http://localhost:5000/api'

def post(path, data, token=None):
    headers={'Content-Type':'application/json'}
    if token: headers['Authorization']=f'Bearer {token}'
    r = requests.post(BASE+path, json=data, headers=headers, timeout=10)
    print('\nPOST', path, '=>', r.status_code)
    print(r.text)
    return r

def get(path, token=None):
    headers={}
    if token: headers['Authorization']=f'Bearer {token}'
    r = requests.get(BASE+path, headers=headers, timeout=10)
    print('\nGET', path, '=>', r.status_code)
    print(r.text)
    return r

try:
    # Health
    print('Health:')
    h = requests.get('http://localhost:5000/api/health', timeout=5)
    print(h.status_code, h.text)

    # Signup consumer
    consumer = {'name':'API Consumer','email':'test_consumer@example.com','password':'secret123','role':'consumer','phone':'9990001111','address':'Demo Address'}
    try:
        r1=post('/auth/signup', consumer)
    except Exception as e:
        print('Signup consumer error', e)

    # Signup farmer
    farmer = {'name':'API Farmer','email':'test_farmer@example.com','password':'secret123','role':'farmer','phone':'8880001111','address':'Farm Address'}
    try:
        r2=post('/auth/signup', farmer)
    except Exception as e:
        print('Signup farmer error', e)

    # Login farmer
    lf = post('/auth/login', {'email':farmer['email'],'password':farmer['password']})
    tf = lf.json()
    farmer_token = tf.get('access_token')

    # Create product as farmer
    prod = {
        'name':'Test Tomato','category':'Vegetables','description':'Fresh tomatoes','price':50,'quantity':100
    }
    pcreate = post('/products', prod, token=farmer_token)
    pid = None
    try:
        pid = pcreate.json().get('product_id')
    except Exception:
        print('Could not parse product create response')

    # Login consumer
    lc = post('/auth/login', {'email':consumer['email'],'password':consumer['password']})
    tc = lc.json()
    consumer_token = tc.get('access_token')

    # Create order as consumer
    if pid:
        order = {
            'items':[{'product_id': pid, 'quantity':2}],
            'shipping_address':'Consumer Address'
        }
        o=create = post('/orders', order, token=consumer_token)
    else:
        print('Skipping order because no product id')

    # Create review as consumer
    if pid:
        review = {'product_id': pid, 'rating':5, 'comment':'Great product!'}
        rrev = post('/reviews', review, token=consumer_token)

    print('\nSmoke test complete')
except Exception as e:
    print('Smoke test exception', e)
    sys.exit(1)
