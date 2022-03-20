import array
import pandas as pd


class ExportToData:
    def __init__(self):
        self.pandas = pd

    # TODO export to excel
    def export_to_excel_with_many_sheets(self, file_path, files: array):
        print("Exporting result to excel file.....")
        writer = self.pandas.ExcelWriter(file_path, engine='openpyxl')

        files[0].to_excel(writer, sheet_name="저PER_저PBR")

        writer.save()
