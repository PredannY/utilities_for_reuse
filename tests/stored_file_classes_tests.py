import platform
import random
import unittest
import os
from classes.stored_file_classes import StoredFileContainer
from utils.file_utils import create_temp_dir, remove_dir


def create_new_file(temporary_dir: str, file_name: str):
    """
    Функция, предназначенная для создания нового файла
    :param str temporary_dir: путь до файла
    :param  str file_name: имя файла
    :return: any_file: файл
    """
    any_file_name = os.path.join(temporary_dir, file_name)
    any_file = open(any_file_name, mode='w')
    any_file.write('Some comment')
    return any_file


class TestStoredFileContainer(unittest.TestCase):
    """
    Unit test для тестирования компоненты get_unlocked_files
    """
    def test_block_files(self):
        if platform.system() == 'Linux':
            # Создать временную папку
            temporary_folder = create_temp_dir()
            blocked_files_list = []
            unblocked_files_list = []
            try:
                # Создать файлы
                for i in range(100):
                    is_file_blocked = random.choice([True, False])
                    new_file = create_new_file(temporary_folder, str(i))
                    # Если True - создать файл с блокировкой
                    if is_file_blocked:
                        blocked_files_list.append(new_file)
                    # Иначе создать файл без блокировки
                    else:
                        new_file.close()
                        unblocked_file = open(new_file.name, mode='r')
                        _contents = unblocked_file.read()
                        unblocked_files_list.append(unblocked_file)
                stored_file_container_obj = StoredFileContainer(temporary_folder)
                # Сравнить списки. Если количество элементов равно - тест пройден
                self.assertEqual(len(unblocked_files_list), len(stored_file_container_obj.get_unlocked_files()))
            finally:
                # Закрыть файлы без блокировки
                for any_unblocked_file in unblocked_files_list:
                    any_unblocked_file.close()
                # Закрыть файлы с блокировкой
                for any_blocked_file in blocked_files_list:
                    any_blocked_file.close()
                # Удалить папку
                remove_dir(temporary_folder)
