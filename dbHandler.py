import csv
import os

CSV_FILE = "criminal.csv"

def insertData(data, filename=CSV_FILE):
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write header if file is new
        if not file_exists:
            writer.writerow([
                "Name", "Father's Name", "Mother's Name", "Gender",
                "DOB(yyyy-mm-dd)", "Blood Group", "Identification Mark",
                "Nationality", "Religion", "Crimes Done", "Image"
            ])

        # Write data row
        writer.writerow([
            data.get("Name", "Not Available"),
            data.get("Father's Name", "Not Available"),
            data.get("Mother's Name", "Not Available"),
            data.get("Gender", "Not Available"),
            data.get("DOB(yyyy-mm-dd)", "Not Available"),
            data.get("Blood Group", "Not Available"),
            data.get("Identification Mark", "Not Available"),
            data.get("Nationality", "Not Available"),
            data.get("Religion", "Not Available"),
            data.get("Crimes Done", "Not Available"),
            data.get("Image", "Not Available")  
        ])

    print(f"✅ Data saved to {filename}")
    return True


def retrieveData(name, filename=CSV_FILE):
    if not os.path.exists(filename):
        print("❌ No criminal.csv file found yet.")
        return None

    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Name"].strip().lower() == name.strip().lower():
                print(f"✅ Found record for {name}: {row}")
                return row

    print(f"❌ No record found for {name}")
    return None
