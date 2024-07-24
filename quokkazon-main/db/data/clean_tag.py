import csv

input_file = '/home/ubuntu/quokkazon/db/data/Tag_1.csv'
output_file = '/home/ubuntu/quokkazon/db/data/Tag.csv'

new_rows = []

with open(input_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
        first_col = row[0]
        second_col = row[1]
        third_col = row[2]
        fourth_col = row[3]
        tag1, tag2, tag3 = row[4].split(','), row[5].split(','), row[6].split(',')
        for i in range(len(tag1)):
            one = [first_col, tag1[i]]
            two = [first_col, tag2[i]]
            three = [first_col, tag3[i]]

            new_rows.append(one)
            new_rows.append(two)
            new_rows.append(three)
            
with open(output_file, 'w', newline='') as output_csv:
    writer = csv.writer(output_csv)
    writer.writerows(new_rows)
    
# Sample Tag csv data:    
# "4","Grass bundle","food","","food","natural","ingredient","2018-10-01 13:12:58","2018-10-01 13:12:58"
# "5","Stick bundle","tool","","tool","outdoor","equipment","2018-10-01 13:12:58","2018-10-01 13:12:58"