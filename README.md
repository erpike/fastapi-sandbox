### FastApi Sandbox project by Erpike

#### Quickstart:

1. bash run: (port=80)
   - `bash run.sh -s your_secret_key -u username -p password`
     - builds docker image
     - starts docker container
     - shows log

2. python run: (port=8000)
   - create .env file and set `USER_NAME` & `USER_PASSWORD` variables
   - run `uvicorn main:app`
     - flag: `--env-file PATH` Environment configuration file.
     - flag: `--reload` (restart server on code update)

- available addresses:
  - http://127.0.0.1:{port}/docs (swagger)
  - http://127.0.0.1:{port}/redoc (ReDoc)

- additive commands:
  - `bash clean-docker.sh` (cleans created doker image and container)

##### Little theory:

Key `FastAPI` features:
- automatic documentation
  - `swagger`
  - `ReDoc`
- security and authentication
- dependency injection
  - Objects don't create each other, but provide a way to inject the needed dependencies instead.
- testing
