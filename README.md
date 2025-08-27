# python-web

## API
```
cd ./api
python3 -m venv venv 
source venv/bin/activate       
pip install "fastapi[standard]"
pip freeze > requirements.txt
```

### Recreate env
```
cd ./api
pip install -r requirements.txt
```

### Run locally
```
cd .
make run-api-local
```

### Deactivate venv
```
deactivate
```