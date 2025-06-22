import logging
import os
import re

from dotenv import load_dotenv  # type: ignore

from src.accessing_database import AccessingDatabase
from src.db_manager import DBManager
from src.getting_from_api import ApiHH

logger_main = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"log/{__name__}.log", mode="w", encoding="UTF8")
file_formatter = logging.Formatter(
    "\n%(asctime)s %(levelname)s %(name)s \n%(funcName)s %(lineno)d: \n%(message)s", datefmt="%H:%M:%S %d-%m-%Y"
)
file_handler.setFormatter(file_formatter)
logger_main.addHandler(file_handler)
logger_main.setLevel(logging.INFO)


def main():
    logger_main.info("Get started main")
    load_dotenv()
    triger = True

    # Входные данные
    api_src = "https://api.hh.ru/vacancies"
    # Выбранные кампании
    company = [
        (0, "TORA"),
        (1, "DEV SOLUTIONS CIS"),
        (2, "PROXY"),
        (3, "Aurma.kz"),
        (4, "Kelyanmedia"),
        (5, "ЛУКОЙЛ"),
        (6, "ELEKTRSINTEZ"),
        (7, "IT-Implant"),
        (8, "ТехРевизор"),
        (9, "Протектор"),
        (10, "Autodata"),
    ]

    item_api_hh = ApiHH(api_src, company)
    item_d_b_manager = DBManager()

    item_accessing_database = AccessingDatabase(
        {
            "port": os.getenv("DATABASE_PORT", default="5432"),
            "user": os.getenv("DATABASE_USER", default="postgres"),
            "host": os.getenv("DATABASE_HOST", default="localhost"),
            "password": os.getenv("DATABASE_PASSWORD"),
            "database": os.getenv("DATABASE_NAME", default="postgres"),
            "table_name": "vacancies",
        }
    )

    # Получение массивов даннных и создаие таблиц
    vacahcy = item_api_hh.get_vacancies_of_api()

    print(item_accessing_database.creating_a_vacancy_table)
    item_accessing_database.query_tables_with_data(vacahcy, "vacancies")

    item_accessing_database.creating_a_company_table
    item_accessing_database.query_tables_with_data(company, "company")

    # Осовной блок
    while triger:
        pattern = re.compile(r"['.,?)(]")

        user_choice = input(
            "Привет! Добро пожаловать в программу подбора вакансий\n"
            + """Выберите необходимый пункт меню:
    1. Хотите запросить список
       вакансий и работать с ним?
    2. Выйти

    Введите номер варианта: """
        ).lower()

        if user_choice == "1":
            logger_main.info("1, create item DBManager")

            if (
                "да"
                == input(
                    """
            Если хотите список всех вакансий с указанием названия компании,
            названия вакансии и зарплаты и ссылки на вакансию, введите "да": """
                ).lower()
            ):
                all_vacancies = item_d_b_manager.get_all_vacancies(item_accessing_database)
                for vacanci in all_vacancies:
                    print(vacanci)

            if (
                "да"
                == input(
                    """
            Если хотите список всех вакансий, у которых зарплата выше
            средней по всем вакансиям, введите "да": """
                ).lower()
            ):
                avg_salary = item_d_b_manager.get_vacancies_with_higher_salary(item_accessing_database, "vacancies")
                for salary in avg_salary:
                    print(salary)

            if (
                "да"
                == input(
                    """
            Если хотите список всех компаний и количество вакансий у каждой
            компании, введите "да": """
                ).lower()
            ):
                companies = item_d_b_manager.get_companies_and_vacancies_count(item_accessing_database)
                for compani in companies:
                    print(compani)

            if (
                "да"
                == input(
                    """
            Если хотите увидеть среднюю зарплату по вакансиям,
            введите "да": """
                ).lower()
            ):
                print(item_d_b_manager.get_avg_salary(item_accessing_database, "vacancies")[0])

            if (
                "да"
                == input(
                    """
            Если хотите найти вакансии по ключевому слову,
            введите "да": """
                ).lower()
            ):
                seach_word = item_d_b_manager.get_vacancies_with_keyword(
                    item_accessing_database, input("Введите слово для поиска: ").title()
                )
                for compani in seach_word:
                    print(re.sub(pattern, "", (f"{compani[1], compani[2], compani[3]}")))

            logger_main.info(f"{item_d_b_manager}")
            print("\nВозвращаюсь в главное меню\n")

        elif user_choice == "2":
            print("До следующей встречи)")
            triger = False
        else:
            print("Хм, кажется такого варианта у меня пока нет(")

    logger_main.info("End main")


if __name__ == "__main__":
    main()
