import csv
import re
from plantuml import PlantUML


def extract_process_names_from_log(csv_file_path):
    # Set to store unique data extracted from column 4 (assuming 0-based indexing)
    unique_data_set = set()

    # Regular expression pattern to match text within square brackets at the beginning of the string
    pattern = re.compile(r'^\[[^\]]*\]')

    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            # Assuming that the CSV file has at least 4 columns
            for row in csv_reader:
                if len(row) >= 4:
                    column_3_data = row[3]  # Assuming column 4 is at index 3 (0-based indexing)

                    # Extract text within square brackets at the beginning using regular expression
                    match = re.match(pattern, column_3_data)

                    # Check if there is a match and it doesn't start with "TS", then add it to the set
                    if match:
                        content_within_brackets = match.group(0)[1:-1]  # Remove the brackets
                        if not content_within_brackets.startswith('TS '):
                            unique_data_set.add(content_within_brackets)

    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return list(unique_data_set)


# def sort_csv_file(file_path):
#     # Create a dictionary to store CSV writers for each label
#     writers = {}
#     output_files = {}

#     with open(file_path, 'r') as csvfile:
#         csv_reader = csv.reader(csvfile)
        
#         # Assuming the first row contains the column titles
#         column_titles = next(csv_reader)

#         # Read and sort the remaining rows
#         for row in csv_reader:
#             # Assuming the label is in the third column (index 2)
#             label = row[2]

#             # If we haven't encountered this label before, create a new CSV writer for it
#             if label not in writers:
#                 output_file = open(f"{label}_log.csv", 'w', newline='')
#                 output_files[label] = output_file
#                 writers[label] = csv.writer(output_file)
#                 writers[label].writerow(column_titles)
            
#             # Write the row to the appropriate CSV file
#             writers[label].writerow(row)
    
#     # Close all output files
#     for output_file in output_files.values():
#         output_file.close()

def create_sequence_diagram():
    plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
    plantuml.processes_file(filename='sample.txt', outfile='sequence_diagram.png')


def main():
    csv_file_path = "Logs\\LNL-M_WarmReset_log.csv"

    process_names = extract_process_names_from_log(csv_file_path)
    # print(process_names)

    example = 'Python->CSME: Start\n'
    example += 'activate CSME\n'
    example += 'CSME->OSSE: Authentication Request\n'
    example += 'activate OSSE\n'
    example += 'OSSE->ESE: Authentication Request\n'
    example += 'activate ESE\n'
    example += 'ESE->OSSE: Authentication Response\n'
    example += 'deactivate ESE\n'
    # example += 'note right of OSSE: OSSE thinks about it\n'
    example += 'OSSE->CSME: Authentication Response\n'
    example += 'deactivate OSSE\n'
    example += 'CSME->BIOS: run\n'
    example += 'activate BIOS\n'
    example += 'BIOS->CSME\n'
    example += 'deactivate BIOS\n'
    example += 'CSME->Python: End\n'
    example += 'deactivate CSME\n'
    try:
        with open('sample.txt', 'w') as sequence_diagram_file:
            sequence_diagram_file.write(example)
    except FileNotFoundError:
        print("The 'docs' directory does not exist")

    create_sequence_diagram()


if __name__ == "__main__":
    main()  