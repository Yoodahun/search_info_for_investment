import array
import pandas as pd

class ExportToData:
    def __init__(self):
        self.pandas = pd

#TODO export to excel
    def export_to_excel_with_many_sheets(self, file_path, files: array):
        writer = self.pandas.ExcelWriter(file_path, engine='xlsxwriter')

        files[0].to_excel(writer, sheet_name="")





