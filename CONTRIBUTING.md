# Contributing

## Local Development

```
git clone https://github.com/arueth/cloudrun-web-django.git
cd cloudrun-web-django
```

```
sudo apt install libpq-dev python3-pip python3.10-venv
```

```
python3 -m venv .venv
```

```
source .venv/bin/activate
```

```
pip install -r requirements-dev.txt
pip install -r requirements.txt
```

```
cd src
```

```
LOCAL_DEV=true python manage.py migrate
```

```
LOCAL_DEV=true python manage.py runserver 0.0.0.0:8080
```

## Adding additional dev requirements

- Add packages to the `requirements-dev.in` file

```
pip-compile requirements-dev.in --output-file requirements-dev.txt 
git add requirements-dev.in requirements-dev.txt
```

## Adding additional requirements

- Add packages to the `requirements.in` file

```
pip-compile
git add requirements.in requirements.txt
```

## Local CloudRun Testing

- From the repository root directory where the `Dockerfile` and `local-service.dev.yaml` files are located

  ```
  gcloud beta code dev
  ```

### Troubleshooting

```
minikube -p gcloud-local-dev
```

## Local Development Testing

```
mkdir -p /cloudsql
cloud_sql_proxy -dir=/cloudsql -instances="<CLOUDSQL_CONNECTION_NAME>"

ENVIRONMENT=dev python manage.py migrate
ENVIRONMENT=dev python manage.py runserver 0.0.0.0:8080
```