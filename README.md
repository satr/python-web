# Example on Python
* FastAPI: REST API, GraphQL
* Flask: Web-app
* SQL: PostgreSQL
* Containers: Docker, Docker compose

## API
### Create env
```
cd ./api
python -m venv .venv
source .venv/bin/activate       
pip install -r requirements.txt
# Run following command when changed requirements.txt
# pip freeze > requirements.txt
```
### Re-install env
```
cd ./api
pip install -r requirements.txt
```

### Run locally - gunicorn ensure to reload web-page on changed source code
```
cd <repo-root>
make run-api-local
```
Open links
* [healthz](http://localhost:8000/healthz)
* [swagger UI](http://localhost:8000/docs)
* [redocs](https://github.com/Redocly/redoc) UI [docs](http://localhost:8000/redocs)
* [OpenAPI](https://www.openapis.org/) [schema](http://localhost:8000/openapi.json)

#### Test API
* Create and get products with REST API
  * create
    ```
    P1=$(curl localhost:8000/products --json '{"name":"test1", "price": 20.0}'|jq -r .id)
    P2=$(curl localhost:8000/products --json '{"name":"test2", "price": 30.0}'|jq -r .id)
    ```
  * get
    ```
    curl localhost:8000/products
    curl localhost:8000/products/$P1
    curl localhost:8000/products/$P2
    ```
* Create and get products with GraphQL
  * create
    ```
    curl -X 'POST' 'http://localhost:8000/graphql/' \
      -H 'accept: application/json' -H 'Content-Type: application/json' \
      -d '{
        "query": "mutation CreateProduct($input: CreateProductInput!) { create_product(input: $input) { id }}",
        "variables": { "input": {"name": "p1","price": 19.99 }}
        }'
    ```
  * get
    ```
    curl -X 'POST' 'http://localhost:8000/graphql/' \
      -H 'accept: application/json' -H 'Content-Type: application/json' \
      -d '{"query": "{products{name,id,price,description,created_at,updated_at}}"
    }'
    
    curl -X 'POST' 'http://localhost:8000/graphql/' \
      -H 'accept: application/json' -H 'Content-Type: application/json' \
      -d '{"query": "{product(id:\"064f529a-b5f8-4c24-a8af-92f6c931aab2\"){id,name}}"}'
    
    curl -X 'POST' 'http://localhost:8000/graphql/' \
      -H 'accept: application/json' -H 'Content-Type: application/json' \
      -d '{"query": "{product(name:\"my-product1\"){id,name}}"}'
    ```
* Create orders with REST API
```
ORDER_ID1=$(curl localhost:8000/orders --json '{"items":[{"id":"'$P1'","quantity":2},{"id":"'$P2'","quantity":10}]}'|jq -r .order_id)
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

### Generate API client for flask-app
* Run API locally
* [Re-]Generate API client
```
make gen-api-client
```

### Build and run api and apps with docker compose
```
docker compose up
```
Open the link [http://127.0.0.1:8001](http://127.0.0.1:8001)

## Run RabbitMQ locally
```
make run-mq
#or
docker run -it -p 5672:5672 -p 15672:15672 --name rabbitmq --rm rabbitmq:3-management
```
* Open the Dashboard link [http://localhost:15672/](http://localhost:15672/), user: guest, password: guest
