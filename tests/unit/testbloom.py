# -*- coding: utf-8 -*-
from bloomfilter import read_wordlist, BloomFilter, read_wordsearch
import hashlib
import logging
from bitarray import bitarray
import subprocess
import pytest

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('pytest bloom3')
logging.info("pytest bloomfilter")
logging.debug("debug")


def test_bitmap_creation():
    bf = BloomFilter(1000)
    assert (1000) == (bf.bit_array.count(False))


def test_hash():
    tstr = "this is a fine string"
    tstr = "écrit ça dans un fichier"
    # https://stackoverflow.com/questions/5297448/how-to-get-md5-sum-of-a-string-using-python
    # https://stackoverflow.com/questions/7585307/how-to-correct-typeerror-unicode-objects-must-be-encoded-before-hashing
    # md5 operates on bytes so encode str into bytes
    # The MD5 message digest hashing algorithm processes data in 512-bit
    # blocks, broken down into 16 words composed of 32 bits each. The output
    # from MD5 is a 128-bit message digest value.

    h = hashlib.md5(tstr.encode('utf-8')).hexdigest()
    h1 = hashlib.md5(tstr.encode('utf-8')).hexdigest()
    assert (h) == (h1)


def test_insert():
    line = u'écrit'
    bf = BloomFilter(100)
    i1, i2 = bf.insert(line, bf.n)

    logging.debug('\n my line {0}'.format(line.encode('utf-8')))
    logging.debug('\n whoset: \n bits {0} set: {0}  index: {2} \
                  index: {3} '.format(bf.bit_array,
                  bf.bit_array.count(True), i1, i2))
    logging.debug('n')
    assert [i1, i2, bf.bit_array.count(True), bf.bit_array.count(False)] == [
        89, 61, 2, 98]


def test_read_wordlist():
    n = 100
    file = "tests/ascii_words.txt"
    print('n')
    bf = BloomFilter(n)
    read_wordlist(bf, n, file)
    test_bit_array = bitarray('000000000000000000000100010000000000000101000000y0001000000000000000001010000000001000000000000101000')
    print('\n *******************\n bf and set \n', bf.bit_array)
    print('\n Test_bit_array \n', test_bit_array)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    assert (bitarray(test_bit_array) == bf.bit_array)


def test_search_one_word():
    n = 100
    file = "tests/ascii_words.txt"
    print('n')
    bf = BloomFilter(n)
    print('n')
    file_encoding = subprocess.getoutput('file -b --mime-encoding %s' % file)
    fileIN = open(file, encoding=file_encoding)
    line = fileIN.readline()
    i1, i2 = bf.insert(line, bf.n)
    fnd, j, k = bf.find_word(line, n)
    print("\n ***********after word one\n", bf.bit_array)

    assert ([fnd, i1, i2]) == ([True, j, k])


def test_search_two_words():
    n = 100
    file = "tests/ascii_words.txt"
    print('n')
    bf = BloomFilter(n)
    print('n')
    file_encoding = subprocess.getoutput('file -b --mime-encoding %s' % file)
    fileIN = open(file, encoding=file_encoding)
    line = fileIN.readline()
    i1, i2 = bf.insert(line, bf.n)
    fnd1, j1, j2 = bf.find_word(line, n)
    print("\n ***********after word one\n", bf.bit_array)
    line = fileIN.readline()
    i3, i4 = bf.insert(line, bf.n)
    fnd2, j3, j4 = bf.find_word(line, n)
    print("\n ***********after word two\n", bf.bit_array)
    assert ([fnd1, fnd2, i1, i2, i3, i4]) == ([True, True, j1, j2, j3, j4])


def test_no_wordfile():
    n = 100
    bf = BloomFilter(n)
    with pytest.raises(Exception):
        read_wordsearch(bf, n, "ThisFileShouldNotBefound.txt")


def test_write_test_file():
    fileh = open('./data/playdata/testdata.txt', 'w', encoding="iso-8859-1")
    fileh.write('zzz\n')
    fileh.write('étagère\n')
    fileh.write("étui's\n")
    fileh.close()


'''
what if not latin-1 file? will it work?
max size of input line


def test_read_wordlist_file():
    bf = BloomFilter(100)
    file="tests/oneline.txt"
    file_encoding = subprocess.getoutput('file -b --mime-encoding %s' % file)

    file_stream = codecs.open(file, 'r', file_encoding)
    print("\n opened input file {a} and {b}", file,
                 file_encoding)
    i = 0

    for line in file_stream:
        print(line.encode('8859'))
        bf.insert(line.encode('8859'), bf.n)
        i += 1
    for line in file_stream:
        line =u'écrit'
        index = mmh3.hash((line.encode('utf-8')), 1) % bf.n
        bf.bit_array[index] = 1
        # index2 = mmh3.hash((line.encode('utf-8')), 2) % bf.n
        index2 = mmh3.hash((line.encode('utf-8')), 2) % bf.n
        bf.bit_array[index2] = 1
        print("line", line.encode('utf-8'))
    # read_wordlist_file(bf, bf.n, file="oneline.txt")
    print("bf.array",bf.bit_array, bf.bit_array.count(True), index, index2)

    print("bf.array", bf.bit_array, bf.bit_array.count(True))
    assert (1) == (True)
'''
