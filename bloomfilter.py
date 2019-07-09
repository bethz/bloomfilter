# -*- coding: utf-8 -*-
import logging
import argparse
import subprocess
import mmh3
from math import log
from bitarray import bitarray


class Logging_setup(object):
    @property
    def logger(self):
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)


class BloomFilter(Logging_setup):
    """
    A hash function takes input and outputs a unique identifier of fixed
    length which is used for identification of input.

    """
    def __init__(self, size):
        """
        Init the Bloomfilter
        Arguments:
        size - size of the bitarray

        Return:
        Ref to Bloomfilter
        """

        self.bit_array = bitarray(size)
        self.n = size
        # initialize to zero
        self.bit_array.setall(0)

        logging.debug("in Bloomfilter")
        logging.debug('array[1000000] {a}'.format(a=self.bit_array[:100]))
        logging.debug("check count for 1's {a}".format(
                    a=self.bit_array.count(True)))
        logging.debug("check count for 0's {a}".format(
                      a=self.bit_array.count(False)))

    def insert(self, line, n):
        """
        Insert into BloomFilter according to hashes
        Arguments:
        line - entry for bloomfilter
        n    - size of the bloomfilter, num bits

        Return:
        index1 - first hash
        index2 - second hash
        """

        # mod to size of bitarray
        index1 = mmh3.hash((line.encode('utf-8')), 1) % n
        self.bit_array[index1] = 1
        index2 = mmh3.hash((line.encode('utf-8')), 3) % n
        self.bit_array[index2] = 1
        logging.debug("insert line {} index {} index {}".format(
                      line.encode('utf-8'), index1, index2))
        return index1, index2

    def check():
        pass

    def find_word(self, line, n):
        """
        Find if the word is in the dictionary with indices
        Arguments:
        line - check for this line in the bloomfilter
        n - size of bloomfilter
        Return:
        {True:False} - True if found, False if not
        indices - the indices if found, else 0,0
        """
        logging.debug("in search")
        h1 = mmh3.hash((line.encode('utf-8')), 1) % n
        h2 = mmh3.hash((line.encode('utf-8')), 3) % n
        # j = h1 % self.n
        j = int(h1) % n
        k = int(h2) % n
        logging.debug("find line {} index {} index {}".format(line.encode(
                     'utf-8'),
                     h1, h2))

        if self.bit_array[h1] == 0 or self.bit_array[h2] == 0:
            return(False, 0, 0)
        else:
            return(True, j, k)


def openfile(file):
    """
    Open a file with it's encoding
    Arguments:
    file - filename to open

    Return:
    fileh   - file reference
    fencode - file encoding
    """

    fencode = subprocess.getoutput('file -b --mime-encoding %s' % file)
    fileh = open(file, encoding=fencode)
    logging.debug("fencode ".format(fencode))
    return fileh, fencode


def setup_dict(bf, n, file, fileh, fencode):
    """
    Arguments:
    bf      - reference to bloomfilter
    n       - size of bloomfilter 
    file    - filename
    fileh   - reference to file
    fencode - file encoding

    Return:
    None
    """

    line = fileh.readline()
    i = 0
    while line:
        x, y = bf.insert(line, n)
        logging.debug(" line {}. {} ".format(i+1, line))
        logging.debug(" bitarray {0}".format(bf.bit_array))
        # if (i < 10 or i > 338770):
        if (i < 10 or i > 470):
            # encodel = line.encode("utf-8")
            logging.debug(" line is {}. {}".format(i+1, line))
            logging.debug("8859 {}. {} {}".format(
                          i+1,
                          fencode,
                          line.encode(fencode, "ignore").decode("utf-8",
                                                                "ignore")))
            logging.debug("8859 {}. {} {}".format(i+1,
                                                  fencode,
                                                  line.encode(fencode,
                                                              "ignore")))

        i += 1
        line = fileh.readline()

    logging.debug(" Dictionary file {0} has {1} lines, file_encoding is {2}"
                  .format(file, i, fencode))


