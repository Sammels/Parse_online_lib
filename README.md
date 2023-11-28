# Парсер книг с сайта tululu.org

------------

Проект создан, для скачивания книг.

### Как установить
Для работы, надо установить ["Python"](https://www.python.org/downloads/release/python-3116/)

1. Далее установить виртуальное окружение
```bash
python -m venv env
```
2. Далее клонируем этот репозиторий
```text
git clone https://github.com/Sammels/Parse_online_lib.git
```
3. После этого нужно установить необходимые библиотеки

```bash
pip install -r requirements.txt
```
Вот список библиотек.
```text
requests==2.31.0
beautifulsoup4==4.12.2
pathvalidate==3.0.0
argparse==1.4.0
lxml==4.9.3
```

### Аргументы

Пример работы:
```bash
python tululu.py --start_page 45 --end_page 55 
```
`--start_page` - Аргумент который указывает на первый номер книги.</br>
`--end_page` - Аргумент указывающий последнюю книгу необходимую к скачиванию.


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
