
# User Microservice

Technology Stack : Fast API, SQLite and Auth0


## Installation

User management service

```bash
  cd project name
```
Create a virtualenv to prevent any conflicts

```bash
  virtualenv venv
  venv/bin/activate
```
Install all the dependencies
```bash
  run pip install -r requirements.txt
```

Start the Fast API app 

```bash
  uvicorn app.main:app --reload
```

## Testing

After starting the FAST API app you can test it at http://127.0.0.1:8000/docs or there are test cases written for all the API's just in the /tests directory and you can run the test scripts by executing pytest test_filename.py in your terminal

