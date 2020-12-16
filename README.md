###### Foodgram - Учебный проект Яндекс Практикум

![Workflow check](https://github.com/mechnotech/foodgram-project/workflows/Foodgram/badge.svg)

Адрес: http://food-gram.ru

**Описание проекта:**

Foodgram это сервис рецептов. После регистрации, можно создавать свои рецепты, подписываться на других пользовтелей, добавлять рецепты в избранное. А так же планировать покупки нужных инградиентов.

Сервис использует
базу данных [Postgresql](https://www.postgresql.org), вебсервер [NGINX](https://nginx.org), бекэнд [Django](https://www.djangoproject.com) упакованых в отдельных контейнерах Docker.
Данные, статика и медиафайлы проброшены на хост машину в виде Volumes.

**Для старта с нуля:**

Установка автоматическая при push в репозиторий Github с помощью Github Workflow (см файл foodgram-workflow.yaml в папке .github/workflow!)
В нем описаны переменные типа ${{ secrets.SOME_VAR }} - эти переменные надо задать в разделе settings репозитория Github

Пример secrets.ENV (Переменая будет импортирована на VPS и в контейнер с Django при deploy)

>DB_ENGINE=django.db.backends.postgresql
>
>DB_NAME=foodgram
>
>POSTGRES_USER=foodgram
>
>POSTGRES_PASSWORD=###password###
>
>DB_HOST=db
>
>DB_PORT=5432
>
>SECRET_KEY='######'
>
>MAILGUN_API_KEY='3c1b36a*****************-*******dae4a3'
>
>MAILGUN_WEBHOOK_SIGNING_KEY='3c1b36a*****************-*******dae4a3'

Перед тем как приступить к разворачиванию проекта, необходимо создать VPS(виртуальный сервер) c доступом по ключу SSH (для теста был выбран Яндекс.Облако)
После создания виртуалной машины, необходимо подготовить её:
- нужно зайти на VPS, посмотреть на консоль и, глубоко вздохнув, продолжить
- установить git, docker, docker-compose `sudo apt install -y docker.io docker-compose git`

Теперь VPS готов принмать автоматические обновления при изменениях в master ветке Github (миграция изменений БД настроена выполняться автоматически при каждом обновлении)

Если необходимо создать суперпользователя для админки Django, то после первого деплоя, нужно зайти в работающий контейнер c Django `sudo docker exec -it foodrgam_web bash`
и внутри него выполнить:

- `python manage.py createsuperuser` (по желанию, чтоб управлять через админку)
- `python manage.py loaddata --exclude auth.permission --exclude contenttypes fixtures.json` - (по желанию, заполняет тестовыми данными базу данных. ВАЖНО! выполнять только для первого деплоя, иначе удалит все текущие данные в базе данных проекта)
- `exit` - для выхода из контейнера

Сервис будет доступен по основному IP адресу (или домену) сайта

Админка _IP-adress_/admin

**Для разработчиков!**

Есть набор пресетов данных для чистой базы. Для этого нужно:

Подключить базу, Сделать migrate, выполнить `python manage.py add_ingredients` и `python manage.py add_tags` (заполняет необходимые поля тэгов и преднабор ингредиентов)

Можно удалять существующие и создавать свои теги для фильтрации рецептов по тегу и создания/редактирования рецептов, для этого:

Зайти в админку Django, создать Тэг, заполнив три поля. (Пример заполнения: tag - Бранч, color - yellow, slug - branch)
Изменения отобразятся сразу на страницах проекта после установки нового тега. 

В settings.py в режиме DEBUG=True, дефолтная база указана как SQLite, в боевом режиме - PostgreSql

Почтовый сервис в боевом режиме - MailGun (настроен для Европейской зоны!)

----

Над проектом работал: Евгений Шумилов
 
По вопросам развития и поддержки пишите: в Гитхаб!