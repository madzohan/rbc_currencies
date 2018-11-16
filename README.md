# Parse rbc.ru currencies

## Installation
- `pip3 install pipenv`
- `pipenv install`
## Running
```
> pipenv run python script.py USD
+--------+-------+--------+
| Time   |   Buy |   Sell |
+========+=======+========+
| 23:36  | 67.05 |  64.93 |
+--------+-------+--------+

> pipenv run python app.py EUR
+--------+-------+--------+
| Time   |   Buy |   Sell |
+========+=======+========+
| 23:36  |  76.4 |  74.15 |
+--------+-------+--------+
```