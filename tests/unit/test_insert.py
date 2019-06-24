from bf2 import *


def test_passing():
    assert (1, 2, 3) == (1, 2, 3)


def test_known_value_in_list():
    pass


def test_value_not_in_list():
    pass


def test_bitmap_clear():
    bf = bf2.BloomFilter(1000)
    print('bf.count ', bf.count())
    assert (1,2) == (1,2)
    pass


def test_add_first_entry():
    # check a known value is entered
    pass


def test_add_same_word_twice():
    # check no other values are set
    pass


def test_word_not_there():
    pass


if __name__ == "__main__":

    test_passing()
    test_bitmap_clear()
