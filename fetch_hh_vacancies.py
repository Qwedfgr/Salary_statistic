# -*- coding: utf-8 -*-
import requests


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


def predict_rub_salary(vacancy):
    salary = vacancy['salary']
    if salary is None\
            or salary['currency'] != 'RUR':
        return None
    if not salary['from'] is None\
            and not salary['to'] is None:
        sal = (salary['from'] + salary['to'])/2
    elif not salary['from'] is None:
        sal = salary['from'] * 1.2
    elif not salary['to'] is None:
        sal = salary['to'] * 0.8
    else:
        sal = None
    return sal


def get_statistic_salary(found_vacancies, sum_salary=0, vacancies_processed=0):
    for vacancy in found_vacancies:
        predict_salary = predict_rub_salary(vacancy)
        if predict_salary is not None:
            vacancies_processed += 1
            sum_salary += predict_salary
    return vacancies_processed, sum_salary


def get_vacancies_page(language, page = 0):
    url = 'https://api.hh.ru/vacancies/'
    params = {
        'text': 'Программист {}'.format(language),
        'area': 2,  # Москва
        'search_period': '',
        'page': page
    }
    r = requests.get(url=url, params=params)
    return r.json()




