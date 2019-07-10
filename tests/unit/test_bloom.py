from bloom.bloomfilter import BloomFilter, openfile, setup_dict
import hashlib
import logging
from bitarray import bitarray
import subprocess

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('pytest bloom3')
logging.info("pytest bloomfilter")
logging.debug("debug")


def test_bitmap_creation():
    bf = BloomFilter(1000)
    assert (1000) == (bf.bit_array.count(False))


def test_bitmap_clear():
    bf = BloomFilter(1000)
    assert bf.bit_array.count(True) == 0


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


def test_ascii_wordlist():
    n = 100
    file = "tests/ascii_words.txt"
    print('n')
    bf = BloomFilter(n)
    tfileh, tencode = openfile(file)
#    setup_dict(bf, size_bitarray, dict_file, dfileh, dencode)
    setup_dict(bf, n, file, tfileh, tencode)
    test_bit_array = bitarray('0000000000000000000001000100000000000001010000000001000000000000000001010000000001000000000000101000')
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
    x, y = openfile("ThisFileShouldNotBefound.txt")
    assert x == 0 and y == 0


def test_write_test_file():
    fileh = open('./data/playdata/testdata.txt', 'w', encoding="iso-8859-1")
    fileh.write('zzz\n')
    fileh.write('étagère\n')
    fileh.write("étui's\n")
    fileh.close()
