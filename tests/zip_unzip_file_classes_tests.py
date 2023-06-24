from classes.zip_unzip_file_classes import ZipFile, UnZipFile
from utils.file_utils import create_temp_dir, remove_dir
import unittest
import os
from classes.stored_file_classes import StoredFile


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


def create_zip_folder(dir_to_zip_create: str) -> ZipFile:
    """
       Функция, предназначенная для создания временных фалов во временной папке и архива
       :param str dir_to_zip_create:
       :return: возвращает архив
    """
    uncreated_files_list = [
        'test__txt_file1.txt',
        'test_txt_file_2.txt',
        'test_txt_file_3.txt'
    ]
    stored_file_obj_list: list[StoredFile]
    stored_file_obj_list = []
    for unzipped_file in uncreated_files_list:
        create_new_file(dir_to_zip_create, unzipped_file)
        stored_file_obj_list.append(StoredFile(dir_to_zip_create, unzipped_file))
    return ZipFile(dir_to_zip_create, 'test_arch.zip', stored_file_obj_list)


class TestZipFile(unittest.TestCase):
    """
    Unit test для тестирования компоненты make_zip_files
    """
    def test_zip_archive_create(self):
        # Создаем временную папку
        temporary_folder = create_temp_dir()
        try:
            # Вызываем функцию для создания файлов и архива
            zip_file_obj = create_zip_folder(temporary_folder)
            false_bool, output_str = zip_file_obj.make_zip_files(False)
            # Проверяем, если False - тест пройден
            self.assertEqual(False, false_bool)
        finally:
            # Удаляем временную папку
            remove_dir(temporary_folder)


class TestUnZipFile(unittest.TestCase):
    """
    Unit test для тестирования компоненты make_zip_files
    """
    def test_zip_archive_unpack(self):
        # Создаем временную папку
        temporary_folder = create_temp_dir()
        zip_file_obj = create_zip_folder(temporary_folder)
        zip_file_obj.make_zip_files(True)
        try:
            # Вызываем функцию для создания файлов и архива
            unzip_file_obj = UnZipFile(temporary_folder, 'test_arch.zip', temporary_folder)
            false_bool, stored_file_list, output_str = unzip_file_obj.make_unzip_files(False)
            # Проверяем, если False - тест пройден
            self.assertEqual(False, false_bool)
        finally:
            # Удаляем временную папку
            remove_dir(temporary_folder)

    def test_zip_archive_badzip_error(self):
        # Создаем временную папку
        temporary_folder = create_temp_dir()
        create_zip_folder(temporary_folder)
        created_zip = os.path.join(temporary_folder, 'test_arch.zip')
        # Ломаем архив
        with open(created_zip, 'w') as converted_zip:
            converted_zip.write('[g[g[[]y]]y]nn[[g=')
        try:
            unzip_file_obj = UnZipFile(temporary_folder, 'test_arch.zip', temporary_folder)
            # Вызываем метод для разархивации и ожидаем, что он выдаст False,
            # пустой список и соообщение об ошибке
            true_bool, empty_list, error_str = unzip_file_obj.make_unzip_files(False)
            self.assertEqual(True, true_bool)
            self.assertEqual([], empty_list)
            self.assertIn('что-то не так. Возможно архив сломан! Ошибка', error_str)
        finally:
            # Удаляем временную папку
            remove_dir(temporary_folder)
