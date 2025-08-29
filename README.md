# python-web

## API
### Create env
```
cd ./api
python -m venv .venv
source .venv/bin/activate       
python3 -m .venv venv 
#pip install "fastapi[standard]"
pip freeze > requirements.txt
```
### Re-install env
```
cd ./api
pip install -r requirements.txt
```

### Recreate env
```
cd ./api
pip install -r requirements.txt
```

### Run locally - gunicorn ensure to reload web-page on changed source code
```
cd .
make run-api-local
```
Open links
* [healthz](http://localhost:8000/healthz)
* [swagger UI](http://localhost:8000/docs)
* [redocs](https://github.com/Redocly/redoc) [docs UI](http://localhost:8000/redocs)

#### Test API
* Create products
```
P1=$(curl localhost:8000/products --json '{"name":"test1", "price": 20.0}'|jq -r .product_id)
P2=$(curl localhost:8000/products --json '{"name":"test2", "price": 30.0}'|jq -r .product_id)
curl localhost:8000/products
curl localhost:8000/products/$P1
curl localhost:8000/products/$P2
```
* Create orders
```
ORDER_ID1=$(curl localhost:8000/orders --json '{"items":[{"product_id":"'$P1'","quantity":2},{"product_id":"'$P2'","quantity":10}]}'|jq -r .order_id)
curl localhost:8000/orders
curl localhost:8000/orders/$ORDER_ID1
```
 
### Build and run api docker image
```
cd ./api
docker build . -t api
docker run -it -p 8000:8000 api
```
Open the link [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Deactivate venv
```
deactivate
```