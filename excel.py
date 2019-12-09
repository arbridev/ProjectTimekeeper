## external imports
import openpyxl
import os
import string

class ExcelHandler():

    workbook = ''
    filepath = ''

    __alphabet = string.ascii_uppercase

    def __init__(self):
        print('init excel handler')

    def newWorkbook(self, path):
        self.workbook = openpyxl.Workbook()
        self.filepath = path
        self.workbook.save(path)

    def openWorkbook(self, path):
        self.workbook = openpyxl.load_workbook(filename = path)
        self.filepath = path

    def inputText(self, text, cell):
        sheet = self.workbook.active
        sheet[cell] = text
        self.workbook.save(self.filepath)

    def inputNumber(self, number, cell):
        sheet = self.workbook.active
        sheet[cell].value = int(number.replace('.', ''))
        self.workbook.save(self.filepath)

    