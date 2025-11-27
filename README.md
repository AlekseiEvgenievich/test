# Task: агрегирование performance по position

Небольшой CLI-скрипт на Python, который:

- читает один или несколько CSV-файлов;
- группирует строки по полю `position`;
- считает среднее значение поля `performance` для каждой `position`;
- выводит аккуратную таблицу с помощью `tabulate`;
- покрыт тестами на `pytest`.

## Структура проекта

```text
.
├── task.py            # основной скрипт
└── test/
    └── test_task.py   # тесты на pytest

pip install tabulate pytest

python task.py --files data1.csv data2.csv --report avg_performance

