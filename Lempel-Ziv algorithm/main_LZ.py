from lempel_ziv_compressor import *
import os
from subprocess import check_output
import platform


def assert_equals(file1, file2, path=''):
    print()
    if platform.win32_ver()[0]:
        print(check_output("FC {} {}".format(path + file1, path +
                                             file2), shell=True).decode())
    elif platform.linux_distribution()[0] or platform.mac_ver()[0]:
        print(check_output("diff {} {}".format(path + file1, path +
                                               file2), shell=True).decode())


def compress(filename):
    pass


@timer
def main():
    # Especify the directory where we have the files
    files_directory_name = 'Files'
    path_to_files = os.getcwd() + '\\' + files_directory_name
    file_name = 'quijote_campus'  # File name without extension!

    # Compressing the file
    file_to_compress = LempelZiv(
        filename=file_name + '.txt', path=path_to_files)
    file_to_compress.compressFile()  # Ouput: file_name.bin

    # Decompressing the file
    file_to_decompress = LempelZiv(
        filename=file_name + '.bin', path=path_to_files)
    file_to_decompress.decompressFile()  # Ouput: <file_name>_decompressed.txt

    # Make sure original and decompressed files are equal:
    original_file = file_name + '.txt'
    decompressed_file = file_name + '_decompressed.txt'
    assert_equals(original_file, decompressed_file,
                  path=".\\{}\\".format(files_directory_name))


if __name__ == '__main__':
    main()
