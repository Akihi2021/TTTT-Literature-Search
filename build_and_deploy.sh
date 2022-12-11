docker build -t vinok/tttt .

docker push vinok/tttt:latest

chmod 777 ./login_and_deploy.sh

./login_and_deploy.sh