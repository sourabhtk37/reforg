
# Reforg

A Key value store service with server and client(cli) programs
## Features
- Http server for adding, updating and fetching key:value pair
- LRU cache implementation for quick access to data
- Uses unix dbm interface for persistent storage
- FastAPI provides openAPI docs (also known as swagger API)
- Cli client for making http calls to the server endpoints
- Watch a particular key for changes


  
## API Reference
API docs and reference are also available via openAPI spec which can be access at: http://<server-ip>/docs

#### Get key

```http
  GET /api/v1/keys?key=key
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `key`      | `string` | **Required**. "key" you are trying to access  |

#### Put key value

```http
  PUT /api/v1/keys?key=key&value=value
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `key`      | `string` | **Required**. Key to update |
| `value`    | `string` | **Required**. value to be updated corresponding to the key  |


#

# Deployment

To deploy this project run

```bash
  git clone https://github.com/sourabhtk37/reforg.git
  cd reforg/
  docker build -t reforg .      # Creates an image
  docker run -d --name reforg-container -p 80:80 reforg   # run container with port mapping on 80/tcp
```
Your application would be accessible from `127.0.0.1(localhost)` and NIC interface ip.


  
## Installation 

Install my-project with npm

```bash
cd reforg/
python3 -m venv venv    # Create a virtual env (optional)
source venv/bin/activate  # activate venv
pip install -r requirements.txt
```
    
## Usage/Examples for cli
You can access http server endpoints via cli client as well: 

```bash
python reforg/cli.py -h
usage: http client [-h] [-url http_api_url] [-get Key] [-put Key Value] [-watch Key] [-interval seconds]

Call HTTP endpoints for a key value store service

optional arguments:
  -h, --help         show this help message and exit
  -url http_api_url  Api server url
  -get Key           Retreive key from server, eg: -get a
  -put Key Value     Add key:value to server, eg: -put a b
  -watch Key         Watch key for changes, eg: -watch a
  -interval seconds  Set watch/poll interval for watch option
```

## Documentation

##### Directory Structure
```
.
├── kvstore   # Data Store implementing LRU cache
│   ├── core.py
├── reforg    # cli client 
│   ├── cli.py
│   ├── http_client.py
│   ├── __init__.py
├── server    # http API server
│   ├── main.py
└── tests
├── requirements_reforg.txt  # requirements for the 
├── setup.py
├── LICENSE
├── logging.conf
├── README.md
├── Dockerfile

8 directories, 18 files
```
## Issues/Optimizations

- In case of deployment via gunicorn or similar servers that spins up multiple workers, 
  multiple instances of the python objects could be created which cause data consistency 
  as each instance would have it's own copy of data. 
  To solve this:
  - Implement redis for storing the key:value store in memory therefore involving IPC between
    worker processes.
  - Another similar alternative is to Implement `multiprocessing.connection` module in python.
    Which also involves IPC.