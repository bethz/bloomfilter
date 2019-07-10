# bloomfilter.py

# Description
  This Github implements a Bloom filter  based spell checker in python. This work started from a useful idea about improving coding capability from [CodeKata](http://codekata.com/kata/kata05-bloom-filters/).
   
It includes:
  - a python implementation of a Bloom Filter 
  - input list for dictionary creation in iso-8859-1, Latin-1
  - logging in the Bloom Filter and in pytest
  - argparse to provide help with input parameters
  - unit tests using pytest

  Bloom filters are interesting because they are a very space efficient way to find if something is a member of a set when the set can be quite large.   False positives are possible but false negatives are not. Bloom Filters are [explained in detail.](https://en.wikipedia.org/wiki/Bloom_filter).


Summarized from [CodeKata](http://codekata.com/kata/kata05-bloom-filters/):
```
 Bloom filters work by initializing a big array of bits to zero.  Then, generate an independent hash value for each word in the list you want to look up, in this case, a list of dictionary words.  The hash is used to set the corresponding bit in the array of bits. It is not an issue if there are clashes in the bit array.

To check if a word is in the list, use the same hash that was used to set up the bitmap.  If the bits in the array corresponding to the hash are set,  the the word may be in the list. If not set, then that word is not in the list.

Sometimes a Bloom filter will report a false positive. This will not happen frequently as long as the bitmap is not heavily loaded.

```

The Bloom filter is full when at capacity:
```
 m * ((ln 2 ^ 2) / abs(ln p))

 where:
 m - number of bits in the bloom filter bit array
 p - the false positive probability

```
The [word list](here) used comes from SCOWL, which is Copyright 2000-2011 by Kevin Atkinson. 


Python provides a [Bloomfilter](https://github.com/wxisme/py-bloomfilter) but the goal of this project was to learn about implementing a Bloom filter so one was implemented.


# Usage
``` 
usage: python bloomfilter.py [-h] [--prob PROB] [--items ITEMS] [--showstats]

Try out a bloomfilter

optional arguments:
  -h, --help       show this help message and exit
  --prob PROB      Probability of false positive, integer percentages, 1 is 1
                   percent or 10 is 10 percent
  --items ITEMS    Number of items in dictionary to search
  --showstats      Use without value to show bloomfilter stats

This bloomfilter is not pip installable.
The dictionary file is in data/wordlist.txt
The words to search for are in data/searchwords.txt
During development, testing different dictionaries was accomplished by copying to these files. 
```

# Highlights


# Number of bits and false positive rate
```
Given:

    n: how many items you expect to have in your filter (e.g. 216,553)
    p: your acceptable false positive rate {0..1} (e.g. 0.01 → 1%) we want to calculate:
    m: the number of bits needed in the bloom filter
    k: the number of hash functions we should apply

The formulas:

m = -n*ln(p) / (ln(2)^2) the number of bits

k = m/n * ln(2) the number of hash functions

Assumptions:

n = 400,000 
    Note: The dictionary list has 338,882 items. This number was rounded up for convenience.
p = 1%

```

[Calculation info](https://stackoverflow.com/questions/658439/how-many-hash-functions-does-my-bloom-filter-need)

# Interesting Items
- Character encoding

	[Joelonsoftware](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/)

	[Quick summary of that](https://medium.com/@joffrey.bion/charset-encoding-encryption-same-thing-6242c3f9da0c)

- hashing for Bloom filters is different than filters for cryptographic functions
- hashing for Bloom filters should be very, very fast with uniform spread
- [Python Hash functions](https://www.pythoncentral.io/hashing-strings-with-python/)

- Here's a [paper](http://bit.ly/rgYdK3) that shows that you can similuate n hash functions with just 2 hash functions.

- Python stores text in Unicode code points. A bit of knowledge is necessary to [process these properly](http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html). I used a provided wordlist that was Latin-1.  In particular, the process of converting from a sequence of bytes (i.e. binary data) to a sequence of code points (i.e. text data) is decoding, while the reverse process is encoding. Latin-1 maps byte values directly to the first 256 Unicode points. Note that Windows has it's own "latin-1" variant called cp1252 but does not map all 256 possible byte values.  Converting between and learning the nuances was an interesting learning experience.

- A docker container was used to run this code and the pytest.  I learned to use vscode on my local system to connect to the docker container to leverage it's environment.

# Unit Tests

```
Run unit tests:

    python -m pytest -v -s tests/unit/testbloom.py
```

Unit tests demonstrate testing of base functionality
- Each and every word in the dictionary is not tested to confirm it returns true
- false positives are hard to test

# Interesting References
[Intro to Bloom Filters](https://www.geeksforgeeks.org.bloom-filters-introduction-and-python-implementation/)

# DevOps
No DevOps at this time.

# bloomfilter note

- it's difficult to write test for false positive
    However, how do we write unit tests for false positives? It’s impossible to write a conclusive unit test for the “includes” method since returning True does not necessarily mean the word exists. We can run the test repeatedly to determine the probability of getting a false positive and determine if that matches our theoretical calculations, but, as Prashanth brought up, this kind of testing isn’t unit testing because running the same test doesn’t always return True.
