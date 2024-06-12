from datetime import datetime,timedelta
import csv
import os

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Check if the entered username and password are correct
    if username == "Hammad" and password == "1592":
        print("Login successful!")
        return True
    else:
        print("Invalid username or password. Try again.")
        return False

def change_password():
    new_password = input("Enter a new password: ")
    # In a real-world scenario, you would store the new password securely.
    print("Password changed successfully.")


BOOKS_CSV_FILE = 'library.csv'
ISSUED_BOOKS_CSV_FILE = 'issued_books.csv'


def add_book():
    print("Add a new Book Record")
    print("=====================")

    book_id = input('Enter book id: ')
    book_name = input('Enter book name: ')
    author_name = input('Enter author name: ')

    # Check if the book already exists in the library
    if not is_book_present(book_id):
        with open(BOOKS_CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([book_id, book_name, author_name])
        print("Book Record Saved")
    else:
        print("Book with the given ID already exists.")

    input("Press any key to continue..")

def is_book_present(book_id):
    with open(BOOKS_CSV_FILE, 'r', newline='\r\n') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == book_id:
                return True
    return False

def edit_book():
    print("Modify a Book Record")
    print("====================")
    book_id_to_modify = input('Enter book ID whose record you want to modify: ')

    if is_book_present(book_id_to_modify):
        with open(BOOKS_CSV_FILE, 'r', newline='') as f:
            with open('temp.csv', 'w', newline='\r\n') as f_temp:
                reader = csv.reader(f)
                writer = csv.writer(f_temp)

                for row in reader:
                    if row and row[0] == book_id_to_modify:
                        print("-------------------------------")
                        print("Book ID:", row[0])
                        print("Book Name:", row[1])
                        print("Author:", row[2])
                        print("-------------------------------")

                        choice = input("Do you want to modify this Book Record? (y/n): ")
                        if choice.lower() == 'y':
                            new_book_id = input('Enter new book ID: ')
                            new_book_name = input('Enter new book name: ')
                            new_author_name = input('Enter new author name: ')
                            updated_row = [new_book_id, new_book_name, new_author_name]
                            writer.writerow(updated_row)
                            print("Book Record Modified")
                        else:
                            writer.writerow(row)
                    else:
                        writer.writerow(row)

        os.remove(BOOKS_CSV_FILE)
        os.rename('temp.csv', BOOKS_CSV_FILE)
        print("Press any key to continue...")
        input()
    else:
        print("Book not found in the library.")
        input("Press any key to continue...")

def delete_book():
    print("Delete a Book Record")
    print("=====================")
    book_id_to_delete = input('Enter book ID whose record you want to delete: ')

    if is_book_present(book_id_to_delete):
        with open(BOOKS_CSV_FILE, 'r', newline='') as f:
            with open('temp.csv', 'w', newline='') as f_temp:
                reader = csv.reader(f)
                writer = csv.writer(f_temp)

                for row in reader:
                    if row and row[0] == book_id_to_delete:
                        print("-------------------------------")
                        print("Book ID:", row[0])
                        print("Book Name:", row[1])
                        print("Author:", row[2])
                        print("-------------------------------")

                        choice = input("Do you want to delete this Book Record? (y/n): ")
                        if choice.lower() == 'n':
                            writer.writerow(row)
                        else:
                            print("Book Record Deleted")
                    else:
                        writer.writerow(row)

        os.remove(BOOKS_CSV_FILE)
        os.rename('temp.csv', BOOKS_CSV_FILE)
        print("Press any key to continue...")
        input()
    else:
        print("Book not found in the library.")
        input("Press any key to continue...")

def search_book():
    print("Search a Book Record")
    print("=====================")
    book_id_to_search = input('Enter book ID you want to search: ')

    if is_book_present(book_id_to_search):
        with open(BOOKS_CSV_FILE, 'r', newline='') as f:
            reader = csv.reader(f)

            for row in reader:
                if row and row[0] == book_id_to_search:
                    print("-------------------------------")
                    print("Book ID:", row[0])
                    print("Book Name:", row[1])
                    print("Author:", row[2])
                    print("-------------------------------")

        print("Press any key to continue...")
        input()
    else:
        print("Book not found in the library.")
        input("Press any key to continue...")

def show_all_books():
    print("List of All Books")
    print("=================")

    with open(BOOKS_CSV_FILE, 'r', newline='') as f:
        reader = csv.reader(f)

        for row in reader:
            if row:
                print("-------------------------------")
                print("Book ID:", row[0])
                print("Book Name:", row[1])
                print("Author:", row[2])

    print("-------------------------------")
    input("Press any key to continue...")


def issueBook():
    print("Issue a Book")
    print("=====================")
    book_id = input("Enter book id to issue: ")

    with open('library.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        library_data = list(reader)

    issued_book = None
    for book in library_data:
        if book[0] == book_id:
            issued_book = book
            library_data.remove(book)
            break

    if issued_book:
        with open('issued_books.csv', 'a', newline='') as f_issued:
            writer = csv.writer(f_issued)
            issued_book.append(get_due_date())  # Add due date to the issued book record
            writer.writerow(issued_book)
        with open('library.csv', 'w', newline='\r\n') as f_library:
            writer = csv.writer(f_library)
            writer.writerows(library_data)
        print("Book issued successfully!")
    else:
        print("Book not found in the library.")

    input("Press any key to continue..")

def return_issued_book():
    print("Return Issued Book")
    print("=====================")
    book_id_to_return = input("Enter book ID to return: ")

    with open(ISSUED_BOOKS_CSV_FILE, 'r', newline='') as f_issued:
        issued_books_data = list(csv.reader(f_issued))

    returned_book = next((book for book in issued_books_data if book[0] == book_id_to_return), None)

    if returned_book:
        fine = max(0, (datetime.now() - datetime.strptime(returned_book[-1], '%Y-%m-%d')).days) * 5
        print(f"Book returned successfully! Fine: ${fine}")

        issued_books_data.remove(returned_book)

        with open(ISSUED_BOOKS_CSV_FILE, 'w', newline='\r\n') as f_issued:
            csv.writer(f_issued).writerows(issued_books_data)

        with open(BOOKS_CSV_FILE, 'a', newline='') as f_library:
            csv.writer(f_library).writerow(returned_book[:-1])  # Remove the due date before returning to the library
    else:
        print("Book not found in the issued books records.")

    input("Press any key to continue...")

def calculate_fine(returned_book):
    due_date = datetime.strptime(returned_book[-1], '%Y-%m-%d')
    days_delayed = max(0, (datetime.now() - due_date).days)
    return days_delayed * 5

def get_due_date():
    return (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    
def dashboard():
    while True:
        print("\n|--------------------------|")
        print("| Library Management System |")
        print("| ------------------------- |")
        print(datetime.now())
        print("\n########################")
        print("        Dashboard")
        print("########################")
        print("1. Add a new Book Record")
        print("2. Edit Existing Book Record")
        print("3. Delete Existing Book Record")
        print("4. Search a Book")
        print("5. Show all Books")
        print("6. Issue Book")
        print("7. Return Issued Book")
        print("8. Log out")
        print("-------------------------------")

        choice = input('Enter your choice: ')

        if choice == '1':
            add_book()
        elif choice == '2':
            edit_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            search_book()
        elif choice == '5':
            show_all_books()
        elif choice == '6':
            issueBook()
        elif choice == '7':
            return_issued_book()
        elif choice == '8':
            print("You are logged out.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")

    
def admin_panel():
    print("Admin Panel")
    print("1. Login")
    print("2. Change Password")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        if login():
            # If login is successful, call the dashboard function immediately
            dashboard()
            return True 
            # Other admin tasks can be performed here if needed

    elif choice == "2":
        change_password()

    elif choice == "3":
        print("Existing admin panel.")
        exit()

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        return False 

# Main loop for the admin panel
while True:
    admin_panel()
