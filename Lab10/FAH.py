import psycopg2
import csv

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="Nurdaulet05"
)

cur = conn.cursor()

# Create phone_book table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS phone_book (
        id SERIAL PRIMARY KEY,
        "PersonName" VARCHAR(255),
        "PhoneNumber" VARCHAR(20)
    );
''')
conn.commit()

# Insert data from console
def inputData():
    name = input("Enter your name: ").strip()
    number = input("Enter your phone number: ").strip()
    cur.execute(
        'INSERT INTO phone_book("PersonName", "PhoneNumber") VALUES (%s, %s);',
        (name, number)
    )

# Import data from CSV file
def importFromCSV():
    try:
        with open("info.csv", 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) < 2:
                    continue
                personName, phoneNumber = row
                cur.execute(
                    'INSERT INTO phone_book("PersonName", "PhoneNumber") VALUES (%s, %s);',
                    (personName.strip(), phoneNumber.strip())
                )
    except FileNotFoundError:
        print("CSV file not found.")

# Update contact by name
def update_contact():
    name = input("Enter the name of the person you want to update: ").strip()
    print("What would you like to update?")
    print("1. Name\n2. Phone\n3. Both")
    choice = input("Choose an option: ")

    if choice == '1':
        newName = input("Enter new name: ").strip()
        cur.execute(
            'UPDATE phone_book SET "PersonName" = %s WHERE "PersonName" = %s',
            (newName, name)
        )
    elif choice == '2':
        newPhone = input("Enter new phone number: ").strip()
        cur.execute(
            'UPDATE phone_book SET "PhoneNumber" = %s WHERE "PersonName" = %s',
            (newPhone, name)
        )
    elif choice == '3':
        newName = input("Enter new name: ").strip()
        newPhone = input("Enter new phone number: ").strip()
        cur.execute(
            'UPDATE phone_book SET "PersonName" = %s, "PhoneNumber" = %s WHERE "PersonName" = %s',
            (newName, newPhone, name)
        )

# Query and save data to a text file
def queryData():
    cur.execute('SELECT "PersonName", "PhoneNumber" FROM phone_book')
    data = cur.fetchall()
    path = "queredData.txt"

    with open(path, "w", encoding='utf-8') as f:
        for name, number in data:
            f.write(f"Name: {name}\nNumber: {number}\n\n")

# Delete data by name
def deleteData():
    name = input("Enter the name to delete: ").strip()
    cur.execute('DELETE FROM phone_book WHERE "PersonName" = %s', (name,))

# Delete all data
def deleteAllData():
    cur.execute('DELETE FROM phone_book')

# Main loop
def main():
    done = False
    while not done:
        print("\nWhat do you want to do?")
        print("1. Input data from console")
        print("2. Upload from CSV file")
        print("3. Update existing contact")
        print("4. Query data to file")
        print("5. Delete by person name")
        print("6. Delete all data")
        print("7. Exit")

        choice = input("Enter number 1-7: ")
        if choice == '1':
            inputData()
        elif choice == '2':
            importFromCSV()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            queryData()
        elif choice == '5':
            deleteData()
        elif choice == '6':
            deleteAllData()
        elif choice == '7':
            done = True
        else:
            print("Invalid option.")
        conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()