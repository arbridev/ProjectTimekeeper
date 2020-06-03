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

    def new_workbook(self, path):
        self.workbook = openpyxl.Workbook()
        self.filepath = path
        self.workbook.save(path)

    def open_workbook(self, path):
        self.workbook.close()
        self.workbook = openpyxl.load_workbook(filename = path)
        self.filepath = path

    def save_workbook(self):
        self.workbook.save(self.filepath)

    def close(self):
        self.workbook.close()

    ## input methods

    def input_text(self, text, cell):
        sheet = self.workbook.active
        sheet[cell] = text

    def input_number(self, stringNumber, cell):
        sheet = self.workbook.active
        sheet[cell].value = int(stringNumber.replace('.', ''))

    def input_date(self, date, cellCoordinate):
        sheet = self.workbook.active
        sheet[cellCoordinate].value = date

    def input_current_date(self, cell):
        self.input_date(datetime.datetime.now(), cell.coordinate)

    def input_scaffold(self):
        sheet = self.workbook.active
        sheet['A1'] = 'Id'
        sheet['B1'] = 'Start'
        sheet['C1'] = 'End'
        sheet['D1'] = 'Task'
        sheet['E1'] = 'Duration'

    ## helper methods

    def get_next_empty_cell_down(self, column="A"):
        sheet = self.workbook.active
        nextRow = 1
        for cell in sheet[column]:
            if cell.value is None:
                nextRow = cell.row
                break
            else:
                nextRow = cell.row + 1
        return sheet[column + str(nextRow)]

    def get_last_filled_cell(self, column="A"):
        sheet = self.workbook.active
        nextRow = 1
        for cell in sheet[column]:
            if cell.value is None:
                nextRow = cell.row - 1
                break
            else:
                nextRow = cell.row
        return sheet[column + str(nextRow)]

    def get_cell_above(self, cell):
        if cell.row - 1 > 0:
            return cell.offset(row = -1)
        else:
            return None

    def get_cell_below(self, cell):
        return cell.offset(row = 1)

    def get_cell_beside(self, cell, rightside=True):
        if rightside:
            return cell.offset(column = 1)
        else:
            if cell.column - 1 > 0:
                return cell.offset(column = -1)
            else:
                return None

    def adjust_column(self, column, width):
        sheet = self.workbook.active
        sheet.column_dimensions[column].width = width

    def adjust_row(self, row, height):
        sheet = self.workbook.active
        sheet.row_dimensions[row].height = height

    # def adjustCell(self, cell, horizontalAlignment=None, verticalAlignment=None):
    #     if horizontalAlignment != None or verticalAlignment != None:
    #         cell.alignment = Alignment(horizontal=horizontalAlignment, vertical=horizontalAlignment)

    def insert_row(self, atRow):
        sheet = self.workbook.active
        sheet.insert_rows(atRow)
    
    def merge_cells(self, range_string=None, start_row=None, start_column=None, end_row=None, end_column=None):
        sheet = self.workbook.active
        sheet.merge_cells(range_string=range_string, start_row=start_row, start_column=start_column, end_row=end_row, end_column=end_column)
        