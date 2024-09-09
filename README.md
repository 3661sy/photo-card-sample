# Photo-Card-Sample

## Environments

- Language
  - Python 3.10
- Framework
  - Django 4.2.16
  - DRF 3.15.2
  - djangorestframework-simplejwt 5.3.1

## Install Env

```shell
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Set Test Data

```shell
python3 manage.py migrate
python3 manage.py loaddata example.json
```