# uvicorn src.main:app --reload

while getopts s: option
do
  case "${option}" in
    s)secret_key=${OPTARG};;
  esac
done

sudo docker build -t erp-fastapi .
sudo docker run -d --name erp-fastapi-dev --env SECRET_KEY=$secret_key -p 80:80 erp-fastapi
sudo docker logs -f erp-fastapi-dev
