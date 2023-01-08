import array
import pandas as pd


class ExportToData:
    def __init__(self):
        self.pandas = pd

    def export_to_excel(self, file_path, sheet_name, file):
        print("Exporting result to excel file.....")
        writer = self.pandas.ExcelWriter(file_path, engine='openpyxl')
        file.to_excel(writer, sheet_name=sheet_name)

        writer.save()
        print("Export complete.")

    def export_to_excel_with_many_sheets(self, file_path, files: array):
        print("Exporting result to excel file.....")
        writer = self.pandas.ExcelWriter(file_path, engine='openpyxl')

        for sheet_name, file in files:
            file.to_excel(writer, sheet_name=sheet_name)

        writer.save()
        print("Export complete.")
