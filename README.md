# foodgram-project
foodgram-project

Для DEV
1) Тестовая db - postgressql (fixtures.json в корне) - сделать с помощью docker-compose, в .env файл DB_HOST - записать свой IP (docker inspect foodgram_db покажет текущий IP)
2) Если своя чистая база (не postgres). Подключить, Сделать migrate, выполнить python manage.py add_ingredients и python manage.py add_tags
