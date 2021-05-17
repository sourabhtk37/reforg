__author__ = "T K Sourab <sourabhtk37@gmail.com>"


from fastapi import FastAPI, Response
from kvstore.core import KvStore

app = FastAPI()
kv_store = KvStore(capacity=999)


@app.get("/")
def root():
    return {"message": "Hello!"}


@app.get("/api/v1/keys")
def get_key(key: str, response: Response):
    """Retreive value corresponding to the key"""
    value = kv_store.get(key)
    if value:
        return {"key": key, "value": value}
    else:
        response.status_code = 404


@app.put("/api/v1/keys")
def put_key(key: str, value: str):
    """Update key:value pair"""
    kv_store.put(key, value)
    
