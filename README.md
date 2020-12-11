# foodgram-project
foodgram-project

Для DEV!
1) База разработки - PostgreSql (fixtures.json в корне совместима только с ней) - сделать с помощью docker-compose, в .env файл DB_HOST - записать свой IP (docker inspect foodgram_db покажет текущий IP), затем python manage.py migrate, python manage.py loaddata --exclude auth.permission --exclude contenttypes fixtures.json
2) Если своя чистая база (не postgres). Подключить базу, Сделать migrate, выполнить python manage.py add_ingredients и python manage.py add_tags (заполняет необходимые поля тэгов и преднабор ингредиентов)
