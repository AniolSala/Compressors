from huffman_compressor import Huffman, timer  # , average
import os
# import time


@timer
def main():
    # We especify the directory where we have the files
    files_directory_name = 'Files\\'
    path_to_files = os.getcwd() + '\\' + files_directory_name
    file_name = 'quijote'  # File name without extension!

    # Compressing the file
    file_to_compress = Huffman(filename=file_name + '.txt', path=path_to_files)
    file_to_compress.compressFile()  # Ouput: new file named file_name.bin

    # Decompressing the file
    file_to_decompress = Huffman(
        filename=file_name + '.bin', path=path_to_files)
    file_to_decompress.decompressFile()


if __name__ == '__main__':
    main()
