import csv

input_file = '/home/ubuntu/quokkazon/db/data/Category_1.csv'
output_file = '/home/ubuntu/quokkazon/db/data/Category.csv'

new_rows = []

with open(input_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        first_col, second_col, third_col = row[0], row[1], row[2]
        fourth_col_values = row[3].split(',')
        for fourth_value in fourth_col_values:
            new_row = [first_col, fourth_value]
            new_rows.append(new_row)
            
            new_row_without_fourth = [first_col, third_col]
            new_rows.append(new_row_without_fourth)

with open(output_file, 'w', newline='') as output_csv:
    writer = csv.writer(output_csv)
    writer.writerows(new_rows)

