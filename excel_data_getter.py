import openpyxl
import datetime as dt


class ExcelFile:
    """
    Класс для взаимодействия с Excel-файлом
    """
    def __init__(self, filename):
        self.filename = filename
        self.workbook = None

    def get_value(self) -> dict:
        """
        Функция для получения точечно необходимой информации из Excel - файла
        """
        self.workbook = openpyxl.load_workbook(self.filename, data_only=False)

        sheet_parameters = self.workbook['Параметры']
        sheet_invest = self.workbook['Расчет инвест. затрат']
        sheet_chart_dl = self.workbook['Расчет графика ЛП']
        sheet_recoverable_cost = self.workbook['Возмещаемые затраты']

        data_dict = dict()

        ## TODO: сделать даты оплаты оплаты поставщику, сделать сумму по столбцу, а не брать конкретное значение

        # data_dict['Проценты за финансирование'] = cell.value
        total_percent = 0
        for row in sheet_invest.iter_rows(min_row=4, max_row=30):
            cell = row[3]
            if cell.value is not None:
                total_percent += cell.value
        data_dict['Проценты за финансирование'] = total_percent

        data_dict['Размер аванса'] = sheet_invest['B6'].value

        ## TODO: сделать дату передачи
        data_dict['Дата аванса'] = sheet_invest['C6'].value

        total_cost = 0
        for row in sheet_recoverable_cost.iter_rows(min_row=3):
            cell = row[2]
            if cell.value is not None:
                total_cost += cell.value
        data_dict['Возмещаемые затраты'] = total_cost

        total_dl = 0
        for row in sheet_chart_dl.iter_rows(min_row=3):
            cell = row[13]
            if cell.value is not None:
                total_dl += cell.value
        data_dict['Стоимость ДЛ'] = -total_dl

        for row in sheet_parameters.iter_rows():
            cell = row[1]
            if cell.value == 'Отсрочка_ДЛ':
                data_dict['Отсрочка ДЛ'] = sheet_parameters.cell(row=cell.row, column=cell.column + 1).value
            elif cell.value == 'Срок_ДЛ_Мес':
                data_dict['Срок ДЛ'] = sheet_parameters.cell(row=cell.row, column=cell.column + 1).value


        return data_dict
    
    def close_wb(self):
        """
        Функция для закрытия Excel - файла
        """
        self.workbook.close()


filename = 'по факту 302425785.xlsx'
# abs_filename = os.path.abspath(filename)
ssss = ExcelFile(filename)
l = ssss.get_value()
print(l)
ssss.close_wb()
