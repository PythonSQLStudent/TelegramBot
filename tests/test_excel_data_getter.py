import unittest
import openpyxl

from excel_data_getter import ExcelFile

file_path = "C:\\Users\\Admin\\Documents\\GitHub\\TelegramBot\\tests\\test.xlsx"

class ExcelFileTests(unittest.TestCase):

    def setUp(self):
        self.excel_file = ExcelFile(file_path)

    def test_init(self):
        self.assertEqual(self.excel_file.filename, file_path)
        self.assertIsNone(self.excel_file.workbook)

    def test_open(self):
        self.excel_file.open()
        self.assertIsInstance(self.excel_file.workbook, openpyxl.Workbook)

    def test_get_value(self):
        self.excel_file.open()
        value = self.excel_file.get_value('Sheet1', 'A1')
        self.assertEqual(value, 'Я чебурашка')
