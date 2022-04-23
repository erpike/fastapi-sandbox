### FastApi Sandbox project by Erpike

#### Quickstart:

1. bash run: (port=80)
   - `bash run.sh -s your_secret_key`
     - builds docker image
     - starts docker container
     - shows log

2. python run: (port=8000)
   - `uvicorn main:app`
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
