import array
import pandas as pd


class ExportToData:
    def __init__(self):
        self.pandas = pd

    def export_to_excel(self, file_path, file):
        print("Exporting result to excel file.....")
        writer = self.pandas.ExcelWriter(file_path, engine='openpyxl')
        file.to_excel(writer, sheet_name="test")

        writer.save()


    # TODO export to excel
    def export_to_excel_with_many_sheets(self, file_path, files: array):
        print("Exporting result to excel file.....")
        writer = self.pandas.ExcelWriter(file_path, engine='openpyxl')

        files[0].to_excel(writer, sheet_name="저PBR_저PER")
        # files[1].to_excel(writer, sheet_name="KOSDAQ_저PER_저PBR")

        writer.save()