def read_search_list(bf, n, file, fileh, fencode):
    """
    Read the list of strings to search for

    Arguments:
    bf - bloomfilter
    n - 
    file - file to read words from
    fileh - file reference
    fencode - file encoding

    Return:
    none
    """

    line = fileh.readline()

    i = 0
    while line:
        logging.debug("looking for words")
        fnd, j1, j2 = bf.find_word(line, n)
        if fnd:
            logging.info(" line is FOUND! {}. {}".format(i+1,
                          line.encode("iso-8859-1")))
        else:
            logging.debug("\n line is NOT found!{} ".format(line))

        i += 1
        line = fileh.readline()
        if fnd:
            logging.debug("Found {0} set {1} {2}".format(line, j1, j2))
            continue
    logging.info("Search file {0} contains {1} lines, file encoding is \
                 {2}".format(file, i, fencode))


def calc_bf_sizes(n, p):
    """
    Calculate the number of bits and number of hash functions
    recommended for the bloom filter.

    Arguments:
    n: how many items you expect to have in your filter (ie 400,000
       in dictionary)
    p: your acceptable false positive rate {0..1} (e.g. 0.01 → 1%)

    Return:
    m: the number of bits needed in the bloom filter
    k: the number of hash functions to apply in order to obtain the
       desired false positive rate
    """

    ln2 = log(2)  # no base means natural ln
    m = int((-n * log(p)) / (ln2) ** 2)
    k = (m/n) * ln2
    logging.info('BloomFilter stats \n Number of bits in bitarray: {0}, \
                 \n Number of hash functions {1} \n False Positive rate: \
                 {2}%\n'.format(m, k, p*100))
    return m, k


def create_arg_parser():
    """
    Many of the argument defaults are used as arg_parser makes it easy to
    use defaults. The user has many options they can select.
    """

    parser = argparse.ArgumentParser(description='Process some inputs')
    # script to run pytest
    parser.add_argument("--prob",
                        action="store",
                        default=1,
                        type=int,
                        help="Desired probability, 1 is 1%, 10 is 10% etc")
    parser.add_argument("--items",
                        action="store",
                        default=326000,
                        help="Number of items in dictionary to search")
    parser.add_argument("--target",
                        action="store",
                        default='zzz',
                        help="Target to search for in dictionary")
    args = parser.parse_args()

    return args


def main():
    """
     This implements a Bloom filter based spell checker in python.
     It includes:
        - pytest unit tests
        - argparse for command line inputs
        - logging in the Bloom Filter and in pytest

    Bloom filters are interesting because they are a very space efficient way
    to find if an element is a member of a set when the set can be quite large.

    False positives are possible but false negatives are not. Bloom Filters
    are explained [here](https://en.wikipedia.org/wiki/Bloom_filter).


    Basic function
    - add strings in a dictionary to the Bloom filter
    - query the Bloom filter for search strings:
             - some are known to be in the Bloom filter
             - some are known NOT to be in the Bloom filter
    This Bloom filter example uses an input file with ISO-8859-1, Latin-1.
    All strings are converted to utf-8 so that it will work with most input
    string types.

    Also, strings are terminated with \n on input.  It was decided that
    stripping off the \n was not worth time or effort so \n is included
    in the string.

    """
    args = create_arg_parser()
    items_in_filter = args.items
    prob_false_neg = args.prob/100
    dict_file = "data/wordlist.txt"
    search_file = "data/searchwords.txt"

    size_bitarray, k = calc_bf_sizes(items_in_filter, prob_false_neg)
    logging.debug('Set up BF')
    bf = BloomFilter(size_bitarray)

    logging.debug('read dictionary')
    dfileh, dencode = openfile(dict_file)
    # read and insert into Bloomfilter
    setup_dict(bf, size_bitarray, dict_file, dfileh, dencode)
    dfileh.close()

    logging.debug('read search list')
    sfileh, sencode = openfile(search_file)
    read_search_list(bf, size_bitarray, search_file, sfileh, sencode)
    sfileh.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('bloom3')
    logging.debug("bloomfilter")
    logging.debug("debug")

    main()
