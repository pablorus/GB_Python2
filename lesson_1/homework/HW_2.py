from collections import OrderedDict
import csv
import doctest
import hashlib
import unittest

import pytest  # Run from console 'python -m pytest HW_2.py'


__author__ = "Vasilii Moskvin"


class TestHashSumm(unittest.TestCase):
    def test_hash_summ(self):
        self.assertEqual(get_hash_summ('I love Python', 'sha1'), '9233eac58259dd3a13d6c9c59f8001823b6b1fee')

    def test_hash_summ_exc(self):
        with self.assertRaises(KeyError):
            get_hash_summ('X', 'X')


def tst_hash_summ(in_string, in_code, ans):
    assert get_hash_summ(in_string, in_code) == ans, 'Неверная сумма'


def get_hash_summ(in_string, in_code):
    """
    Returns a hexdigest of a in_string.
    :param in_string: input string
    :param in_code: hash algorithm
    :return: a hexdigest of a in_string

    >>> get_hash_summ('I love Python', 'sha1')  # doctest: +NORMALIZE_WHITESPACE
    '9233eac58259dd3a13d6c9c59f8001823b6b1fee'

    """
    dct_hash = dict(sha1=hashlib.sha1,
                    sha224=hashlib.sha224,
                    sha256=hashlib.sha256,
                    sha384=hashlib.sha384,
                    sha512=hashlib.sha512,
                    md5=hashlib.md5)

    h = dct_hash[in_code]()
    h.update(in_string.encode('utf-8'))

    return h.hexdigest()


def main():
    """
    Main function. Reads need_hashes.csv. Gets hexdigest for all strings in the file.
    And appends the received codes in need_hashes.csv.
    :return: chenged need_hashes.csv

    """
    filename = 'need_hashes.csv'
    my_struct = ('string', 'code', 'hex_digest')

    with open(filename, 'r') as csv_file:
        csv_file = csv.reader(csv_file, delimiter=';')
        data = [OrderedDict(zip(my_struct, row)) for row in csv_file]

    for src in data:                                                    # Вопрос: Как можно такую конструкцию в одну
        src['hex_digest'] = get_hash_summ(src['string'], src['code'])   # строку записать?

    with open(filename, 'w', newline='') as csv_file:
        csv_file = csv.DictWriter(csv_file, delimiter=';', fieldnames=my_struct)
        csv_file.writerows(data)


def run_test():
    """
    Conducts tests get_hash_summ(in_string, in_code).
    assert, doctest, unittest
    :return: Results of tests get_hash_summ(in_string, in_code)

    """
    tst_hash_summ('I love Python', 'sha1', '9233eac58259dd3a13d6c9c59f8001823b6b1fee')
    doctest.testmod()
    unittest.main()


if __name__ == '__main__':
    #run_test()
    main()
