import csv


def sort_csv_file(file_path):
    # Create a dictionary to store CSV writers for each label
    writers = {}
    output_files = {}

    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        # Assuming the first row contains the column titles
        column_titles = next(csv_reader)

        # Read and sort the remaining rows
        for row in csv_reader:
            # Assuming the label is in the third column (index 2)
            label = row[2]

            # If we haven't encountered this label before, create a new CSV writer for it
            if label not in writers:
                output_file = open(f"{label}_log.csv", 'w', newline='')
                output_files[label] = output_file
                writers[label] = csv.writer(output_file)
                writers[label].writerow(column_titles)
            
            # Write the row to the appropriate CSV file
            writers[label].writerow(row)
    
    # Close all output files
    for output_file in output_files.values():
        output_file.close()


def main():
    # Use double backslashes or raw string to handle the backslashes in the file path
    file_path = "C:\\Users\\dorcohe1\\OneDrive - Intel Corporation\\Desktop\\Final_proj\\Logs\\LNL-M_WarmReset_log.csv"
    
    # Alternatively, you can use a raw string:
    # file_path = r"C:\Users\dorcohe1\OneDrive - Intel Corporation\Desktop\Final_proj\Logs\LNL-M_WarmReset_log.csv"
    
    sort_csv_file(file_path)


if __name__ == "__main__":
    main()  