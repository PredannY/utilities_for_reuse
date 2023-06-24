from classes.stored_file_classes import StoredFile, StoredFileContainer
import datetime
import typing


class BankCertificateFile(StoredFile):
    """
    Класс, предназанченный для хранения информации о сертификате. Родительский класс StoredFile.
    """
    bank_code: str
    snils: str
    end_date: datetime.datetime
    certificate_condition: str
    is_valid: bool
    pin: str  # может устанавливаться дополнительно

    def __init__(self, file_path: str, file_name: str):
        """
        Конструктор класса. При создании передаются хранимые атрибуты.
        return вызванного метода передается двум атрибутам.
        :param str file_path: путь файла, без имени файла.
        :param str file_name: имя файла с расширением.
        """
        super().__init__(file_path, file_name)
        self.is_valid, self.error_str = self.certificate_name_parse()

    def certificate_name_parse(self) -> (bool, str):
        """
        Метод, предназначенный для проверки имени файла на соответствие, а также
        передачи в атрибуты нужных параметров.
        :return: (bool, str): возврат True или False и строки с описанием
        """
        splited_file_name = self.file_name.split('.')
        if len(splited_file_name) == 4:
            self.bank_code = splited_file_name[0]
            self.snils = splited_file_name[1]
            if len(splited_file_name[2]) == 14:
                try:
                    self.end_date = datetime.datetime.strptime(splited_file_name[2], '%Y%m%d%H%M%S')
                except ValueError:
                    return False, f'Неверный формат даты'
            else:
                return False, f'Неверный формат даты'
            self.certificate_condition = splited_file_name[3]
            try:
                assert len(self.bank_code) == 4, f'Неверный код банка'
                assert len(self.snils) == 11, f'Неверный СНИЛС'
                assert self.certificate_condition in ('cer', 'del'), f'Файл не является сертификатом'
            except AssertionError as a:
                return False, str(a)
            return True, (
                ' Код банка: {}; СНИЛС: {}; Срок окончания сертификата: {}; Состояние сертификата: {}'.
                format(self.bank_code, self.snils, self.end_date, self.certificate_condition))
        else:
            return False, f'{self.file_name} - Имя файла не соответствует имени сертификата'


class BankCertificatesContainer(StoredFileContainer):
    """
    Класс, предназначенный для получения списка файлов из папки, а так же
    создания хранилища сертификатов. Родительский класс StoredFileContainer.
    """
    path_class: typing.Type[BankCertificateFile]
    path_class = BankCertificateFile

    def get_valid_certificates_list(self) -> list[BankCertificateFile]:
        """
        метод, предназначенный для создания хранилища сертификатов.
        :return: list[str] certificates_list: список сертификатов
        """
        certificates_list = []
        for certificate in self.files_list:
            if certificate.is_valid:
                certificates_list.append(certificate)
        return certificates_list

    def get_certificates_by_code(self, bank_code: str, valid_certificates: bool = True):
        """ Получить список сертификатов банка
        :param str bank_code: код банка
        :param bool valid_certificates: True если надо получить только валидные сертификаты
        """
        return [
            x for x in filter(
                lambda x: x.bank_code == bank_code,
                self.get_valid_certificates_list() if valid_certificates else self.files_list
            )
        ]
