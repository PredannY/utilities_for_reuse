import os
from classes.misc_classes import BlockedFilesDetector
import typing

from typing import List


class StoredFile:
    """
    Класс, предназначенный для хранения информации
    и статусе файла, включая данные о его блокировке.
    """

    def __init__(self, file_path: str, file_name: str):
        """
        Конструктор класса. При создании передаются хранимые атрибуты
        :param str file_path: путь файла, без имени файла
        :param str file_name: имя файла с расширением
        """
        self.file_path = file_path
        self.file_name = file_name
        self.is_valid, self.error_str = self.check_element_values()

    def check_element_values(self) -> (bool, str):
        """
        Метод проверки входных данных.
        :return: (bool, str): Возвращает True/False и строку с описанием.
        """
        try:
            assert len(self.file_name) > 0, 'Имя файла не может быть пустым'
            assert len(self.file_path) > 0, 'Директория файла не может быть пустой'
        except AssertionError as a:
            return False, str(a)
        return True, ''

    def __str__(self):
        """
        Строковое представление метода full_file_name
        :return: str: полный путь файла
        """
        return self.full_file_name

    @property
    def full_file_name(self):
        """
        Получить полный путь файла
        :return: str: объединение пути и имени файла
        """
        return os.path.join(self.file_path, self.file_name)


class StoredFileContainer:
    """
    Класс, предназначенный для получения списка файлов и определения
    готовности файлов для обработки(отсутствие блокировок на файле)
    """
    path_class: typing.Type[StoredFile]
    path_class = StoredFile

    def __init__(self, file_directory: str):
        """
        Класс конструктор. Заполняет полными директориями файлов
        список для последующего использования класса
        :param str file_directory: путь файла без имени файла
        """
        self.file_directory = file_directory
        self.files_list = []
        for files_instance in os.listdir(file_directory):
            self.files_list.append(self.path_class(file_directory, files_instance))

    def get_unlocked_files(self) -> List[StoredFile]:
        """
        Проверить блокирован ли файл и отобрать неблокированные файлы
        :return: list[StoredFile]: список незаблокированных файлов
        """
        unlocked_files_list = []
        block_files_det_obj = BlockedFilesDetector()
        for processed_stored_file_obj in self.files_list:
            if not block_files_det_obj.file_is_locked(processed_stored_file_obj.full_file_name):
                unlocked_files_list.append(processed_stored_file_obj)
        return unlocked_files_list
