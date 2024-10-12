import mysql.connector

# Function to execute schema
def execute_schema():
    try:
        # Step 1: Connect to MySQL server (without specifying the database)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port="3306"
        )
        cursor = conn.cursor()
        print("Connected to MySQL server successfully.")
        
        # Step 2: Read and execute the schema file
        with open('sql.sql', 'r') as schema_file:
            schema = schema_file.read()

        # Execute the SQL schema commands
        for statement in schema.split(';'):  # Split by semicolon to handle multiple SQL statements
            if statement.strip():  # Execute non-empty statements
                cursor.execute(statement)
        
        conn.commit()  # Commit changes to the database
        print("Schema executed successfully.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()  # Rollback if there was any error
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed.")

# Function to create a new student account
def create_student_account():
    name = input("Enter your full name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    password = input("Enter your password: ")
    
    try:
        query = "INSERT INTO Students (name, email, phone, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, phone, password))
        conn.commit()
        print("Student account created successfully!")
        student_menu()  # Direct to student menu after successful account creation
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to create a new librarian account
def create_librarian_account():
    name = input("Enter your full name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    password = input("Enter your password: ")
    
    try:
        query = "INSERT INTO Librarian (name, email, phone, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, phone, password))
        conn.commit()
        print("Librarian account created successfully!")
        librarian_menu()  # Direct to librarian menu after successful account creation
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to log in for both students and librarians
def login(role):
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    
    try:
        if role == 'student':
            query = "SELECT * FROM Students WHERE email = %s AND password = %s"
        else:
            query = "SELECT * FROM Librarian WHERE email = %s AND password = %s"
        
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        
        if user:
            print(f"Login successful! Welcome {user[1]} ({role.capitalize()})")
            if role == 'student':
                student_menu()
            else:
                librarian_menu()
        else:
            print("Invalid email or password. Please try again.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Student Menu
def student_menu():
    while True:
        print("\nStudent Menu:")
        print("1. Get Loan")
        print("2. View Loans")
        print("3. View Books")
        print("4. Logout")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            get_loan()
        elif choice == '2':
            view_loans()
        elif choice == '3':
            view_books()
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

# Updated librarian menu to include loan requests management
def librarian_menu():
    while True:
        print("\nLibrarian Menu:")
        print("1. Add Book")
        print("2. View Books")
        print("3. View Loans")
        print("4. View Students")
        print("5. Update Book Details")  # Update book details
        print("6. View Loan Requests")    # New option to view loan requests
        print("7. Process Loan Requests") # New option to approve/reject loan requests
        print("8. Logout")
        
        choice = input("Enter your choice (1/2/3/4/5/6/7/8): ")
        
        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            view_all_loans()
        elif choice == '4':
            view_students()
        elif choice == '5':
            update_book()
        elif choice == '6':
            view_loan_requests()  # View pending loan requests
        elif choice == '7':
            process_loan_request()  # Approve or reject loan requests
        elif choice == '8':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

# Function to add a book (Librarian only)
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author: ")
    publisher = input("Enter publisher: ")
    
    try:
        query = "INSERT INTO Books (title, author, publisher) VALUES (%s, %s, %s)"
        cursor.execute(query, (title, author, publisher))
        conn.commit()
        print("Book added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to view books (Available to both students and librarians)
def view_books():
    try:
        # Query to fetch all book details including publisher and authors
        query = """
            SELECT b.bookID, b.title, b.yearPublished, p.name AS publisher, GROUP_CONCAT(a.name SEPARATOR ', ') AS authors 
            FROM Books b
            LEFT JOIN Publishers p ON b.publisherID = p.publisherID
            LEFT JOIN BookAuthors ba ON b.bookID = ba.bookID
            LEFT JOIN Authors a ON ba.authorID = a.authorID
            GROUP BY b.bookID
        """
        cursor.execute(query)
        books = cursor.fetchall()

        if not books:
            print("No books found in the database.")
            return

        # Display the books in a formatted way
        print("\nList of Books:")
        print("-" * 80)
        for book in books:
            print(f"ID: {book[0]}")
            print(f"Title: {book[1]}")
            print(f"Year Published: {book[2]}")
            print(f"Publisher: {book[3]}")
            print(f"Authors: {book[4]}")
            print("-" * 80)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
def update_book():
    try:
        # Search for a book by title
        search_title = input("Enter the book title (or part of it) to search for: ")

        # Search for books matching the input title
        query = """
            SELECT b.bookID, b.title, b.yearPublished, p.name AS publisher, GROUP_CONCAT(a.name) AS authors 
            FROM Books b
            LEFT JOIN Publishers p ON b.publisherID = p.publisherID
            LEFT JOIN BookAuthors ba ON b.bookID = ba.bookID
            LEFT JOIN Authors a ON ba.authorID = a.authorID
            WHERE b.title LIKE %s
            GROUP BY b.bookID
        """
        cursor.execute(query, ('%' + search_title + '%',))
        books = cursor.fetchall()

        if not books:
            print("No books found with that title.")
            return

        # Display search results
        print("\nSearch Results:")
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Year Published: {book[2]}, Publisher: {book[3]}, Authors: {book[4]}")

        # Prompt the librarian to select a book by bookID
        book_id = input("\nEnter the ID of the book you want to update: ")

        # Fetch details of the selected book
        query = """
            SELECT b.title, b.yearPublished, p.name AS publisher, GROUP_CONCAT(a.name) AS authors 
            FROM Books b
            LEFT JOIN Publishers p ON b.publisherID = p.publisherID
            LEFT JOIN BookAuthors ba ON b.bookID = ba.bookID
            LEFT JOIN Authors a ON ba.authorID = a.authorID
            WHERE b.bookID = %s
            GROUP BY b.bookID
        """
        cursor.execute(query, (book_id,))
        book = cursor.fetchone()

        if not book:
            print("Book not found. Please try again.")
            return

        # Show current book details
        print(f"\nCurrent details - Title: {book[0]}, Year Published: {book[1]}, Publisher: {book[2]}, Authors: {book[3]}")

        # Ask the librarian which fields they want to update
        new_title = input(f"Enter new title (leave blank to keep '{book[0]}'): ") or book[0]
        new_year = input(f"Enter new year published (leave blank to keep '{book[1]}'): ") or book[1]
        new_publisher = input(f"Enter new publisher name (leave blank to keep '{book[2]}'): ") or book[2]
        new_authors = input(f"Enter new authors (comma-separated, leave blank to keep '{book[3]}'): ") or book[3]

        # Update book details in the `Books` table
        query = "UPDATE Books SET title = %s, yearPublished = %s WHERE bookID = %s"
        cursor.execute(query, (new_title, new_year, book_id))
        conn.commit()

        # Update publisher if changed (assumes publisher table is updated separately)
        if new_publisher != book[2]:
            # Check if the publisher exists, if not, create a new one
            query = "SELECT publisherID FROM Publishers WHERE name = %s"
            cursor.execute(query, (new_publisher,))
            publisher = cursor.fetchone()

            if not publisher:
                query = "INSERT INTO Publishers (name) VALUES (%s)"
                cursor.execute(query, (new_publisher,))
                publisher_id = cursor.lastrowid
            else:
                publisher_id = publisher[0]

            # Update the book's publisherID
            query = "UPDATE Books SET publisherID = %s WHERE bookID = %s"
            cursor.execute(query, (publisher_id, book_id))
            conn.commit()

        # Update authors in `BookAuthors` table
        if new_authors != book[3]:
            # First, delete old author associations
            query = "DELETE FROM BookAuthors WHERE bookID = %s"
            cursor.execute(query, (book_id,))

            # Insert new author associations
            author_names = [name.strip() for name in new_authors.split(',')]
            for author_name in author_names:
                # Check if the author exists, if not, create a new one
                query = "SELECT authorID FROM Authors WHERE name = %s"
                cursor.execute(query, (author_name,))
                author = cursor.fetchone()

                if not author:
                    query = "INSERT INTO Authors (name) VALUES (%s)"
                    cursor.execute(query, (author_name,))
                    author_id = cursor.lastrowid
                else:
                    author_id = author[0]

                # Insert into `BookAuthors`
                query = "INSERT INTO BookAuthors (bookID, authorID) VALUES (%s, %s)"
                cursor.execute(query, (book_id, author_id))

            conn.commit()

        print("Book details updated successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()

# Function to view loans (Librarian only)
def view_librarian_loans():
    try:
        query = "SELECT * FROM Loans"
        cursor.execute(query)
        loans = cursor.fetchall()

        print("\nLoans in the library:")
        for loan in loans:
            print(f"Loan ID: {loan[0]}, Student ID: {loan[1]}, Book ID: {loan[2]}, Date: {loan[3]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to view student loans (Student only)
def view_student_loans():
    student_id = input("Enter your student ID: ")
    
    try:
        query = "SELECT * FROM Loans WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        loans = cursor.fetchall()

        print("\nYour Loans:")
        for loan in loans:
            print(f"Loan ID: {loan[0]}, Book ID: {loan[2]}, Date: {loan[3]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to request a loan (Student only)
def get_loan():
    student_id = input("Enter your student ID: ")
    book_id = input("Enter the book ID you want to loan: ")

    try:
        # Insert a loan request into the LoanRequests table with 'pending' status
        query = "INSERT INTO LoanRequests (studentID, bookID) VALUES (%s, %s)"
        cursor.execute(query, (student_id, book_id))
        conn.commit()
        print("Loan request sent successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
# Function to view all book loans
# Function to view all loans
def view_all_loans():
    try:
        # Query to get loan details for all students
        query = """
        SELECT Loans.loanID, Students.name, Books.title, Loans.borrowDate, Loans.dueDate, Loans.returnDate
        FROM Loans
        INNER JOIN Books ON Loans.bookID = Books.bookID
        INNER JOIN Students ON Loans.studentID = Students.studentID
        """
        cursor.execute(query)
        loans = cursor.fetchall()

        if loans:
            print("\nAll Loans in the Library:")
            for loan in loans:
                loan_id, student_name, book_title, borrow_date, due_date, return_date = loan
                return_status = "Returned" if return_date else "Not Returned"
                print(f"Loan ID: {loan_id} | Student: {student_name} | Book Title: {book_title} | Borrow Date: {borrow_date} | Due Date: {due_date} | Return Status: {return_status}")
        else:
            print("No loans found in the library.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to view loans for the logged-in student
def view_loans():
    student_id = input("Enter your student ID: ")  # You can adjust to get the ID of the logged-in student

    try:
        # Query to get loan details for the student
        query = """
        SELECT Loans.loanID, Books.title, Loans.borrowDate, Loans.dueDate, Loans.returnDate
        FROM Loans
        INNER JOIN Books ON Loans.bookID = Books.bookID
        WHERE Loans.studentID = %s
        """
        cursor.execute(query, (student_id,))
        loans = cursor.fetchall()

        if loans:
            print("\nYour Loaned Books:")
            for loan in loans:
                loan_id, title, borrow_date, due_date, return_date = loan
                return_status = "Returned" if return_date else "Not Returned"
                print(f"Loan ID: {loan_id} | Book Title: {title} | Borrow Date: {borrow_date} | Due Date: {due_date} | Return Status: {return_status}")
        else:
            print("No loans found for this student.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to view pending loan requests
def view_loan_requests():
    try:
        query = """
            SELECT lr.requestID, s.name, b.title, lr.requestDate, lr.status
            FROM LoanRequests lr
            JOIN Students s ON lr.studentID = s.studentID
            JOIN Books b ON lr.bookID = b.bookID
            WHERE lr.status = 'pending'
        """
        cursor.execute(query)
        requests = cursor.fetchall()

        if not requests:
            print("No pending loan requests.")
            return

        print("\nPending Loan Requests:")
        print("-" * 80)
        for req in requests:
            print(f"Request ID: {req[0]} | Student: {req[1]} | Book: {req[2]}")
            print(f"Request Date: {req[3]} | Status: {req[4]}")
            print("-" * 80)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to approve or reject a loan request
def process_loan_request():
    request_id = input("Enter the request ID you want to process: ")
    action = input("Do you want to 'approve' or 'reject' this request? ").lower()

    if action not in ['approve', 'reject']:
        print("Invalid action. Please choose 'approve' or 'reject'.")
        return

    try:
        if action == 'approve':
            # Update the status in LoanRequests table
            update_query = "UPDATE LoanRequests SET status = 'approved' WHERE requestID = %s"
            cursor.execute(update_query, (request_id,))

            # Insert the loan into the Loans table
            query = """
                INSERT INTO Loans (studentID, bookID, borrowDate, dueDate)
                SELECT studentID, bookID, CURRENT_DATE, DATE_ADD(CURRENT_DATE, INTERVAL 14 DAY)
                FROM LoanRequests
                WHERE requestID = %s
            """
            cursor.execute(query, (request_id,))
        else:
            # Just update the status to 'rejected'
            update_query = "UPDATE LoanRequests SET status = 'rejected' WHERE requestID = %s"
            cursor.execute(update_query, (request_id,))

        conn.commit()
        print(f"Loan request {action}d successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to view all students
def view_students():
    try:
        # Query to fetch all students
        query = "SELECT studentID, name, email, phone FROM Students;"
        cursor.execute(query)
        students = cursor.fetchall()
        
        if students:
            print("\nStudent Records:")
            for student in students:
                student_id, name, email, phone = student
                print(f"Student ID: {student_id}, Name: {name}, Email: {email}, Phone: {phone}")
        else:
            print("No student records found.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to add a book with authors
def add_book():
    title = input("Enter the book title: ")
    publisher_name = input("Enter the publisher name: ")
    year_published = input("Enter the year of publication: ")
    author_names = input("Enter the author names (comma-separated): ").split(",")  # Multiple authors support
    
    try:
        # Step 1: Check if the publisher exists
        cursor.execute("SELECT publisherID FROM Publishers WHERE name = %s", (publisher_name,))
        publisher = cursor.fetchone()
        
        # Step 2: Insert a new publisher if it does not exist
        if not publisher:
            cursor.execute("INSERT INTO Publishers (name) VALUES (%s)", (publisher_name,))
            conn.commit()
            print(f"Publisher '{publisher_name}' added to the database.")
            cursor.execute("SELECT LAST_INSERT_ID()")  # Fetch the ID of the newly added publisher
            publisher_id = cursor.fetchone()[0]
        else:
            publisher_id = publisher[0]
        
        # Step 3: Insert the new book
        cursor.execute("INSERT INTO Books (title, publisherID, yearPublished) VALUES (%s, %s, %s)",
                       (title, publisher_id, year_published))
        conn.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        book_id = cursor.fetchone()[0]
        print(f"Book '{title}' added successfully with ID {book_id}!")
        
        # Step 4: Handle authors
        for author_name in author_names:
            author_name = author_name.strip()
            # Check if the author exists
            cursor.execute("SELECT authorID FROM Authors WHERE name = %s", (author_name,))
            author = cursor.fetchone()
            
            # Insert the author if not found
            if not author:
                cursor.execute("INSERT INTO Authors (name) VALUES (%s)", (author_name,))
                conn.commit()
                print(f"Author '{author_name}' added to the database.")
                cursor.execute("SELECT LAST_INSERT_ID()")  # Fetch the newly added author ID
                author_id = cursor.fetchone()[0]
            else:
                author_id = author[0]
            
            # Step 5: Link the book and author in BooksAuthors
            cursor.execute("INSERT INTO BookAuthors (bookID, authorID) VALUES (%s, %s)", (book_id, author_id))
            conn.commit()
            print(f"Author '{author_name}' linked to book '{title}'.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()

# Main CLI function
def main():
    execute_schema()  # Run schema creation

    print("Welcome to the University Library System")
    
    try:
        # Step 2: Connect to MySQL server (without specifying the database)
        global conn
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port="3306",
            database="mySchoolLibrary"  # Ensure database exists
        )
        global cursor
        cursor = conn.cursor()
        print("Connected to 'mySchoolLibrary' database successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

    while True:
        print("\nPlease choose your role:")
        print("1. Student")
        print("2. Librarian")
        print("3. Exit")
        
        role_choice = input("Enter your choice (1/2/3): ")
        
        if role_choice == '1':
            role = 'student'
        elif role_choice == '2':
            role = 'librarian'
        elif role_choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            continue
        
        print("\n1. Login")
        print("2. Create Account")
        action_choice = input("Enter your choice (1/2): ")
        
        if action_choice == '1':
            login(role)
        elif action_choice == '2':
            if role == 'student':
                create_student_account()
            else:
                create_librarian_account()
        else:
            print("Invalid choice. Please try again.")

    # Close the connection when the program ends
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed.")

if __name__ == "__main__":
    main()
