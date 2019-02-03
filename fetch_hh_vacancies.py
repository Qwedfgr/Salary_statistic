# -*- coding: utf-8 -*-
import requests
import calculation_salary


def get_stat_salary_hh(languages):
    vacancies = []
    for language in languages:
        vacancies.append([language, *get_language_stat(language)])
    return vacancies


def get_language_stat(language):
    json_vacancies = get_vacancies_page(language, 0)
    total_vacancies = json_vacancies['found']
    found_vacancies = json_vacancies['items']
    pages = json_vacancies['pages']
    vacancies_processed = 0
    sum_salary = 0
    for page in range(pages):
        vacancies_processed, sum_salary = get_statistic_salary(found_vacancies, sum_salary, vacancies_processed)
        found_vacancies = get_vacancies_page(language, page+1)['items']
    average_salary = int(sum_salary/vacancies_processed)
    return total_vacancies, vacancies_processed, average_salary


def get_statistic_salary(found_vacancies, sum_salary=0, vacancies_processed=0):
    for vacancy in found_vacancies:
        predict_salary = calculation_salary.predict_rub_salary(vacancy['salary']['from'], vacancy['salary']['to'])
        if predict_salary is not None:
            vacancies_processed += 1
            sum_salary += predict_salary
    return vacancies_processed, sum_salary


def get_vacancies_page(language, page = 0):
    url = 'https://api.hh.ru/vacancies/'
    params = {
        'text': 'Программист {}'.format(language),
        'area': 1,  # Москва
        'search_period': '',
        'currency': 'RUR',
        'page': page
    }
    response = requests.get(url=url, params=params)
    return response.json()




