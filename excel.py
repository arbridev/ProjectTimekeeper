## external imports

import openpyxl
import os
import string
import datetime
# from openpyxl.styles import Alignment

class ExcelHandler():

    workbook = openpyxl.Workbook()
    filepath = ''

    __alphabet = string.ascii_uppercase

    # def __init__(self):
    #     print('init excel handler')

    ## file methods

    def newWorkbook(self, path):
        self.workbook = openpyxl.Workbook()
        self.filepath = path
        self.workbook.save(path)

    def openWorkbook(self, path):
        self.workbook.close()
        self.workbook = openpyxl.load_workbook(filename = path)
        self.filepath = path

    def saveWorkbook(self):
        self.workbook.save(self.filepath)

    def close(self):
        self.workbook.close()

    ## input methods

    def inputText(self, text, cell):
        sheet = self.workbook.active
        sheet[cell] = text
        self.workbook.save(self.filepath)

    def inputNumber(self, stringNumber, cell):
        sheet = self.workbook.active
        sheet[cell].value = int(stringNumber.replace('.', ''))
        self.workbook.save(self.filepath)

    def inputDatetime(self, date_time, cell):
        sheet = self.workbook.active
        sheet[cell].value = datetime.datetime.strptime(date_time, "%d/%m/%Y")
        self.workbook.save(self.filepath)

    def inputCurrentDatetime(self, cell):
        self.inputDatetime(datetime.datetime.now(), cell)

    def inputScaffold(self):
        sheet = self.workbook.active
        sheet['A1'] = 'Id'
        sheet['B1'] = 'Start'
        sheet['C1'] = 'End'
        sheet['D1'] = 'Task'
        sheet['E1'] = 'Interval'
        self.workbook.save(self.filepath)

    ## helper methods

    def getNextEmptyCellDown(self, column="A"):
        sheet = self.workbook.active
        nextRow = 1
        for cell in sheet[column]:
            if cell.value is None:
                nextRow = cell.row
                break
            else:
                nextRow = cell.row + 1
        return sheet[column + str(nextRow)]

    def getLastFillCellDown(self, column="A"):
        sheet = self.workbook.active
        nextRow = 1
        for cell in sheet[column]:
            if cell.value is None:
                nextRow = cell.row
                break
            else:
                nextRow = cell.row
        return sheet[column + str(nextRow)]

    def getCellAbove(self, cell):
        if cell.row - 1 > 0:
            return cell.offset(row = -1)
        else:
            return None

    def getCellBellow(self, cell):
        return cell.offset(column = 1)

    def getCellBeside(self, cell, rightside=True):
        if rightside:
            return cell.offset(column = 1)
        else:
            if cell.column - 1 > 0:
                return cell.offset(column = -1)
            else:
                return None

    def adjustColumn(self, column, width):
        sheet = self.workbook.active
        sheet.column_dimensions[column].width = width

    def adjustRow(self, row, height):
        sheet = self.workbook.active
        sheet.row_dimensions[row].height = height

    # def adjustCell(self, cell, horizontalAlignment=None, verticalAlignment=None):
    #     if horizontalAlignment != None or verticalAlignment != None:
    #         cell.alignment = Alignment(horizontal=horizontalAlignment, vertical=horizontalAlignment)
        