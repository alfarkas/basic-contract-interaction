# Python/flask sample contract interaction application
Basic contract interaction with a blockchain contract
This is just a sample application to interact with a contract in polygon mumbai chain.

This is not intended to be used in production, if you do, you'll risk your self and other to expose their private keys.

# Setup
```
pipenv shell
pipenv install
```
You can now just go into the python console inside the environment and try the functions by them self or, you can run the flask app to try it with a rest api.
```
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run
```

#### Run service
```
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_APP=service.py
flask run --host=0.0.0.0 -p 5001
```

If the provider network is not working, you can change it by creating a .env file from the .env.example and setting up there a different provider (one from mumbai).

# Poll product creation events
```
pipenv shell
ipython
```
```python
from src.event_subscription import polling_new_products
polling_new_products()
```
Now create a new product in another console or with the flask api, and see it printed out in the console.

## Run tests

```
pytest src/tests
```

#### TODO
- Dockerize repo