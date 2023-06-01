#!/bin/bash
set -e

cd /opt/star-burger/
git reset --hard -q HEAD
git pull -q

source venv/bin/activate

pip install -q -r requirements.txt

./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

yes yes | python manage.py collectstatic > NUL

python manage.py migrate > NUL

systemctl restart starburger.service

echo "Deployment completed successfully"

source .env

curl --request POST \
     --url https://api.rollbar.com/api/1/deploy \
     --header 'X-Rollbar-Access-Token: '$ROLLBAR_TOKEN\
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data "
{
  \"environment\": \"production\",
  \"revision\": \"$(git rev-parse HEAD)\",
  \"rollbar_username\": \"o.panova27\",
  \"local_username\": \"semellot\",
  \"status\": \"succeeded\"
}
"
