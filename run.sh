# uvicorn src.main:app --reload

while getopts s:u:p: option
do
  case "${option}" in
    s)secret_key=${OPTARG};;
    u)superuser_name=${OPTARG};;
    p)superuser_password=${OPTARG};;
  esac
done

sudo docker build -t erp-fastapi .
sudo docker run -d \
  --name erp-fastapi-dev \
  --env SECRET_KEY=$secret_key \
  --env USER_NAME=$superuser_name \
  --env USER_PASSWORD=$superuser_password \
  -p 80:80 \
  erp-fastapi
sudo docker logs -f erp-fastapi-dev
