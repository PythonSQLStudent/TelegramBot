import openpyxl

class ExcelFile:
    """
    Класс для инкапсуляции взаимодействия с Excel-файлом
    """
    def __init__(self, filename):
        self.filename = filename
        self.workbook = None

    def open(self):
        """
        Функция для открытия Excel - файла
        """
        self.workbook = openpyxl.load_workbook(self.filename)

    def get_value(self, sheet_name, cell_address):
        """
        Функция для получения конкретного значения
        :parameter:
        :sheet_name: имя листа Excel - файла
        :cell_address: номер ячейки
        :return: значение внутри ячейки
        """
        sheet = self.workbook[sheet_name]
        return sheet[cell_address].value

    def close(self):
        """
        Функция для закрытия Excel - файла
        """
        self.workbook.close()