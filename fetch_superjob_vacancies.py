# -*- coding: utf-8 -*-
import requests
import os
import calculation_salary as cs
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')


def get_language_stat(language):
    page = pages_number = 1
    found_vacancies = []
    while page <= pages_number:
        page_data = get_vacancies_page(language, page)
        page += 1
        if page_data is not None:
            vacancies_of_pages = page_data['objects']
            total_vacancies = page_data['total']
            pages_number, _ = divmod(total_vacancies, 100)
            for vacancy in vacancies_of_pages:
                found_vacancies.append(vacancy)
    vacancies_processed, average_salary = get_statistic_salary(found_vacancies)
    return total_vacancies, vacancies_processed, average_salary


def get_statistic_salary(found_vacancies, sum_salary=0, vacancies_processed=0):
    for vacancy in found_vacancies:
        predict_salary = cs.predict_rub_salary(vacancy['payment_from'], vacancy['payment_to'])
        if predict_salary is not None:
            vacancies_processed += 1
            sum_salary += predict_salary
        if vacancies_processed:
            average_salary = int(sum_salary / vacancies_processed)
        else:
            average_salary = 0
    return vacancies_processed, average_salary


def get_stat_salary_sj(languages):
    return [[language, *get_language_stat(language)] for language in languages]


def get_vacancies_page(language, page=0):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': TOKEN
    }
    params = {
        'town': 4,  # Москва
        'catalogues': 48,  # Разработка, программирование
        'count': 100,
        'keyword': language,
        'currency': 'rub',
        'no_agreement': 0,
        'page': page
    }
    response = requests.get(url=url, params=params, headers=headers)
    if response.ok:
        return response.json()
    else:
        return None

