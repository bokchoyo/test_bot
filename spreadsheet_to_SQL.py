import csv
import asyncio

from prettytable import PrettyTable

from car_database import CarDatabase  # Replace 'your_module' with the actual module where CarDatabase is defined


async def import_data_from_csv(csv_file_path):
    # Initialize the CarDatabase class
    car_db = CarDatabase()

    # Create the database table if it doesn't exist
    await car_db.create_car_database()

    # Open the CSV file and extract column names
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # Assuming the first row contains column names
        columns = next(reader)

        # Loop through the remaining rows and insert data into the database
        for row in reader:
            # Create a dictionary with column names as keys and row values as values
            data_dict = {}
            for col, value in zip(columns, row):
                data_dict[col] = value

            print("Adding row to database:", data_dict)

            # Insert the row into the database
            await car_db.add_car(**data_dict)


def print_csv_table(csv_file_path):
    # Open the CSV file and create a PrettyTable instance
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        # Assuming the first row contains column names
        columns = next(reader)

        # Create PrettyTable with column names
        table = PrettyTable(columns)

        # Add rows to the table
        for row in reader:
            table.add_row(row)

    # Print the table
    print(table)


# Replace the file path with your CSV file
print_csv_table(r"C:\Users\bokch\Documents\Gearbox_CSV\Koenigsegg.csv")

asyncio.run(import_data_from_csv(r"C:\Users\bokch\Documents\Gearbox_CSV\Koenigsegg.csv"))
