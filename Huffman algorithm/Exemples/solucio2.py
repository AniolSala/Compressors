from heapq import heappush, heappop, heapify
from collections import defaultdict
from huffman import countProbs

def encode(symb2freq):
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

message = open('C:\\Users\\Aniol\\WPy-3661\\Arxius py\\Exercicis\\Parsing\\Huffman algorithm\\message.txt', 'r').read()

huff = encode(countProbs('message.txt'))
for p in huff:
    print(p[0], p[1])
