# -*- coding: utf-8 -*-
import requests
import calculation_salary as cs


def get_stat_salary_hh(languages):
    return [[language, *get_language_stat(language)] for language in languages]


def get_language_stat(language):
    page = pages_number = 1
    found_vacancies = []
    while page <= pages_number:
        page_data = get_vacancies_page(language, page)
        page += 1
        if page_data is not None:
            pages_number = page_data['pages']
            vacancies_of_page = page_data['items']
            total_vacancies = page_data['found']
            for vacancy in vacancies_of_page:
                found_vacancies.append(vacancy['salary'])
    vacancies_processed, average_salary = get_statistic_salary(found_vacancies)
    return total_vacancies, vacancies_processed, average_salary


def get_statistic_salary(found_vacancies):
    vacancies_processed = 0
    sum_salary = 0
    for vacancy in found_vacancies:
        if vacancy is not None:
            predict_salary = cs.predict_rub_salary(vacancy['from'], vacancy['to'])
            if predict_salary is not None:
                vacancies_processed += 1
                sum_salary += predict_salary
    if vacancies_processed:
        average_salary = int(sum_salary / vacancies_processed)
    else:
        average_salary = 0
    return vacancies_processed, average_salary


def get_vacancies_page(language, page=0):
    url = 'https://api.hh.ru/vacancies/'
    params = {
        'text': 'Программист {}'.format(language),
        'area': 1,  # Москва
        'search_period': '',
        'currency': 'RUR',
        'page': page
    }
    response = requests.get(url=url, params=params)
    if response.ok:
        return response.json()
    else:
        return None




