from time import time
from subprocess import check_output
import platform


def assert_equals(file1, file2, path=''):
    '''
    Function that compares if two files are equal using
    the shell of the OS of the user
    '''

    f1, f2 = path + file1, path + file2

    if platform.win32_ver()[0]:
        print('\n', check_output("FC {} {}".format(f1, f2),
                                 shell=True).decode())

    elif platform.linux_distribution()[0] or platform.mac_ver()[0]:
        print('\n', check_output("diff {} {}".format(f1, f2),
                                 shell=True).decode())

    else:
        raise Warning(
            'Unknown operative system. Comparison could not be done.')


def timer(f):
    '''
    Decorator that prints the time of execution
    of a given function

    '''
    def inner_function(*args, **kwargs):
        t1 = time()
        rf = f(*args, **kwargs)
        t2 = time()
        print('{.__name__} has been executed in {} seconds'.format(
            f, round(t2 - t1, 3)))
        return rf
    return inner_function


def average(n):
    '''
    Decorator that executes the function n times
    and print its average time of execution.

    '''
    def inner(f):
        def make_average(*args, **kwargs):
            av = 0
            for _ in range(n):
                t1 = time()
                rf = f(*args, **kwargs)
                t2 = time()
                av += (t2 - t1) / n
            print('The function {.__name__} took {}'.format(f, round(av, 3)) +
                  'seconds to run in an average of {}'.format(n))
            return rf
        return make_average
    return inner
