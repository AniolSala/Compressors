# from LZ_variant import LempelZiv
from LZ_compressor import LempelZiv
import os
import time


def compareFiles(file1, file2, path=os.getcwd(), encoding='unicode_escape'):
    '''
    This function checks that two text files are exactly the same
    '''
    path1 = path + '\\' + file1
    path2 = path + '\\' + file2

    with open(path1, 'r', encoding=encoding) as first, open(
            path2, 'r', encoding=encoding) as second:

        f1, f2 = first.read(), second.read()

    if len(f1) != len(f2):
        print('The files have different sizes.')
        return False

    for i in range(len(f1)):
        if f1[i] != f2[i]:
            print('They differ in the character number', i, ':')
            return False
    print('The two files are equal')
    return True


def main():

    # Choosing the file to compress:
    t1 = time.time()
    filename = 'quijote_campus'
    filespath = os.getcwd() + '\\Files'

    input_filename = filename + '.txt'
    encoded_filename = filename + '_compressed.bin'
    output_filename = filename + '_decompressed.txt'

    # Creating the Huffman object of this file and compressing:
    file = LempelZiv(input_filename, path=filespath)
    file.compressFile(outputname=encoded_filename)
    t2 = time.time()

    # Creating the Huffman object of the file we want to decompress:
    compressed = LempelZiv(encoded_filename, path=filespath)
    compressed.decompress(outputname=output_filename)
    t3 = time.time()

    # Print the total time, the compressing time and the decompressing time:
    print('Total time: ', t3 - t1)
    print('Compressing time: ', t2 - t1)
    print('Decompressing time: ', t3 - t2)

    # Check if the original and the decompressed file are exactly the same:
    compareFiles(input_filename, output_filename, path=filespath)

if __name__ == '__main__':
    main()