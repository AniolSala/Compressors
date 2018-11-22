from time import time
from subprocess import check_output
import platform

def assert_equals(file1, file2, path=''):
    if platform.win32_ver()[0]:
        print('\n', check_output("FC {} {}".format(path + file1, path +
                                             file2), shell=True).decode())
    elif platform.linux_distribution()[0] or platform.mac_ver()[0]:
        print('\n', check_output("diff {} {}".format(path + file1, path +
                                               file2), shell=True).decode())

def timer(f):
    '''
    This function will be used as a decorator
    to show the how lang takes a function to run

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
    This function will be used as a decorator to
    calculate how long takes a function (in an
    average of n) to run

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