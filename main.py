import csv
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import QLocale


def convert_csv_to_chp(input_csv, output_chp, radius=10):
    """
    This function converts a CSV file to a CHP (Custom Header Protocol) file.

    :param input_csv: Path to the input CSV file.
    :param output_chp: Path to the output CHP file.
    :param radius: Radius value to be used in the PExt line. Defaults to 10.
    :return: The number of rows converted.
    """
    input_file = input_csv
    output_file = output_chp
    count_converted_rows= 0

    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter=',')

        with open(output_file, mode='w', encoding='utf-8') as outfile:
            for row in reader:
                count_converted_rows += 1
                name = row['Name']
                latitude = row['Latitude']
                longitude = row['Longitude']

                outfile.write(f'Name="{name}"\n')
                outfile.write('Add1=0,0\n')
                outfile.write('Add2=0,0\n')
                outfile.write('Add3=0,0\n')
                outfile.write(f'PExt=({latitude} {longitude} R{radius})\n')
                outfile.write('Prms=0,0\n')

        return count_converted_rows

class CSVtoCHPConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.setWindowTitle('CSV to CHP Converter')

    def initUI(self):
        layout = QVBoxLayout()
        self.resize(300, 400)  # Width and height of the original window

        # Determining the system language
        locale = QLocale.system()
        language = locale.language()

        if language == QLocale.English:
            label_input_csv = 'Input CSV file:'
            label_output_chp = 'Output CHP file:'
            convert_button_text = 'Convert'
            info_button_text = 'Information'
            browse_button_text = 'Browse'
        elif language == QLocale.Russian:
            label_input_csv = 'Входной файл CSV:'
            label_output_chp = 'Выходной файл CHP:'
            convert_button_text = 'Конвертировать'
            info_button_text = 'Информация'
            browse_button_text = 'Обзор'
        else:
            label_input_csv = 'Input CSV file:'
            label_output_chp = 'Output CHP file:'
            convert_button_text = 'Convert'
            info_button_text = 'Information'
            browse_button_text = 'Browse'

        self.label_input_csv = QLabel(label_input_csv)
        self.input_csv_line_edit = QLineEdit()
        self.browse_input_button = QPushButton(browse_button_text)
        self.browse_input_button.clicked.connect(self.open_input_file_dialog)

        self.label_output_chp = QLabel(label_output_chp)
        self.output_chp_line_edit = QLineEdit()
        self.browse_output_button = QPushButton(browse_button_text)
        self.browse_output_button.clicked.connect(self.open_output_file_dialog)

        convert_button = QPushButton(convert_button_text)
        convert_button.clicked.connect(self.convert)

        info_button = QPushButton(info_button_text)
        info_button.clicked.connect(self.show_info)

        layout.addWidget(self.label_input_csv)
        layout.addWidget(self.input_csv_line_edit)
        layout.addWidget(self.browse_input_button)
        layout.addWidget(self.label_output_chp)
        layout.addWidget(self.output_chp_line_edit)
        layout.addWidget(self.browse_output_button)
        layout.addWidget(convert_button)
        layout.addWidget(info_button)

        self.setLayout(layout)

    def open_input_file_dialog(self):

        locale = QLocale.system()
        language = locale.language()

        if language == QLocale.English:
            open_input_head_text = 'Open input CSV file:'
        elif language == QLocale.Russian:
            open_input_head_text = 'Открыть входной файл CSV:'
        else:
            open_input_head_text = 'Open input CSV file:'

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, open_input_head_text, "",
                                                   "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.input_csv_line_edit.setText(file_path)

    def open_output_file_dialog(self):

        locale = QLocale.system()
        language = locale.language()

        if language == QLocale.English:
            open_output_head_text = 'Create output CHP file:'
        elif language == QLocale.Russian:
            open_output_head_text = 'Создать выходной файл CHP:'
        else:
            open_output_head_text = 'Create output CHP file:'

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, open_output_head_text, "",
                                                   "CHP Files (*.chp);;All Files (*)", options=options)
        if file_path:
            self.output_chp_line_edit.setText(file_path)

    def convert(self):
        input_csv = self.input_csv_line_edit.text()
        output_chp = self.output_chp_line_edit.text()

        locale = QLocale.system()
        language = locale.language()

        if language == QLocale.English:
            error_head_text = 'Error:'
            error_message = 'Please specify both input and output files.'
        elif language == QLocale.Russian:
            error_head_text = 'Ошибка:'
            error_message = 'Пожалуйста, укажите входной и выходной файлы.'
        else:
            error_head_text = 'Error:'
            error_message = 'Please specify both input and output files.'

        if not input_csv or not output_chp:
            QMessageBox.warning(self, error_head_text, error_message)
            return

        try:

            # Calling the conversion function
            count_converted_rows = convert_csv_to_chp(input_csv, output_chp)
            if language == QLocale.English:
                success_head_text = 'Success:'
                success_text = f'Successfully converted {count_converted_rows} geopoints.'
            elif language == QLocale.Russian:
                success_head_text = 'Успешно:'
                success_text = f'Успешно конвертировано {count_converted_rows} геоточек'
            else:
                success_head_text = 'Success:'
                success_text = f'Successfully converted {count_converted_rows} geopoints.'

            # If the conversion is successful
            QMessageBox.information(self, success_head_text, success_text)

        except Exception as e:
            # If an error occurs
            QMessageBox.critical(self, error_head_text, str(e))

    def show_info(self):
        locale = QLocale.system()
        language = locale.language()

        if language == QLocale.English:
            info_text = """
            CSV to CHP Converter v1.0
            Author: Oleg Rud
            Description: This program converts CSV geopoint files to CHP format for AutoGraph software. 
            The ',' delimiter is used for CSV processing.
            """
        elif language == QLocale.Russian:
            info_text = """
CSV to CHP Converter v1.0
Автор: Олег Рудь
Описание: Эта программа конвертирует файлы 
с геоточками CSV в формат CHP для программного 
обеспечения AutoGraph. 
Для обработки CSV используется разделитель ','.
"""
        else:
            info_text = """
            CSV to CHP Converter v1.0
            Author: Oleg Rud
            Description: This program converts CSV geopoint files to CHP format for AutoGraph software. 
            The ',' delimiter is used for CSV processing.
            """
        QMessageBox.about(self, 'Information', info_text)


if __name__ == '__main__':
    app = QApplication([])
    converter = CSVtoCHPConverter()
    converter.show()
    app.exec_()