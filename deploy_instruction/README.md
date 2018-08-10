Деплой веб-приложения на связке Python 3, Django, Nginx, Gunicorn и Supervisor. Установку рассматриваю на Debian-Based системах.

 Установка всех необходимых пакетов.

   sudo apt-get update

sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx supervisor


Создаем базу данных и пользователя PostgreSQL. Переходим в интерактивную сессию PostgreSQL

sudo -u postgres psql

Дальше в сессии PostgreSQL создаем пользователя

CREATE USER testprojectuser WITH PASSWORD 'password';

Изменяем настройки кодировки, уровня изоляции транзакции и часового пояса

ALTER ROLE testprojectuser SET client_encoding TO 'utf8';

ALTER TOLE testprojectuser SET default_transaction_isolation to 'read committed';

ALTER TOLE testprojectuser SET timezone to 'UTC';

Создаём базу данных 

CREATE DATABASE testproject OWNER testprojectuser;

Возможно могут оставаться проблемы с кодировкой. Чтобы поправить это, надо проверить кодировку template, по которому создалась база. Если кодировка не 'UTF-8', тогда шаблон надо удалить и заново создать с необходимой кодировкой. И пересоздать базу для проекта с аналогичными настройками, как расписаны выше.

Выходим из интерактивной сессии PostgreSQL

Дальше создаём виртуальное окружение python (предварительно установив virtualenv) и переносим из Git проект.

Устанавливаем gunicorn и psycopg2(адаптер для работы с PostgreSQL) 

Дальше в settings.py меняем раздел DATABASES на необходимую PostgreSQL базу со всеми настройками. Ставим DEBUG = False. Устанавливаем хосты ALLOWED_HOSTS = {'перечислить хосты сервера'}. Прописываем в переменные STATIC_ROOT и MEDIA_ROOT пути до папки со статикой(css, js) и медиа-файлами

Настраиваем NGINX

server {
    listen 80;
    server_name Доменное имя или IP; 

    location /static/ {
        alias полный путь до static(включая static папку);
    }
    
    location /media/ {
        alias полный путь до static(включая media папку);
    }
    
    location / {
        proxy_pass http://наш_ip:8000; 
        proxy_set_header Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
  }
  
 Перезапускаем NGINX
 
 sudo service nginx restart
 
 В зависимости от необходимых параметров могут понадобиться доп. настройки
 
 Дальше создаем конфиг gunicorn.conf.py 
 
 В него вносим
 
bind = 'IP:8000'

workers = по рекомендуемой документацией формуле 1 + 2 * кол-во ядер
 
user = "пользователь сервера"

[program:program_name]
command=/путь_до_gunicorn_в_виртуальном_окружении testproject.wsgi:application -c /путь_до_gunicorn_конфига_в_папке_проекта (это одна команда)
directory=/путь_до_проекта
user=имя_пользователя
autorestart=true
redirect_stderr=true

после этого возвращаемся в терминал

и запускаем сервер

supervisorctl reread

supervisorctl update

supervisorctl status program_name

supervisorctl restart program_name

Проверяем доступ к сайту. Если не работает, то проверять логи и исправлять ошибки