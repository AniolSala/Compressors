from time import time
import os
from collections import Counter


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
    def __init__(self, filename, path=os.getcwd(), encoding='utf-8'):
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
        self.path = path + '\\'
        self.file = self.path + filename
        self.encoding = encoding
        self.charDist = {}
        self.tree = []
        self.HuffmanTable = {}

    def probDist(self):
        '''
        To count the words we follow the next method:
        1. We open the txt file in the variable text.
        2. We take the first character and we count how many times this
        character appears.
        3. We add the character and its count number to the charDist
        dictionary.
        4. We delete the character from text. Return to point 2 until text
        is an empty string.
        5. Finally the charDist is returned.
        '''

        with open(self.file, 'r', encoding=self.encoding) as output:
            self.charDist = dict(Counter(output.read()))

        self.charDist = dict(sorted(self.charDist.items(),
                                    key=lambda x: x[1], reverse=True))

    def buildTable(self):
        '''Here we will build the 'tree', this is, the collection of
        nodes of the huffman code. The codewords will be assigned based
        on this tree'''

        tempnodes = []
        self.probDist()
        for val in self.charDist.values():
            node = Node(weight=val)
            tempnodes.append(node)
            self.tree.append(node)

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

        i = 0
        for key in self.charDist:
            self.HuffmanTable[key] = self.tree[i].s
            i += 1

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

    @timer
    def compressFile(self, outputname=None, getDict=None):
        '''
        Here we will compress the file using the following steps:
        1. Open the file in the variable called text, and subsitute
        each character in text for its codeword using self.HuffmanTable.
        This new string is called bitstring.
        2. If the length of the bitstring is not multiple of 8, add the
        zeros at the end of the string to ensure len(bitstring) % 8 = 0.
        3. Split bitstring in parts of 8 bits, and create a bytearray from
        this.
        4. Finally, open the file in 'wb' mode and write the bytestring.
        '''

        filename, _ = os.path.splitext(self.file)
        if outputname:
            outputFile = self.path + outputname
        else:
            outputFile = filename + '.bin'

        # 1. We build the HuffmanTable and create the bitstring.
        self.buildTable()
        with open(self.file, 'r', encoding=self.encoding) as output:
            text = output.read()
            codeWordArray = [self.HuffmanTable[x] for x in text]
            bitstring = ''.join(codeWordArray)

        # 2. Adding extra padding to force len(coded_file) % 8 == 0
        extraPad = 8 - len(bitstring) % 8 if len(bitstring) % 8 != 0 else 0
        bitstring = bitstring.zfill(extraPad + len(bitstring))

        padded_info = "{0:08b}".format(extraPad)
        bitstring = padded_info + bitstring

        # 3. Split bitstring in parts of 8 bits and create the bytearray
        b = bytearray([int(bitstring[i:i + 8], 2)
                       for i in range(0, len(bitstring), 8)])

        # 4. Write the bytearray in the new file:
        self.writeDict(outputFile)
        with open(outputFile, 'ab') as output:
            output.write(bytes('\n'.encode(self.encoding)))
            output.write(bytes(b))

        if getDict:
            return self.HuffmanTable

    @timer
    def decompressFile(self, outputname=None):
        '''
        Here we will decompress the file using the following methods:
        1. Get the dictionary.
        2. Find the length of the shorted codeword.
        3. Open the file and substitute all codewords for its character.
        4. Write the translated codeword to the new file.
        '''

        # t1 = time.clock()
        filename, _ = os.path.splitext(self.file)
        if outputname:
            outputFile = self.path + outputname
        else:
            outputFile = filename + '_decompressed.txt'

        with open(self.file, 'rb') as inputfile:

            # We first read and build the dictionary!
            dictionary = b''
            while b'\n\n' not in dictionary:
                dictionary += inputfile.read(1)
            dictionary = dictionary.decode(self.encoding)[:-2]
            dictionary = dictionary.split(';.')
            dictionary = dict([element.split(':.') for element in dictionary])

            # We now read the bytearray
            b = inputfile.read()

        bitsarray = [bin(x)[2:].zfill(8) for x in b]
        bitsarray = ''.join(bitsarray)
        padding = int(bitsarray[:8], 2)
        bitsarray = bitsarray[8 + padding:]

        # t2 = time.clock()
        codewords = ''
        decompressed = []
        for bit in bitsarray:
            codewords += bit
            if codewords in dictionary:
                decompressed.append(dictionary[codewords])
                codewords = ''
        decompressed = ''.join(decompressed)

        with open(outputFile, 'w', encoding=self.encoding) as output:
            output.write(decompressed)

        # t3 = time.clock()
        # print(t3 - t2, t2 - t1)

    def decompress2(self, outputname=None):
        '''
        Alternative decompression (more efficient than decompress method)
        '''

        # t1 = time.time()
        filename, _ = os.path.splitext(self.file)
        if outputname:
            outputFile = self.path + outputname
        else:
            outputFile = filename + '_decompressed.txt'

        with open(self.file, 'rb') as inputfile, open(
                outputFile, 'w', encoding=self.encoding,
                newline='\n') as output:

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

            # t2 = time.time()
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
