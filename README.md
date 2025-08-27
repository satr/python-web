# python-web

## API
```
source venv/bin/activate       
cd ./api
python3 -m venv venv 
pip install "fastapi[standard]"
pip freeze > requirements.txt
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
* [root](http://127.0.0.1:8000)
* [item](http://localhost:8000/items/12?q=value)


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