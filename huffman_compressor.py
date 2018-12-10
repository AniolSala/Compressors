from time import time
import os
from collections import Counter


class Node():

    def __init__(self, weight=None, childs=[], symbol=''):
        '''
        If the node has no childs, the weight must be set
        explicitly; if the node has childs its weight will be
        the sum of the weights of its childrens
        '''

        if len(childs) == 0:
            self.w = weight
        elif len(childs) == 2:
            self.w = childs[0].w + childs[1].w
        self.c = childs
        self.s = symbol


class Huffman():
    def __init__(self, filename, encoding='utf-8'):
        '''
        We assume that the file is in the same folder as the program, and an
        encoding of utf8.
        The variable self.nodes will be the tree that caracterizes the
        Huffman code.
        The charDist variable will be the character distribution probability
        of the file.
        The HuffmanTable variable will be the Huffman dictionary containing
        each character and its codeword.
        '''
        self.file = filename
        self.encoding = encoding
        self.charDist = {}
        self.tree = []
        self.HuffmanTable = {}

    def writeDict(self, filename=None, dictionary=None):
        '''
        Here we will write the dictionary at the beginning of
        the file.
        '''

        if not dictionary:
            dic = self.HuffmanTable
        else:
            dic = dictionary

        if not filename:
            file = self.file
        else:
            file = filename

        with open(file, 'wb') as output:
            for key, val in dic.items():
                output.write(val.encode(self.encoding))
                output.write(':.'.encode(self.encoding))
                output.write(key.encode(self.encoding))
                if key == list(dic)[-1]:
                    output.write('\n'.encode(self.encoding))
                else:
                    output.write(';.'.encode(self.encoding))

    def compressFile(self, outputname=None, getDict=None):
        '''
        Function to compress the file.
        '''

        if outputname:
            outputFile = outputname
        else:
            name, _ = os.path.splitext(self.file)
            outputFile = name + '.bin'

        tempnodes = []
        with open(self.file, 'r', encoding=self.encoding) as inputfile:
            text = inputfile.read()
        self.charDist = dict(Counter(text))

        self.tree = [Node(weight=val) for val in self.charDist.values()]
        tempnodes = self.tree.copy()

        while len(tempnodes) > 1:
            # We build a father node and we add it to the tree list:
            fnode = Node(childs=[tempnodes[-2], tempnodes[-1]])
            self.tree.append(fnode)
            # We delete the last two nodes of tempnodes and add the new one:
            tempnodes.remove(tempnodes[-1])
            tempnodes[-1] = fnode
            # We sort tempnodes to heaviest to lightest:
            tempnodes = sorted(tempnodes, key=lambda x: x.w, reverse=True)

        for node in self.tree[::-1]:
            if len(node.c) == 2:
                node.c[0].s = node.s + '0'
                node.c[1].s = node.s + '1'

        self.HuffmanTable = dict([[key, self.tree[i].s]
                                  for i, key in enumerate(self.charDist)])

        codeWordArray = [self.HuffmanTable[x] for x in text]
        bitstring = ''.join(codeWordArray)

        # 2. Adding extra padding to force len(coded_file) % 8 == 0
        extraPad = 8 - len(bitstring) % 8 if len(bitstring) % 8 != 0 else 0
        bitstring = bitstring.zfill(extraPad + len(bitstring))

        padded_info = "{0:08b}".format(extraPad)
        bitstring = padded_info + bitstring

        # 3. Split bitstring in parts of 8 bits and create the bytearray
        b = int(bitstring, 2).to_bytes(int(len(bitstring) / 8), 'big')

        # 4. Write the bytearray in the new file:
        self.writeDict(outputFile)
        with open(outputFile, 'ab') as output:
            output.write(bytes('\n'.encode(self.encoding)))
            output.write(bytes(b))

        if getDict:
            return self.HuffmanTable

    def decompressFile(self, outputname=None):
        '''
        Here we will decompress the file using the following methods:
        1. Get the dictionary.
        2. Find the length of the shorted codeword.
        3. Open the file and substitute all codewords for its character.
        4. Write the translated codeword to the new file.

        '''

        if outputname:
            outputFile = outputname
        else:
            filename, _ = os.path.splitext(self.file)
            outputFile = filename + '_decompressed.txt'

        with open(self.file, 'rb') as inputfile,\
                open(outputFile, 'w', encoding=self.encoding, newline='\n') as output:

            # We first read and build the dictionary!
            dictionary = b''
            while b'\n\n' not in dictionary:
                dictionary += inputfile.read(1)
            dictionary = dictionary.decode(self.encoding)[:-2]
            dictionary = dictionary.split(';.')
            dictionary = dict([element.split(':.') for element in dictionary])

            # We now read the bytearray
            extraPad = int.from_bytes(inputfile.read(1), 'big')
            b = inputfile.read()

            n_bytes = len(b)
            bitstring = bin(int.from_bytes(b, 'big'))[2:].zfill(n_bytes * 8)
            bitstring = bitstring[extraPad:]

            # We now translate the codewords to the original characters:
            decompressed = []
            token = ''
            for bit in bitstring:
                token += bit
                if token in dictionary:
                    decompressed.append(dictionary[token])
                    token = ''

            output.write(''.join(decompressed))

    def decompressFile2(self, outputname=None):
        '''
        Alternative decompression (more efficient than decompress method)
        '''

        filename, _ = os.path.splitext(self.file)
        if outputname:
            outputFile = outputname
        else:
            outputFile = filename + '_decompressed.txt'

        with open(self.file, 'rb') as inputfile, open(outputFile,
                                                      'w', encoding=self.encoding, newline='\n') as output:

            # We first read and build the dictionary!
            dictionary = b''
            while b'\n\n' not in dictionary:
                dictionary += inputfile.read(1)
            dictionary = dictionary.decode(self.encoding)[:-2]
            dictionary = dictionary.split(';.')
            dictionary = dict([element.split(':.') for element in dictionary])

            # We now read the bytearray
            extraPad = int.from_bytes(inputfile.read(1), 'big')
            b = inputfile.read()

            n_bytes = len(b)
            bitstring = bin(int.from_bytes(b, 'big'))[2:].zfill(n_bytes * 8)
            bitstring = bitstring[extraPad:]

            # We now translate the codewords to the original characters:
            codewords = ''
            decompressed = []
            for bit in bitstring:
                codewords += bit
                if codewords in dictionary:
                    decompressed.append(dictionary[codewords])
                    codewords = ''

            decompressed = ''.join(decompressed)

            output.write(decompressed)
