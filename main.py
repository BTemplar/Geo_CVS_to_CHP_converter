import csv


def convert_csv_to_chp(input_file, output_file, delimiter=';'):
    """
    This function processes a CSV file and writes the processed data to another CSV file.

    :param input_file: The path to the input CSV file.
    :param output_file: The path to the output CHP file.
    :param delimiter: The delimiter used in the CSV files.
    :return: None
    """
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter=delimiter)

        with open(output_file, mode='w', encoding='utf-8') as outfile:
            for row in reader:
                name = row['Name']
                latitude = row['Latitude']
                longitude = row['Longitude']

                outfile.write(f'Name="{name}"\n')
                outfile.write('Add1=0,0\n')
                outfile.write('Add2=0,0\n')
                outfile.write('Add3=0,0\n')
                outfile.write(f'PExt=({latitude} {longitude} R10)\n')
                outfile.write('Prms=0,0\n')

input_csv = 'input.csv'
output_chp = 'output.chp'
convert_csv_to_chp(input_csv, output_chp)
