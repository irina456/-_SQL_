import logging

from src.accessing_database import AccessingDatabase
from src.base_classes import Manager

logger_db_manager = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"log/{__name__}.log", mode="w", encoding="UTF8")
file_formatter = logging.Formatter(
    "\n%(asctime)s %(levelname)s %(name)s \n%(funcName)s %(lineno)d: \n%(message)s", datefmt="%H:%M:%S %d-%m-%Y"
)
file_handler.setFormatter(file_formatter)
logger_db_manager.addHandler(file_handler)
logger_db_manager.setLevel(logging.INFO)


class DBManager(Manager):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return """
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
    """

    def get_companies_and_vacancies_count(self, item_class) -> list:
        """Возвращает список всех компаний и
        количество вакансий у каждой компании

        Returns:
            (list): результат в формате списка
        """
        result = []
        times = item_class.manual_query_entry(
            f"SELECT DISTINCT employer, COUNT(*) FROM vacancies GROUP BY employer ORDER BY COUNT(*) DESC;"
        )
        for time in times:
            result.append(f"{time[0]}, {time[1]}")

        return result

    def get_all_vacancies(self, item_class) -> list:
        """Возвращает список всех вакансий с указанием
        - названия компании
        - названия вакансии
        - зарплаты
        - сылки на вакансию

        Args:
            item_class (class instance): экземпляр класса

        Returns:
            list: список вакансий
        """
        "Возвращает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"
        result = []
        times = item_class.manual_query_entry(
            f"""SELECT comp.name AS company_name,
                    vacancies.name AS vacanci_name,
                    vacancies.salary,
                    vacancies.link
                    FROM company AS comp
                    JOIN vacancies ON comp.name=vacancies.employer;"""
        )

        for time in times:
            result.append(f"{time[0]}, {time[1]}, {time[2]}, {time[3]}")

        return result

    def get_avg_salary(self, item_class, table_name: str = "") -> float:
        """Получает среднюю зарплату по вакансиям

        Returns:
            float: средняя зарплата
        """
        result = []
        times = item_class.manual_query_entry(f"SELECT AVG(salary) FROM {table_name};")
        for time in times:
            result.append(f"{round(float(time[0]))}")

        return result

    def get_vacancies_with_keyword(self, item_class, seach_word: str = "") -> list:
        """получает список всех вакансий,
        в названии которых содержатся переданные в метод слова,
        например python

        Args:
            seach_word (str, optional): слово дл поиска. Defaults to "".

        Returns:
            list: список вакансий
        """
        time = item_class.manual_query_entry(f"SELECT * FROM vacancies WHERE name LIKE '{seach_word}%_'")
        return time

    def get_vacancies_with_higher_salary(self, item_class, table_name: str = "") -> list:
        """Получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям

        Returns:
            list: список вакансий
        """
        ""
        result = []

        times = item_class.manual_query_entry(
            f"SELECT name FROM vacancies {table_name} WHERE salary > (SELECT avg(salary) FROM vacancies);"
        )
        for time in times:
            result.append(f"{time[0]}")

        return result
