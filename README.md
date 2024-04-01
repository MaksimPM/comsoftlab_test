<h1 align="center">Comsoftlab Test</h1> 
  
 Основной стек проекта:
  
      1. Python==3.11
      
      2. Django==4.2
      
      3. PostgreSQL

<h2 align="left">Для запуска проекта необходимо:</h2>
  
• Установить виртуальное окружение в корневой папке проекта командой:
```shell
python3.11 -m venv venv
```

• Создать в корне проекта файл ```.env``` и заполнить данные по образцу из файла ```.env.sample```

• Установить все необходимые зависимости, указанные в файле ```requirements.txt```:
```shell
pip install -r requirements.txt
```
• Выполнить создание и применение миграций командами:
```shell
python3 manage.py makemigration
```
```shell
python3 manage.py migrate
```
   
• Создать суперпользователя командой:
```shell
python3 manage.py csu
```

• Запустить сервер командой
```shell
python3 manage.py runserver
```

<h2 align="left">Для запуска проекта через Docker необходимо:</h2>

Создать и заполнить файл ```.env``` по шаблону файла ```.env.sample```

Создать и заполнить файл ```.env.docker``` по шаблону файла ```.env.docker.sample```

Создать Docker контейнер командой:
```shell
docker-compose build
```
Запустить Docker контейнер командой:
```shell
docker-compose up
```

<h2 align="left">Логика работы:</h2>
<h3 align="left">Получение сообщений с почты:</h3>

  • При получении сообщений на электронную почту, непрочитанные сообщения выводятся в интерфейс с сохранением вложенных файлов в папку в корне проекта ```media/attachments```.
 
