# Крсовой проект "введение в Object Oriented Programming"



## Запуск проекта
Запустите следующую команду в терминале, находясь в корневой дирректории проекта, чтобы увидеть результат работы всех функций:
```
python .\__main__.py
```

### Требование для запуска:
- python - v3.13
- poetry >=2.0.0
- requests >=2.32.3
Для загрузки необходимых пакетов необходимо запустить в терминале:
```
poetry update
```


## Модуль main
Перед началом работы необходимо в файле ".env.sample" внесите необходимые данные и измените наименование на ".env"
При запуске, из корневой папки проекта, будет запущена программа, в ней продемонстрированна работа всех методов



## Пакет src:
В пакете присутствуют следующие модули:
- get api hh
- db_manager
- base_classes.py


#### Модуль DB managers:
get_companies_and_vacancies_count:
    Возвращает список всех компаний и количество вакансий у
    каждой компании

get_all_vacancies:
    Возвращает список всех вакансий с указанием названия компании,
    названия вакансии и зарплаты и ссылки на вакансию

get_avg_salary:
    Получает среднюю зарплату по вакансиям

get_vacancies_with_keyword:
    Получает список всех вакансий,
    в названии которых содержатся переданные в метод слова,
    например python

get_vacancies_with_higher_salary:
    Получает список всех вакансий,
    у которых зарплата выше средней по всем вакансиям



## Тестирование 
Для запуска тестов потребуется:
pytest = "^8.3.4"
pytest-cov = "^6.0.0"

Далее в терминале нужно запустить команду:
```
pytest
```


******************************************************************************************************************

# Coursework project "Introduction to Object Oriented Programming"

## Launching the project
Run the following command in the terminal, being in the root directory of the project, to see the result of all functions:
```
python .\__main__.py
```

### Requirement for launching:
- python - v3.13
- poetry >=2.0.0
- requests >=2.32.3
To download the necessary packages, you need to run in the terminal:
```
poetry update
```

## Module main
Before starting work, you need to enter the necessary data in the file ".env.sample" and change the name to ".env"
When launched, from the root folder of the project, the program will be launched, it demonstrates the operation of all methods

## Package src:
The package contains the following modules:
- get api hh
- db_manager
- base_classes.py

#### DB managers module:
get_companies_and_vacancies_count:
Returns a list of all companies and the number of vacancies for

each company

get_all_vacancies:
Returns a list of all vacancies with the company name,

job title and salary and a link to the vacancy

get_avg_salary:
Gets the average salary for vacancies

get_vacancies_with_keyword:
Gets a list of all vacancies,
whose title contains the words passed to the method,
for example python

get_vacancies_with_higher_salary:
Gets a list of all vacancies,
whose salary is higher than the average for all vacancies

## Testing
To run the tests you will need:
pytest = "^8.3.4"
pytest-cov = "^6.0.0"

Next, you need to run in the terminal command:
```
pytest
```
=======
# -_SQL_
>>>>>>> 8033d810c397e0c24dfed1bf9d543c9c5b7b8893
