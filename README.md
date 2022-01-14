[![codecov](https://codecov.io/gh/alfarkas/basic-contract-interaction/branch/main/graph/badge.svg)](https://codecov.io/gh/alfarkas/basic-contract-interaction)


# Python/flask sample contract interaction application
Basic contract interaction with a blockchain contract
This is just a sample application to interact with a contract in polygon mumbai chain.

This is not intended to be used in production, if you do, you'll risk your self and other to expose their private keys.

# Setup
## Docker and Docker Compose installation

Install Docker:

- `https://docs.docker.com/install/`

After install Docker, proceed to install Docker Compose:

- `https://docs.docker.com/compose/install/`

## Build image
```bash
docker-compose -f docker-compose.yml build
```

## Project configuration
Copy the `.env.example` and complete it with your secrets.
```bash
cp .env.example .env
```
Replace any value if needed.

## Run
```bash
docker-compose -f docker-compose.yml up -d
```
Stop

```bash
docker-compose -f docker-compose.yml down
```

# Poll product creation events
```bash
docker exec -ti api ipython
```
```python
from src.event_subscription import polling_new_products
polling_new_products()
```
Now create a new product in another console or with the flask api, and see it printed out in the console.

## Run tests

```
docker exec -t api pytest src/tests
```
