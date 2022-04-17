FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src
COPY ./demo.db /app/demo.db

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
