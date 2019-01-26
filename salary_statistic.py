from terminaltables import DoubleTable
from fetch_hh_vacancies import get_stat_salary_hh
from fetch_superjob_vacancies import get_stat_salary_sj

languages = [
    '1с',
    'python',
    'go',
    'java',
    'javascript',
    'c++',
    'c',
    'ruby',
    'c#',
    'c'
]


def print_table(title, data):
    header = ('Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата')
    data.insert(0, header)
    table_instance = DoubleTable(data, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()


def main():
    title = 'SuperJob Москва'
    print_table(title, get_stat_salary_sj(languages))

    title = 'HH Москва'
    print_table(title, get_stat_salary_hh(languages))


if __name__ == '__main__':
    main()

