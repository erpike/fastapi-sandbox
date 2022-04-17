FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

RUN apt-get update && apt-get install -y vim

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./src /app/src
# VOLUME ./demo.db /demo.db  TODO: define why not work?

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
