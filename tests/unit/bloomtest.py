from bf2 import *


def test_passing():
    assert (1, 2, 3) == (1, 2, 3)


def test_bitmap_creation():
    bf = BloomFilter(1000)
    assert (1000) == (bf.bit_array.count(False))


def test_hash():
    tstr = "this is a fine string"
    #h1 = hash1(tstr.encode('8859'))
    #h2 = hash2(tstr.encode('8859'))
    #print('h is ', h1, h2)
    assert (1) == (True)
