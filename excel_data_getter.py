import openpyxl

class ExcelFile:
    """
    Класс для инкапсуляции взаимодействия с Excel-файлом
    """
    def __init__(self, filename):
        self.filename = filename
        self.workbook = None

    def get_value(self) -> dict:
        """
        Функция для получения точечно необходимой информации из Excel - файла
        """
        self.workbook = openpyxl.load_workbook(self.filename)
        sheet_parameters = self.workbook['Параметры']
        sheet_invest = self.workbook['Расчет инвест. затрат']
        sheet_chart_dl = self.workbook['Расчет графика ЛП']
        sheet_recoverable_cost = self.workbook['Возмещаемые затраты']
        data_dict: dict
        data_dict['ИТОГО проценты за финансирование за период поставки'] = sheet_invest['D31'].value
        data_dict['Размер аванса'] = sheet_invest['B6'].value
        data_dict['Дата аванса'] = sheet_invest['C6'].value

        ## TODO: возмещаемые затраты находятся по слову "Итого"
        # data_dict['Возмещаемые затраты'] = sheet_recoverable_cost['C8'].value


        ## TODO: цикл, который проходит по листу и суммирует до None
        data_dict['Стоимость ДЛ'] = sheet_chart_dl

        ## TODO: находить по тегу на отсрочку ДЛ
        data_dict['Отсрочка ДЛ'] = sheet_parameters['C35'].value


        return data_dict
    
    def close_wb(self):
        """
        Функция для закрытия Excel - файла
        """
        self.workbook.close()
