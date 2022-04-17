# uvicorn src.main:app --reload

sudo docker build -t erp-fastapi .
sudo docker run -d --name erp-fastapi-dev -p 80:80 erp-fastapi
sudo docker logs -f erp-fastapi-dev

sudo docker rm erp-fastapi-dev --force
sudo docker rmi erp-fastapi