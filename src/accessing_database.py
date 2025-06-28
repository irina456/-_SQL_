import logging

import psycopg2  # type: ignore

logger_accessing_database = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"log/{__name__}.log", mode="w", encoding="UTF8")
file_formatter = logging.Formatter(
    "\n%(asctime)s %(levelname)s %(name)s \n%(funcName)s %(lineno)d: \n%(message)s", datefmt="%H:%M:%S %d-%m-%Y"
)
file_handler.setFormatter(file_formatter)
logger_accessing_database.addHandler(file_handler)
logger_accessing_database.setLevel(logging.INFO)


class AccessingDatabase:
    parametrs: dict

    def __init__(self, parametrs):
        parameters = self.__nput_parameters_check(parametrs)
        self.__password = parameters["password"]
        self.__port = parameters["port"]
        self.__user = parameters["user"]
        self.__host = parameters["host"]
        self.__database = parameters["database"]
        self.table_name = parameters["table_name"]

    def __nput_parameters_check(self, dict_input_parameters: dict = {}):
        """Приватный метод валидации данных
        переадйте словарь с ключами "port", "user", "host", "database", "table_name"
        и джанными, которые вы ходите изменить

        Иначе метод подставит данные по умолчанию

        Args:
            dict_input_parameters (dict, optional): _description_. Defaults to {}.

        Returns:
            _type_: _description_
        """
        keys = ["port", "user", "host", "database", "table_name", "password"]
        default_values = ["5432", "postgres", "localhost", "postgres", "vacancies", ""]
        result = {}

        for i, value in enumerate(keys):
            try:
                temp = dict_input_parameters[value]
                result[value] = temp
            except KeyError:
                result[value] = default_values[i]
        return result

    def __str__(self):
        """Делайте print экземпляра класса, чтобы увидеть список и значение всех атрибутов

        Returns:
            _str_: атрибуты класса
        """
        return f"""
    port: {self.__port}
    user: {self.__user}
    host: {self.__host}
    password: top secret
    database: {self.__database}
    table_name: {self.table_name}"""

    def __call__(self):
        """Вызовите экземпляр и получите список тапблиц

        Returns:
            str: список тапблиц
        """        
        result = ""

        connection = psycopg2.connect(
            port=self.__port, user=self.__user, host=self.__host, database=self.__database, password=self.__password
        )
        cursor = connection.cursor()
        try:
            with cursor:
                cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
                result = cursor.fetchall()

            connection.commit()

        except psycopg2.InternalError as error:
            print(
                """     ERROR: Таблица не найдена
            Синтаксическая ошибка в SQL-запросе
            Неправильное количество заданных параметров"""
            )
            logger_accessing_database.warning(error)

        except psycopg2.ProgrammingError as error:
            print(
                """     ERROR: Таблица не найдена или уже существует,
            синтаксическая ошибка в SQL-запросе,
            неправильное количество заданных параметров"""
            )
            logger_accessing_database.warning(error)

        except psycopg2.Error as error:
            print(f"ERROR: Хм, исключительная ошибка {error}")
            logger_accessing_database.warning(error)

        finally:
            if not result:
                result = "Ни одной таблицы не найдено"
            cursor.close()
            connection.close()
        return result

    @property
    def creating_a_vacancy_table(self) -> str:
        """Метод создания таблицы вакансий

        Returns:
            _str_: сообщение
        """        
        connection = psycopg2.connect(
            port=self.__port, user=self.__user, host=self.__host, database=self.__database, password=self.__password
        )
        cursor = connection.cursor()
        try:
            with cursor:
                cursor.execute(
                    f"""CREATE TABLE {self.table_name} (
                    vacancy_id int PRIMARY KEY,
                    name text NOT NULL,
                    link text NOT NULL,
                    salary int NOT NULL,
                    employer text  NOT NULL,
                    requirements text
                    )"""
                )

            connection.commit()
            return f"Таблица {self.table_name} успешно создана"

        except psycopg2.InternalError as error:
            print(
                """     ERROR: Таблица не найдена или уже существует,
            Синтаксическая ошибка в SQL-запросе
            Неправильное количество заданных параметров"""
            )
            logger_accessing_database.warning(error)
            return error

        except psycopg2.ProgrammingError as error:
            print(
                """     ERROR: Таблица не найдена или уже существует,
            синтаксическая ошибка в SQL-запросе,
            неправильное количество заданных параметров"""
            )
            logger_accessing_database.warning(error)
            return error

        except psycopg2.Error as error:
            print(f"ERROR: Хм, исключительная ошибка {error}")
            logger_accessing_database.warning(error)
            return error

        finally:
            cursor.close()
            connection.close()

    @property
    def creating_a_company_table(self, data: list[list] = [[]]):
        """Метод создания таблицы кампаний

        Args:
            data (list[list], optional): список вакансий. Defaults to [[]].
        """        
        self.manual_query_entry(f"CREATE TABLE company (company_id serial NOT NULL, name text NOT NULL)")

    def query_tables_with_data(self, data: list[list] = [[]], table_name: str = "vacancies") -> list:
        """Метод создания, отправки запроса на заполнение данными таблиц
        Передайте только название таблици и ее столбцов, метод сомтавит запрос формата:
        "INSERT INTO {_название_таблицы_} VALUES ...."
        И передайте список списков на заполнение

        Args:
            query_content (str, optional): ваш запрс, только название таблици и ее столбцов. Defaults to "".
            data (list[list], optional): _description_. Defaults to [[]].

        Returns:
            _list_: 
        """
        result = []

        connection = psycopg2.connect(
            port=self.__port, user=self.__user, host=self.__host, database=self.__database, password=self.__password
        )
        cursor = connection.cursor()
        try:
            with cursor:
                for customer in data:
                    if table_name == "vacancies":
                        cursor.execute(
                            f"""INSERT INTO {self.table_name}
                            ("vacancy_id", "name", "link", "salary", "employer", "requirements")
                            VALUES ({", ".join(["%s"] * len(customer))})
                            RETURNING *""",
                            customer,
                        )
                    elif table_name == "company":
                        cursor.execute(
                            f"""INSERT INTO {table_name}
                            ("company_id", "name")
                            VALUES ({", ".join(["%s"] * len(customer))})
                            RETURNING *""",
                            customer,
                        )
                result = cursor.fetchall()

            connection.commit()

        except psycopg2.InternalError as error:
            print(
                """     ERROR: Таблица не найдена
            Синтаксическая ошибка в SQL-запросе
            Неправильное количество заданных параметров"""
            )
            logger_accessing_database.warning(error)

        except psycopg2.ProgrammingError as error:
            print(
                """     ERROR: Таблица не найдена или уже существует,
            синтаксическая ошибка в SQL-запросе,
            неправильное количество заданных параметров"""
            )
            logger_accessing_database.warning(error)

        except psycopg2.Error as error:
            print(f"ERROR: Хм, исключительная ошибка {error}")
            logger_accessing_database.warning(error)

        finally:
            cursor.close()
            connection.close()

        return result

    def manual_query_entry(self, query_content: str = "") -> list:
        """Выполнение ручного запроса и возврат результата
        Передайте строку с вашим запросом.

        Args:
            query_content (str, optional): текст запроса. Defaults to "".

        Returns:
            list: результат в формате объекта
        """
        result = []

        connection = psycopg2.connect(
            port=self.__port, user=self.__user, host=self.__host, database=self.__database, password=self.__password
        )
        cursor = connection.cursor()
        try:
            times = []
            with cursor:
                cursor.execute(query_content)
                try:
                    times = cursor.fetchall()
                except psycopg2.ProgrammingError:
                    pass

            for time in times:
                result.append(time)

            connection.commit()

        except psycopg2.InternalError as error:
            print(
                """     ERROR: Таблица не найдена или уже существует,
            Синтаксическая ошибка в SQL-запросе
            Неправильное количество заданных параметров"""
            )
            logger_accessing_database.warning(error)
            return error

        except psycopg2.ProgrammingError as error:
            print(
                """     ERROR: Таблица не найдена или уже существует,
            синтаксическая ошибка в SQL-запросе,
            неправильное количество заданных параметров"""
            )
            logger_accessing_database.warning(error)
            return error

        except psycopg2.Error as error:
            print(f"ERROR: Хм, исключительная ошибка {error}")
            logger_accessing_database.warning(error)
            return error

        finally:
            cursor.close()
            connection.close()

        return result

    def change_database_password(self, passwd: str = ""):
        """Метод смена пароля базы данных

        Args:
            passwd (str, optional): введите новый пароль. Defaults secret.
        """
        if not passwd:
            self.__password = passwd
