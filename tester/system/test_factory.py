import os

from colorama import Fore

from tester.test.test import Test


def get_all_tests(tests: list) -> ['class']:
    import_all_tests()
    tests_available = get_all_tests_available()
    if tests == ['all']:
        return tests_available
    return [t for t in tests_available if t.__module__.split('.')[-1:][0] in tests]


def import_all_tests():
    modules = os.listdir('tester/test')
    for t in modules:
        if t.endswith('.py'):
            print(Fore.CYAN + 'import ' + 'tester.test.' + t[:-3])
            __import__('tester.test.' + t[:-3], globals(), locals(), [], 0)


def get_all_tests_available() -> list:
    return find_subclassing_tests(Test)


def find_subclassing_tests(test: 'class') -> list:
    subclasses = test.__subclasses__()
    return_list = subclasses
    for subclass in subclasses:
        return_list += find_subclassing_tests(subclass)
    return return_list
