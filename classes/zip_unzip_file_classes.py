import zipfile
import os
from classes.stored_file_classes import StoredFile
import logging


def error_message_for_zipfile(message_value: str) -> (bool, str):
    """
    Функция для создания return.
    :param str message_value: строка с сообщением
    :return (bool, str): возвращает True и строку с сообщением
    """
    logging.error(message_value)
    return True, message_value


class ZipFile:
    """
    Компонента предназначенная для архивации файлов в архив
    """

    def __init__(self, archive_path: str, archive_name: str, files_to_zip: list[StoredFile]):
        """
        Класс конструктор. При создании передаются хранимые атрибуты.
        :param str archive_path: путь, по которому будет создан архив
        :param str archive_name: имя архива
        :param list[StoredFile] files_to_zip: список передаваемых экземпляров класса StoredFile
        """
        self.archive_path = archive_path
        self.archive_name = archive_name
        self.files_to_zip = files_to_zip

    def make_zip_files(self, delete_base_file: bool) -> (bool, str):
        """
        Метод, который создает архив из переданных в конструкторе файлов
        и, в зависимости от True/False, удаляет или оставляет базовые файлы.
        :param bool delete_base_file: передает True или False.
        Если True - удаляет базовый файл, False - пропускает удаление.
        :return: (bool, str): возврат True или False и лога с описанием.
        """
        archive_full_path = os.path.join(self.archive_path, self.archive_name)
        try:
            my_zip = zipfile.ZipFile(archive_full_path, mode='w', compression=zipfile.ZIP_DEFLATED)
            if not os.path.isfile(archive_full_path):
                return error_message_for_zipfile(f'Архив {self.archive_name} не был найден!')
            for unzipped_file in self.files_to_zip:
                unzipped_file_path = unzipped_file.full_file_name
                try:
                    my_zip.write(unzipped_file_path, unzipped_file.file_name)
                    logging.info(f'Файл {unzipped_file.file_name} был успешно добавлен в архив {self.archive_name}')
                except FileNotFoundError as fnfe:
                    my_zip.close()
                    os.remove(archive_full_path)
                    return error_message_for_zipfile(f'Файла {unzipped_file.file_name} не найдено по пути '
                                                     f'{unzipped_file.file_path}! Ошибка {fnfe}')
            my_zip.close()
            if len(my_zip.infolist()) < 1:
                os.remove(archive_full_path)
                return error_message_for_zipfile(f'Архив {archive_full_path} пуст!')
        except PermissionError as pe:
            return error_message_for_zipfile(f'Не хватает прав доступа для записи файлов в архив {self.archive_name}! '
                                             f'Ошибка {pe}')
        created_archive_message = f'{archive_full_path} - Архив по пути {self.archive_path} был успешно создан'
        if delete_base_file:
            message = f'Все исходные файлы были успешно удалены.'
            for already_zipped_file in self.files_to_zip:
                file_to_delete = already_zipped_file.full_file_name
                try:
                    os.remove(file_to_delete)
                except OSError as er:
                    return error_message_for_zipfile(
                        f'Удаление исходного файла {file_to_delete} не было завершено успешно! Ошибка {er}')
        else:
            message = f'Исходные файлы были сохранены'
        good_message = '. '.join([created_archive_message, message])
        logging.info(good_message)
        return False, good_message


def error_message_for_unzipfile(message_value: str, files_list) -> (bool, list[StoredFile], str):
    """
    Функция для создания return.
    :param str message_value: строка с сообщением
    :param list[StoredFile] files_list: список объектов класса StoredFile
    :return: (bool, list[StoredFile], str): возвращает True, список объектов класса, и строку с сообщением
    """
    logging.error(message_value)
    return True, files_list, message_value


class UnZipFile:
    """
    Компонента, предназначенная для разархивации файлов из архива
    """

    def __init__(self, archive_path: str, archive_name: str, path_to_unzip: str):
        """
        Класс конструктор. При создании передаются хранимые атрибуты.
        :param str archive_path: путь до архива
        :param str archive_name: имя архива
        :param str path_to_unzip: путь, в который надо будет распаковать файлы из архива
        """
        self.archive_path = archive_path
        self.archive_name = archive_name
        self.path_to_unzip = path_to_unzip

    def make_unzip_files(self, delete_archive: bool) -> (bool, list[StoredFile], str):
        """
        Метод, который разархивировывает файлы из архива в указанную директорию,
        и в зависимости от True/False удаляет или не удаляет архив.
        :param bool delete_archive: передает True/False.
        Если True - удаляет архив, False - оставляет архив.
        :return: (bool, list[StoreFile], str) - возвращает True/False, список объектов класса и строку
        """
        unzipped_files_list = []
        archive_full_path = os.path.join(self.archive_path, self.archive_name)
        if not os.path.isfile(archive_full_path):
            return error_message_for_unzipfile(f'Архив {archive_full_path} не найден!', unzipped_files_list)
        if not os.path.isdir(self.path_to_unzip):
            return error_message_for_unzipfile(f'Папка {self.path_to_unzip} не найдена!', unzipped_files_list)
        try:
            with zipfile.ZipFile(archive_full_path, 'r') as zip_file:
                for zipped_file in zip_file.infolist():
                    try:
                        zip_file.extract(zipped_file.filename, self.path_to_unzip)
                        unzipped_files_list.append(StoredFile(self.path_to_unzip,
                                                              zipped_file.filename))
                    except zipfile.BadZipFile as bzf:
                        for unzipped_file in unzipped_files_list:
                            os.remove(unzipped_file.full_file_name)
                        return error_message_for_unzipfile(f'Файл {zipped_file} в архиве {self.archive_name} сломан! '
                                                           f'Разархивация невозможна!'
                                                           f'\n Ошибка {bzf}!', unzipped_files_list)
                    except OSError as ose:
                        for unzipped_file in unzipped_files_list:
                            os.remove(unzipped_file.full_file_name)
                        return error_message_for_unzipfile(f'Произошла системная ошибка при разархивации '
                                                           f'файла {zipped_file} из архива {self.archive_name}!'
                                                           f' Ошибка {ose}!', unzipped_files_list)
        except zipfile.BadZipFile as bzf:
            return error_message_for_unzipfile(f'С архивом {self.archive_name} что-то не так. Возможно архив сломан! '
                                               f'Ошибка {bzf}', unzipped_files_list)
        archive_unpack_message = f'{self.archive_name} - Архив был успешно распакован по пути: {self.path_to_unzip}'
        if delete_archive:
            message = f'Удаление архива {self.archive_name} прошло успешно'
            try:
                os.remove(archive_full_path)
                logging.info(message)
            except OSError as er:
                return error_message_for_unzipfile(f'{archive_full_path} - Удаление архива не было завершено успешно!'
                                                   f' Ошибка {er}', unzipped_files_list)
        else:
            message = f'Архив {self.archive_name} был сохранён'
        output_message = '. '.join([archive_unpack_message, message])
        logging.info(output_message)
        return False, unzipped_files_list, output_message
