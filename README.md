
# **Links register app**

> :alembic: This application is a POC of my abilities and skills


## :construction: Install

*  Create virtual enviroment for application

```sh
python3 -m venv myvenv
```

* Download packages from requirements.txt

```sh
pip install -r requirements.txt
```

* Configure your redis-server configuration inside `link_saver.settings`
    * REDIS_HOST - Host of redis
    * REDIS_PORT = Port of redis


## :rocket: Usage

```sh
python manage.py runserver
```

## :white_check_mark: Run tests

```sh
python manage.py test
```

<!--
[TODO] If project is deployed to DockerHub:

## :whale: Supported tags

[Dockerhub monogramm/__app_slug__](https://hub.docker.com/r/monogramm/__app_slug__/)

* `latest`

-->

## :bust_in_silhouette: Authors

* [Aminov Emil](https://github.com/AminovE99)


## :zap: Possible Enhancement
* :whale: Create docker-compose for app

## :page_facing_up: License

This project is [AGPL v3](uri_license) licensed.