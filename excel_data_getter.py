import openpyxl
import pandas as pd
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

        # получаем проценты за финансирование
        total_percent = 0
        for row in sheet_invest.iter_rows(min_row=4, max_row=30):
            cell = row[3]
            if cell.value is not None:
                total_percent += cell.value
        data_dict['Итого проценты за финансирование'] = total_percent

        ## даты оплаты оплаты поставщику, размер оплаты поставщику, проценты за финансирование
        for row in sheet_invest.iter_rows(min_row=9, max_row=14):
            cell = row[3]
            if cell.value is not None and cell.value != 0:
                data_dict[sheet_invest.cell(row = cell.row, column=cell.column - 3).value + ' сумма'] = sheet_invest.cell(row = cell.row, column=cell.column - 2).value
                data_dict[sheet_invest.cell(row = cell.row, column=cell.column - 3).value + ' дата'] = sheet_invest.cell(row = cell.row, column=cell.column - 1).value
                data_dict[sheet_invest.cell(row = cell.row, column=cell.column - 3).value + ' проценты'] = sheet_invest.cell(row = cell.row, column=cell.column).value

        # получаем размер аванс
        data_dict['Размер аванса'] = sheet_invest['B6'].value

        # поучаем дату аванса
        data_dict['Дата аванса'] = sheet_invest['C6'].value

        # получаем дату передачи
        data_dict['Дата передачи'] = sheet_invest['C3'].value

        # получаем дату первого периода
        data_dict['Дата первого периода'] = sheet_chart_dl['B5'].value

        # получаем проценты первого периода
        data_dict['Проценты первого периода'] = sheet_chart_dl['M5'].value

        # получаем сумму возмещаемых затрат
        total_cost = 0
        for row in sheet_recoverable_cost.iter_rows(min_row=3):
            cell = row[2]
            if cell.value is not None:
                total_cost += cell.value
        data_dict['Возмещаемые затраты'] = total_cost

        # получаем сумму ДЛ
        total_dl = 0
        for row in sheet_chart_dl.iter_rows(min_row=3):
            cell = row[13]
            if cell.value is not None:
                total_dl += cell.value
        data_dict['Сумма ДЛ'] = -total_dl

        # получаем сумму процентов за период лизинга
        total_percent = 0
        for row in sheet_chart_dl.iter_rows(min_row=3):
            cell = row[12]
            if cell.value is not None:
                total_percent += cell.value
        data_dict['Сумма процентов за период лизинга'] = total_percent

        # получаем сумму субсидии
        total_subs = 0
        for row in sheet_chart_dl.iter_rows(min_row=3):
            cell = row[14]
            if cell.value is not None:
                total_subs += cell.value
        data_dict['Сумма субсидии за лизинг'] = -total_subs

        # получаем данные с листа параметров: Итого_ДКП_С_НДС, Отсрочка ДЛ, Срок ДЛ в мес
        for row in sheet_parameters.iter_rows():
            cell = row[1]
            if cell.value == 'Отсрочка_ДЛ':
                data_dict['Отсрочка ДЛ'] = sheet_parameters.cell(row=cell.row, column=cell.column + 1).value
            elif cell.value == 'Срок_ДЛ_Мес':
                data_dict['Срок ДЛ'] = sheet_parameters.cell(row=cell.row, column=cell.column + 1).value
            elif cell.value == 'ИТОГО_ДКП_С_НДС':
                data_dict['ИТОГО_ДКП_С_НДС'] = sheet_parameters.cell(row=cell.row, column=cell.column + 1).value


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
df = pd.DataFrame.from_dict(l, orient="index")
df.to_excel("data.xlsx")