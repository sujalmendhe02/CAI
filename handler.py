import csv
import os

CSV_FILE = "Criminal.csv"

def insertData(data, filename=CSV_FILE):
    """Insert a new criminal record into CSV file"""
    fields = ['Name', "Father's Name", "Gender", "DOB(yyyy-mm-dd)", "Crimes Done"]
    row = [
        data.get('Name', 'Not Available'),
        data.get("Father's Name", 'Not Available'),
        data.get('Gender', 'Not Available'),
        data.get('DOB(yyyy-mm-dd)', 'Not Available'),
        data.get('Crimes Done', 'Not Available')
    ]

    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write header only if file is new or empty
        if not file_exists or os.path.getsize(filename) == 0:
            writer.writerow(fields)
        writer.writerow(row)

    print(f"✅ Data inserted for {data.get('Name')}")
    return True


def retrieveData(name, filename=CSV_FILE):
    """Retrieve a criminal record by name"""
    if not os.path.exists(filename):
        print("❌ Criminal.csv file not found")
        return None

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Name"].strip().lower() == name.strip().lower():  # Case-insensitive match
                print(f"✅ Found record for {name}")
                return row

    print(f"❌ No record found for {name}")
    return None


def getAllCriminals(filename=CSV_FILE):
    """Get all criminal records from CSV file"""
    criminals = []
    if not os.path.exists(filename):
        return []

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            criminals.append(row)

    return criminals

# print(retrieveData('ss'))
