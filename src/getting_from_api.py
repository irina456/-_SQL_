import logging

import requests as re

from src.base_classes import GetAPI

logger_db_manager = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"log/{__name__}.log", mode="w", encoding="UTF8")
file_formatter = logging.Formatter(
    "\n%(asctime)s %(levelname)s %(name)s \n%(funcName)s %(lineno)d: \n%(message)s", datefmt="%H:%M:%S %d-%m-%Y"
)
file_handler.setFormatter(file_formatter)
logger_db_manager.addHandler(file_handler)
logger_db_manager.setLevel(logging.INFO)


class ApiHH(GetAPI):

    url: str
    select_companies: list

    def __init__(self, url, select_companies):
        """"""
        self.__url = url
        self.__params = {"text": "", "page": 1, "per_page": 10}
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__vacancies = []
        self.__select_companies = self.__preparing_list_vacancies(select_companies)

    def __str__(self):
        """Делайте print экземпляра класса, чтобы увидеть список и значение всех атрибутов"""
        return f"""  url: {self.__url}
    params: {self.__params}
    headers: {self.__headers}
    vacancies: {self.__vacancies}"""

    def __preparing_list_vacancies(self, select_companies: list = []) -> list:
        """Метод конвертации в простой список, где значения
        имеют тип str

        Args:
            select_companies (list, optional): Список кампаний.
            Defaults to [].

        Returns:
            list: Список кампаний
        """
        result = []

        for i, value in enumerate(select_companies):
            result.append(value[1])
        return result

    def get_vacancies_of_api(self, search_word: str = "") -> list:
        """Метод получает список всех вакансий,
        в названии которых содержатся переданные в метод слова

        Args:
            search_word (str, optional): слово для поиска. Defaults to "".

        Raises:
            ConnectionError: Ошибка соединения
            ValueError: Не корректные условия запроса,
                ошибочная ссылка

        Returns:
            list: Список вакансий со всеми данными
        """
        ""
        self.__params["text"] = search_word
        while self.__params.get("page") != 20:
            vacancies = []
            try:
                response = re.get(self.__url, headers=self.__headers, params=self.__params)
                if response.status_code == 200:
                    try:
                        times = response.json()["items"]
                        for time in times:
                            vacancies.append(time)
                    except IndexError:
                        logger_db_manager.warning(f"sent an empty list(:\n{response.json()["items"]}")

            except re.exceptions.ConnectionError:
                vacancies = []
                raise ConnectionError("Connection Error. Please check your network connection.")

            except re.exceptions.HTTPError:
                vacancies = []
                raise ValueError("HTTP Error. Please check the URL.")

            finally:
                logger_db_manager.info("Attempt to access API completed")

            self.__vacancies.extend(vacancies)
            self.__params["page"] += 1

        self.__vacancies = self.__drop_salary_null
        self.__vacancies = self.__making_a_convenient_list

        return self.__vacancies

    @property
    def __drop_salary_null(self) -> list:
        """Приватный метод обработки "null" - пустого
        значения в json

        Returns:
            list: Список вакансий с отсутствием пустых значений
        """
        for i, value in enumerate(self.__vacancies):
            try:
                if not value["salary"]["from"]:
                    self.__vacancies[i]["salary"]["from"] = 0

            except TypeError:
                try:
                    if not value["salary"]:
                        self.__vacancies[i]["salary"] = {"from": 0}

                except TypeError:
                    converted = {}
                    try:
                        converted = {
                            "id": value[0],
                            "name": value[1],
                            "alternate_url": value[2],
                            "salary": {"from": value[3]["from"]},
                            "employer": {"name": value[4]},
                            "snippet": {"requirement": value[5]},
                        }
                    except TypeError:
                        converted = {
                            "id": value[0],
                            "name": value[1],
                            "alternate_url": value[2],
                            "salary": {"from": 0},
                            "employer": {"name": value[4]},
                            "snippet": {"requirement": value[5]},
                        }
                    self.__vacancies[i] = converted

        return self.__vacancies

    @property
    def __making_a_convenient_list(self) -> list:
        """Метод подготовки данных, для внесения в колонки
        таблицы базы данных

        Returns:
            list: Конвертированный список для заполнения
                таблиц БД
        """
        result = []
        for vacanci in self.__vacancies:
            if vacanci["employer"]["name"] in self.__select_companies:
                result.append(
                    [
                        vacanci["id"],
                        vacanci["name"],
                        vacanci["alternate_url"],
                        vacanci["salary"]["from"],
                        vacanci["employer"]["name"],
                        vacanci["snippet"]["requirement"],
                    ]
                )
        return result
