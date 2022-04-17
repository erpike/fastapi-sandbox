### FastApi Sandbox project by Erpike

##### quickstart:

1. bash run: (port=80)
   - `run.sh`
      - builds docker image
      - starts docker container
      - shows log

2. python run: (port=8000)
   - `guvicorn main:app`
     - flag: `--reload` (restart server on code update)

- available addresses:
  - http://127.0.0.1:port/docs
  - http://127.0.0.1:port/redoc
