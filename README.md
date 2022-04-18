### FastApi Sandbox project by Erpike

#### Quickstart:

1. bash run: (port=80)
   - `run.sh`
      - builds docker image
      - starts docker container
      - shows log

2. python run: (port=8000)
   - `uvicorn main:app`
     - flag: `--reload` (restart server on code update)

- available addresses:
  - http://127.0.0.1:{port}/docs (swagger)
  - http://127.0.0.1:{port}/redoc (ReDoc)


##### Little theory:

key `FastAPI` features:
- automatic documentation
  - `swagger`
  - `ReDoc`
- security and authentication
- dependency injection
- testing
