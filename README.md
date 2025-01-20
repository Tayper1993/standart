# Standart

## Стек
* `python 3.12`
* `Flask`
* `flask-sqlalchemy`
* `sqlite`

### Работа с зависимостями
* Устанавливаем `pip-compile`
```bash
pip install pip-tools
```
* Добавляем новую зависимость в список `project.dependencies` в `pyproject.toml`
* Генерируем обновленный `requirements.txt`
```bash
pip-compile -o requirements.txt pyproject.toml
```
* Устанавливаем зависимости
```bash
pip install -r requirements.txt
```
#### Добавление `dev` зависимости проекта:
* Добавляем новую зависимость в список `dev` в `project.optional-dependencies` в `pyproject.toml`
* Генерируем обновленный `requirements-dev.txt`
```bash
pip-compile --extra=dev -o requirements-dev.txt pyproject.toml
```


## Конфигурация:
* Переменные окружения берутся из файла `.config`

## Запуск:
* Локально: `flask run`

## Документация:
* swagger: `{base_url}/apidocs`
* openapi (json): `{base_url}/openapi.json`

## Линтеры:

### pre-commit

1. Запустить скрипт:

   ```shell
   pre-commit run -a
   ```