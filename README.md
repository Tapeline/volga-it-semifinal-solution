> Solution for Volga-IT'24 semifinals

# Запуск
```shell
docker compose up -d
```
при этом должны быть предоставлены следующие переменные окружения:
- `SECRET_KEY` - секретный ключ API
- `DB_USER` - пользователь к БД (всем)
- `DB_PASS` - пароль указанного пользователя БД
- `ELASTIC_USER` - пользователь elasticsearch
- `ELASTIC_PASS` - пароль этого пользователя
- `ELASTIC_KIBANA_USER`, `ELASTIC_KIBANA_PASS` - данные для Kibana

В файле `.env` указана стандартная конфигурация переменных.

# Основное задание:
1. Account URL: http://localhost:8081/ui-swagger
2. Hospital URL: http://localhost:8082/ui-swagger
3. Timetable URL: http://localhost:8083/ui-swagger
4. Document URL: http://localhost:8084/ui-swagger

# Дополнительное задание:
1. ElasticSearch URL: http://localhost:9200/
2. Kibana URL: http://localhost:5601/

