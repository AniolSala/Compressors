from huffman_compressor import Huffman
from lempel_ziv_compressor import LempelZiv
from lib import timer, average, assert_equals
import os


@timer
def compress(compressor, *args, **kwargs):
    if compressor == 'LempelZiv':
        file_to_compress = LempelZiv(*args, **kwargs)
    elif compressor == 'Huffman':
        file_to_compress = Huffman(*args, **kwargs)
    else:
        raise ValueError('Valid compressors are "LempelZiv" and "Huffman"')

    file_to_compress.compressFile()


@timer
def decompress(compressor, *args, **kwargs):
    if compressor == 'LempelZiv':
        file_to_decompress = LempelZiv(*args, **kwargs)
    elif compressor == 'Huffman':
        file_to_decompress = Huffman(*args, **kwargs)
    else:
        raise SyntaxError('Valid compressors are "LempelZiv" and "Huffman"')

    file_to_decompress.decompressFile()


@timer
def main():
    # Especify the directory where we have the files
    files_directory = '\\Files'
    path_to_files = os.getcwd() + files_directory
    file_name = 'quijote_campus'  # File name without extension!

    # Choosing the compressor (LempelZiv or Huffman)
    compressor = 'Huffman'

    # Compressing the file
    compress(compressor, filename=file_name + '.txt', path=path_to_files)

    # Decompressing the file
    decompress(compressor, filename=file_name +
               '.bin', path=path_to_files)

    # Make sure original and decompressed files are equal:
    assert_equals(file_name + '.txt', file_name + '_decompressed.txt',
                  ".{}\\".format(files_directory))


if __name__ == '__main__':
    main()
