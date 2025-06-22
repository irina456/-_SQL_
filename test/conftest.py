import pytest

from src.db_manager import DBManager


@pytest.fixture
def object_d_b_manager_default():
    item_test_hh = DBManager("https://api.hh.ru/vacancies", {})
    return item_test_hh


@pytest.fixture
def object_d_b_manager_params():
    item_test_hh = DBManager(
        "https://api.hh.ru/vacancies", {"port": "", "user": "", "host": "", "text": "", "database": ""}
    )
    return item_test_hh
