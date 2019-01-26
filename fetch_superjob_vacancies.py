# -*- coding: utf-8 -*-
import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')


def predict_rub_salary(vacancy):
    if not vacancy['currency'] == 'rub':
        return None
    if vacancy['payment']:
        salary = vacancy['payment']
    elif vacancy['payment_from'] and vacancy['payment_to']:
        salary = (vacancy['payment_from'] + vacancy['payment_to']) / 2
    elif vacancy['payment_from']:
        salary = vacancy['payment_from'] * 1.2
    elif vacancy['payment_to']:
        salary = vacancy['payment_to'] * 0.8
    else:
        salary = None
    return salary


def get_language_stat(language):
    json_vacancies = get_vacancies_page(language, 0)
    total_vacancies = json_vacancies['total']
    found_vacancies = json_vacancies['objects']
    vacancies_processed = 0
    sum_salary = 0
    pages, _ = divmod(total_vacancies, 100)
    for page in range(pages + 1):
        vacancies_processed, sum_salary = get_statistic_salary(found_vacancies, sum_salary, vacancies_processed)
        found_vacancies = get_vacancies_page(language, page + 1)['objects']
    if vacancies_processed:
        average_salary = int(sum_salary / vacancies_processed)
    else:
        average_salary = 0
    return total_vacancies, vacancies_processed, average_salary


def get_statistic_salary(found_vacancies, sum_salary=0, vacancies_processed=0):
    for vacancy in found_vacancies:
        predict_salary = predict_rub_salary(vacancy)
        if predict_salary is not None:
            vacancies_processed += 1
            sum_salary += predict_salary
    return vacancies_processed, sum_salary


def get_stat_salary_sj(languages):
    vacancies = []
    for language in languages:
        vacancies.append([language, *get_language_stat(language)])
    return vacancies


def get_vacancies_page(language, page = 0):
    url = '	https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': token
    }
    params = {
        'town': 4,  # Москва
        'catalogues': 48,  # Разработка, программирование
        'count': 150,
        'keyword': language,
        'no_agreement': 0,
        'page': page
    }
    r = requests.get(url=url, params=params, headers=headers)
    return r.json()