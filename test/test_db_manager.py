import pytest


def test_shown_object_d_b_manager_default(object_d_b_manager_default, capsys):
    print(object_d_b_manager_default)
    captured = capsys.readouterr()
    assert (
        captured.out
        == """  url: https://api.hh.ru/vacancies
    params: {'text': '', 'page': 1, 'per_page': 10}
    headers: {'User-Agent': 'HH-User-Agent'}
    vacancies: []
    port: 5432
    user: postgres
    host: localhost
    password: top secret
    database: postgres
    table_name: vacancies
"""
    )


def test_shown_object_d_b_manager_params(object_d_b_manager_params, capsys):
    print(object_d_b_manager_params)
    captured = capsys.readouterr()
    assert (
        captured.out
        == """  url: https://api.hh.ru/vacancies
    params: {'text': '', 'page': 1, 'per_page': 10}
    headers: {'User-Agent': 'HH-User-Agent'}
    vacancies: []
    port: 
    user: 
    host: 
    password: top secret
    database: 
    table_name: vacancies
"""
    )
