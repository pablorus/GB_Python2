from collections import OrderedDict
import os
import re
import hashlib
import unittest


__author__ = "Vasilii Moskvin"


def get_hash_summ(in_byte, in_code):
    """
    Returns a hexdigest of a in_byte.
    :param in_byte: input byte string
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
    h.update(in_byte)

    return h.hexdigest()


# ------------------------------------------------------3.1------------------------------------------------------------

'''
    Реализовать функцию разбиения файла на кусочки указанной длины.

        На входе: имя исходного файла и размер в байтах для разрезания файла<br>
        На выходе: количество полученных файлов-фрагментов

'''


def cut_file(file_path, size):
    """
    Cuts the file 'file_path' into several parts of the size 'size'
    :param file_path: path to file
    :param size: size of parts
    :return: several parts of the file 'file_path'

    """
    dir_path = os.sep.join(file_path.split(os.sep)[:-1])
    with open(file_path, 'rb') as f:
        raw_data = f.read()

    reg = '.{{1,{}}}'.format(size)
    data = re.findall(bytes(reg, encoding='utf-8'), raw_data, re.DOTALL)

    for index, src in enumerate(data):
        with open(os.path.join(dir_path, 'cut_{}'.format(str(index))), 'wb') as f:
            f.write(src)

    return str(index)


def tst_cut_file(file_path, dir_path):
    """
    Tests function cut_file(file_path, size)
    :param file_path: path to cut file
    :param dir_path: path to directory with cut file
    :return: error, if the file was not properly cut

    """
    lst_dir = [os.path.join(dir_path, filename) for filename in os.listdir(dir_path) if filename.startswith('cut_')]

    log_path = os.path.join(dir_path, 'log.jpg')
    with open(log_path, 'wb') as f:
        for src in sorted(lst_dir, key=lambda x: float(re.findall(r'.*_(\d+)$', x)[0])):
            with open(src, 'rb') as temp_f:
                temp_data = temp_f.read()
            f.write(temp_data)

    with open(log_path, 'rb') as f:
        log_data = f.read()
    log_hash = get_hash_summ(log_data, 'md5')

    with open(file_path, 'rb') as f:
        file_data = f.read()
    file_hash = get_hash_summ(file_data, 'md5')

    os.remove(log_path)

    assert log_hash == file_hash, 'Cut file error'


# ------------------------------------------------------3.2------------------------------------------------------------

'''
    Реализовать функцию составления текстового файла с md5-хэшами файлов в указанной директории

        На входе: имя директории с файлами, имя файла для записи результатов<br>
        На выходе: количество просмотренных файлов

'''


def get_hash_in_dir(dir_path, res_path):
    """
    Returns file with the list of hash summs from files in the dir_path.
    :param dir_path: path to directory with files
    :param res_path: path to result files
    :return: file with the list of hash summs from files in the dir_path

    """
    lst_files = [os.path.join(dir_path, file_name) for file_name in os.listdir(dir_path)
                 if not file_name.endswith('.md5')]

    lst_hash = []
    for file_path in lst_files:
        with open(file_path, 'rb') as f:
            data = f.read()
        lst_hash.append(get_hash_summ(data, 'md5'))

    with open(res_path, 'w') as f:
        for hash_line in lst_hash:
            f.write('{}\n'.format(hash_line))

    return len(lst_files)


# ------------------------------------------------------3.3------------------------------------------------------------

'''
    Реализовать функцию "склеивания" файла на основе упорядоченных хэш-сумм

        На входе: имя директории с файлами-кусочками, имя файла с хэш-суммами, имя выходного файла<br>
        На выходе: размер полученного файла

'''


def get_full_file(dir_path, md5_file_path, res_path):
    """
    Creates full file from many parts.
    :param dir_path: path to directory with parts of full file
    :param md5_file_path: path to list of hash summs
    :param res_path: path to result file
    :return: Creates full file from many parts

    """
    lst_files = [os.path.join(dir_path, file_name) for file_name in os.listdir(dir_path)
                 if not file_name.endswith('.md5')]

    with open(md5_file_path, 'r') as f:
        hash_summ = OrderedDict(map(lambda line: (line.strip(), ''), f))

    for file_path in lst_files:
        with open(file_path, 'rb') as f:
            data = f.read()
        h = hashlib.md5()
        h.update(data)
        hash_summ[h.hexdigest()] = file_path

    with open(res_path, 'wb') as f_res:
        for hash, file_path in hash_summ.items():
            with open(file_path, 'rb') as f:
                data = f.read()
            f_res.write(data)

    return os.path.getsize(res_path)


def main():
    # --------------------------------------3.1-----------------------------------------------------------------------

    print('№ 3.1 "Cut file"')
    dir_path = os.path.abspath(input('Enter path to directory with cut file:\n'))
    file_path = os.path.join(dir_path, input('Enter the name of cut file:\n'))
    size = int(input('Enter the size of cut parts (bytes):\n'))

    print('Count of new files: {}'.format(cut_file(file_path, size)))

    tst_cut_file(file_path, dir_path)

    # --------------------------------------3.2-----------------------------------------------------------------------

    print('№ 3.2 "List of hash in a directory"')
    dir_path = os.path.abspath(input('Enter path to directory with files:\n'))
    res_path = os.path.abspath(input('Enter path to result file:\n'))

    print('Viewed {} files'.format(get_hash_in_dir(dir_path, res_path)))

    # --------------------------------------3.3-----------------------------------------------------------------------

    print('№ 3.3 "Creates full file from many parts."')
    dir_path = os.path.abspath(input('Enter path to directory with files:\n'))
    md5_file_path = os.path.abspath(input('Enter path to file with list of hashes:\n'))
    res_path = os.path.abspath(input('Enter path to result file:\n'))

    print('Size of reuslt file: {} bytes'.format(get_full_file(dir_path, md5_file_path, res_path)))


if __name__ == '__main__':
    main()
