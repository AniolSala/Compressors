from time import time
import os
from math import log, ceil
import numpy as np


class LempelZiv():
    def __init__(self, filename, encoding='utf-8'):
        self.file = filename
        self.table = {''.encode(encoding): 0}
        self.encoding = encoding

    def compressFile2(self, outputname=None, getDict=None):
        '''
        Here we will compress the file following the next steps:
        1. Open the file and encode it. We will work on a bytes string.
        2. We apply thel LZ algorithm on the bytes string:
            a) We initialize the dictionary (self.table) with an empty
            bytearray. We set this as the position 0.
            b) We look, at each iteration, the segment [start:len(bytestring)]
            of the bytestring (we begin with start = 0). If we find a
            subsegment of bytes that is not in self.table, we look for
            the position of its prefix (this is, the bytes of the subsegment
            except the last one) to add, in compressed, the position + the
            last byte (both in binary) of the subsegment. Finally we add this
            subsegment to self.table.
            NOTE: A single character has prefix '', which
            is an empty bytearray whose position is 0 as mentioned before.
        3. Finally, we look how many positions we found and how many bits
        are needed to write these positions in binary. With this we can set
        the same bit length for each element of compressed.
        4. We join all elements of comressed in a bitstring, then we convert it
        to bytes to write the compressed file.
        '''

        filename, _ = os.path.splitext(self.file)
        if outputname:
            outputFile = outputname
        else:
            outputFile = filename + '.bin'

        # with open(self.file, 'r', encoding=self.encoding) as output:
        #     text = output.read().encode(self.encoding)

        with open(self.file, 'rb') as output:
            text = output.read()

        # Here begins the Lempel Ziv algorithm:
        start = 0
        n_data = len(text) + 1
        compressed = []
        # t1 = time()
        while True:
            for i in range(1, n_data - start):
                w = text[start:start + i]

                if w not in self.table:
                    pos = self.table[w[:-1]]
                    codeword = bin(pos)[2:] + bin(w[-1])[2:].zfill(8)
                    compressed.append(codeword)

                    self.table[w] = len(self.table)
                    start += i
                    break

            # If the last characters of the file have appeared before:
            else:
                if start != n_data - 1:
                    pos = self.table[w[:-1]]
                    compressed.append(bin(pos)[2:] + bin(w[-1])[2:].zfill(8))
                break
        # t2 = time()

        # n_bits is the number of bits needed to write in binary the n postions
        n_bits = int(log(len(self.table), 2)) + 1

        bitstring = ''.join([bits.zfill(n_bits + 8) for bits in compressed])
        # t3 = time()
        # print(t3 - t2, t2 - t1)

        # We add the padding to make len(bitstring) % 8 == 0:
        extraPad = 8 - len(bitstring) % 8 if len(bitstring) % 8 != 0 else 0
        bitstring = bitstring.zfill(len(bitstring) + extraPad)

        # We pass the bitstring to bytes to write the file:
        encoded = int(bitstring, 2).to_bytes(
            int(len(bitstring) / 8), 'big')

        # We write the file
        with open(outputFile, 'wb') as output:
            # First we write the n_bits to be able to decompress the file.
            output.write(n_bits.to_bytes(ceil(n_bits / 256), 'big'))
            output.write(extraPad.to_bytes(1, 'big'))
            output.write(encoded)

        # print(t3 - t2, t2 - t1)

        if getDict is True:
            return self.table

    def compressFile(self, outputname=None):
        '''
        Alternative compressing method method

        '''

        filename, _ = os.path.splitext(self.file)
        if outputname:
            outputFile = outputname
        else:
            outputFile = filename + '.bin'

        with open(self.file, 'rb') as output:
            text = output.read()

        # text = [byte.to_bytes(1, 'big') for byte in bytestring]
        # t1 = time()

        compressed = []
        token = b''
        for i in range(len(text)):
            byte = text[i]
            token += byte.to_bytes(1, 'big')
            if token not in self.table:
                pos = self.table[token[:-1]]
                codeword = bin(pos)[2:] + bin(byte)[2:].zfill(8)
                self.table[token] = len(self.table)
                compressed.append(codeword)
                token = b''

        # If the last bytes have not been included (and so token is not empty):
        if token:
            pos = self.table[token[:-1]]
            codeword = bin(pos)[2:] + bin(byte)[2:].zfill(8)
            self.table[token] = len(self.table)
            compressed.append(codeword)

        # t2 = time()
        # print(t2 - t1)
        n_bits = int(log(len(self.table), 2)) + 1

        bitstring = ''.join([bits.zfill(n_bits + 8) for bits in compressed])

        # We add the padding to make len(bitstring) % 8 == 0:
        extraPad = 8 - len(bitstring) % 8 if len(bitstring) % 8 != 0 else 0
        bitstring = bitstring.zfill(len(bitstring) + extraPad)

        # We pass the bitstring to bytes to write the file:
        encoded = int(bitstring, 2).to_bytes(
            int(len(bitstring) / 8), 'big')

        # We write the file
        with open(outputFile, 'wb') as output:
            # First we write the n_bits to be able to decompress the file.
            output.write(n_bits.to_bytes(ceil(n_bits / 256), 'big'))
            output.write(extraPad.to_bytes(1, 'big'))
            output.write(encoded)

    def decompressFile(self, outputname=None):
        '''
        Here we will decompress the file:
        1. Read the n_bits used to write in binary each position.
        2. Read the extraPad and remove the zeros added to make
        len(bitstring) % 8 = 0.
        3. Knowing n_bits and knowing that each character is 8 bits
        long, read the encoded file in intervals of n_bits + 8, where
        the first n_bits will be the position (pos) and the next 8 bits
        will be the character (char) that follows that position.
        '''

        filename, _ = os.path.splitext(self.file)
        if outputname:
            outputFile = outputname
        else:
            outputFile = filename + '_decompressed.txt'

        keys = {0: b''}

        with open(self.file, 'rb') as output:
            n_bits = int.from_bytes(output.read(1), 'big')
            extraPad = int.from_bytes(output.read(1), 'big')
            encoded = output.read()
            n_bytes = len(encoded)
            encoded = int.from_bytes(encoded, 'big')
        bitstring = bin(encoded)[2:].zfill(n_bytes * 8)
        bitstring = bitstring[extraPad:]

        text = []
        for i in range(0, int(len(bitstring) / (n_bits + 8))):
            pos = bitstring[i * (n_bits + 8): n_bits +
                            i * (n_bits + 8)]
            last_char = bitstring[(i + 1) * n_bits +
                                  i * 8: (i + 1) * (n_bits + 8)]

            characters = keys[int(pos, 2)] + \
                int(last_char, 2).to_bytes(1, 'big')

            text.append(characters)
            keys[len(keys)] = characters

        with open(outputFile, 'w', encoding=self.encoding,
                  newline='\n') as output:
            text = b''.join(text)
            text = text.decode(self.encoding)
            output.write(text)
