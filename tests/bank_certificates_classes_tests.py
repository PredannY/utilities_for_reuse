import unittest
import os
from classes.bank_certificates_classes import BankCertificatesContainer, BankCertificateFile
from utils.file_utils import create_temp_dir, remove_dir


def create_new_file(file_dir, any_file_name) -> None:
    """
    Функция, предназначенная для создания нового файла.
    :param str file_dir: путь до файла
    :param str any_file_name: имя файла
    """
    full_any_file_dir = os.path.join(file_dir, any_file_name)
    any_file = open(full_any_file_dir, mode='w')
    any_file.write('Some comment')
    any_file.close()


class TestBankCertificateFile(unittest.TestCase):
    """
    Unit test для тестирования компонент get_certificates_list и certificate_name_parse
    """
    certificates_list = [
        'dddddd',  # False
        '0648.11111111111.20220923174555.zzz',  # False
        '0646.11111111111.20241323174555.cer',  # False
        '0646.11111111111.202413231745.cer',  # False
        '8754.11111111111.2021z812143545.cer',  # False
        '0647.11111111111.20220923174555.del',  # True
        '0646.11111111111.20220923174555.cer',  # True
        '0645.11111111111.20220923174555.cer',  # True
    ]

    def test_certificates_container(self):
        # Создать временную папку
        temporary_folder = create_temp_dir()
        try:
            # Создать временные файлы
            for certificate in self.certificates_list:
                create_new_file(temporary_folder, certificate)
            bank_certificates_container_obj = BankCertificatesContainer(temporary_folder)
            # Сравнить количество элементов списка с int. Если количество элементов равно int - тест пройден
            self.assertEqual(len(bank_certificates_container_obj.get_valid_certificates_list()), 3)
        finally:
            # Удалить временную папку
            remove_dir(temporary_folder)

    def test_certificate_file(self):
        # Создать временную папку
        temporary_folder = create_temp_dir()
        try:
            # Создать временные файлы
            for count, certificate in enumerate(self.certificates_list):
                create_new_file(temporary_folder, certificate)
                bank_certificate_file_obj = BankCertificateFile(temporary_folder, certificate)
                # Если индекс меньше 5 то возвращает False, иначе True. Если все False и True совпали - тест пройден.
                (self.assertFalse if count < 5 else self.assertTrue)(bank_certificate_file_obj.is_valid)
        finally:
            #
            remove_dir(temporary_folder)
