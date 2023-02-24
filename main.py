# Доработать декоратор logger в коде ниже.
# Должен получиться декоратор, который записывает в файл
# 'main.log' дату и время вызова функции, имя функции, аргументы,
# с которыми вызвалась, и возвращаемое значение.
# Функция test_1 в коде ниже также должна отработать без ошибок.

import datetime
import os
import requests


def logger1(old_function):
    with open('main.log', 'w', encoding='utf-8') as f:
        f.write(f'main.log файл создан \n')

    def new_function(*args, **kwargs):
        with open('main.log', 'a', encoding='utf-8') as f:
            f.write(f'Дата и время вызыва функции {datetime.datetime.now()} \n')
            f.write(f'Вызвали {old_function.__name__} c аргументами {args} и {kwargs} \n')
            result = old_function(*args, **kwargs)
            f.write(f'Результат {result} \n')
        return result

    return new_function

def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger1
    def summator(a, b=0):
        return a + b

    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def logger2(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'{path} файл создан \n')

    def __logger(old_function):
        def new_function(*args, **kwargs):
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f'Дата и время вызыва функции {datetime.datetime.now()} \n')
                f.write(f'Вызываем {old_function.__name__} c аргументами {args} и {kwargs} \n')
                result = old_function(*args, **kwargs)
                f.write(f'Результат {result} \n')
            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger2(path)
        def summator(a, b=0):
            return a + b

        @logger2(path)
        def div(a, b):
            return a / b

        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        div(4, 2)
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'

@logger1
@logger2(path='log_4.log')
def superheroes(names):
    global superheroes_best
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    response = requests.get(url)
    list_superheroes = response.json()
    new_dict = {}
    for name in names:
        for data in list_superheroes:
            if name == data['name']:
                superheroes_best = data['powerstats']['intelligence']
        new_dict[name] = superheroes_best
    best_hero = max(new_dict, key=new_dict.get)
    print(f'Самый умный супергерой это: {best_hero}, с интеллектом равным {new_dict[best_hero]}')


if __name__ == '__main__':
    test_1()
    test_2()
    superheroes(['Hulk', 'Captain America', 'Thanos'])


