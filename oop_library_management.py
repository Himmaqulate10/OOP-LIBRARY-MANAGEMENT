"""Library Management System (Object-Oriented version)

Classes:
    Book       - one book and its borrowed/available state
    Account    - base class for anyone who can log in
    Librarian  - an Account that can add and remove books
    User       - an Account that can view, search, borrow and return books
    Library    - stores the books and accounts, and does the actual work
    LibraryApp - the signup / login screen that runs the program
"""


class Book:
    def __init__(self, title, author):
        self.title = title.strip()
        self.author = author.strip()
        self.borrowed = False  # False = available, True = borrowed

    def borrow(self):
        """Mark the book as borrowed. Returns False if it was already borrowed."""
        if self.borrowed:
            return False
        self.borrowed = True
        return True

    def give_back(self):
        """Mark the book as returned. Returns False if it was not borrowed."""
        if not self.borrowed:
            return False
        self.borrowed = False
        return True

    def matches(self, keyword):
        keyword = keyword.lower()
        return keyword in self.title.lower() or keyword in self.author.lower()

    def __str__(self):
        status = "Borrowed" if self.borrowed else "Available"
        return f"{self.title} by {self.author} [{status}]"


class Account:
    role = "account"

    def __init__(self, username, password):
        self.username = username
        self._password = password

    def check_password(self, password):
        return self._password == password

    def menu(self, library):
        raise NotImplementedError("Each account type must define its own menu")


class Librarian(Account):
    role = "librarian"

    def menu(self, library):
        print(f"\nWelcome Librarian {self.username}")
        while True:
            option = input(
                "\nWhat would you like to do: \n1. Add a Book \n2. Remove a Book "
                "\n3. Logout \n: "
            )
            if option == "1":
                title = input("Enter Book title: ")
                author = input("Enter Book author: ")
                library.add_book(title, author)
                print(f"Successfully added '{title}'")
            elif option == "2":
                title = input("Title of the book you want to remove: ")
                if library.remove_book(title):
                    print(f"Successfully removed '{title}'")
                else:
                    print("Book not found")
            elif option == "3":
                print(f"Goodbye {self.username}")
                break
            else:
                print("Invalid input")


class User(Account):
    role = "user"

    def menu(self, library):
        print(f"\nWelcome {self.username}")
        while True:
            option = input(
                "\n1. View all books \n2. Search for a book \n3. Borrow a book "
                "\n4. Return a book \n5. Exit \n: "
            )
            if option == "1":
                self.view_books(library)
            elif option == "2":
                keyword = input("Enter title or author to search: ")
                self.search_books(library, keyword)
            elif option == "3":
                title = input("Title of the book you want to borrow: ")
                self.borrow_book(library, title)
            elif option == "4":
                title = input("Title of the book you want to return: ")
                self.return_book(library, title)
            elif option == "5":
                print(f"Goodbye {self.username}")
                break
            else:
                print("Invalid input")

    def view_books(self, library):
        if not library.books:
            print("No books in the library")
            return
        print("\n--- ALL BOOKS ---")
        for number, book in enumerate(library.books, start=1):
            print(f"{number}. {book}")

    def search_books(self, library, keyword):
        results = library.search(keyword)
        if not results:
            print("No book found")
            return
        for book in results:
            print(f"- {book}")

    def borrow_book(self, library, title):
        book = library.find_book(title)
        if book is None:
            print("Book not found")
        elif book.borrow():
            print(f"You have borrowed '{book.title}'")
        else:
            print("Sorry, this book has already been borrowed")

    def return_book(self, library, title):
        book = library.find_book(title)
        if book is None:
            print("Book not found")
        elif book.give_back():
            print(f"You have returned '{book.title}'. Thank you!")
        else:
            print("This book was not borrowed")


class Library:
    ROLES = {"librarian": Librarian, "user": User}

    def __init__(self, name):
        self.name = name
        self.books = []
        self.accounts = {}  # {username: Account}

    # ---- books ----
    def add_book(self, title, author):
        self.books.append(Book(title, author))

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.strip().lower():
                return book
        return None

    def remove_book(self, title):
        book = self.find_book(title)
        if book is None:
            return False
        self.books.remove(book)
        return True

    def search(self, keyword):
        return [book for book in self.books if book.matches(keyword)]

    # ---- accounts ----
    def signup(self, username, password, role):
        if username in self.accounts:
            print("Username already taken. Try another one.")
            return False
        self.accounts[username] = self.ROLES[role](username, password)
        print(f"Signup successful as a {role}! You can now login.")
        return True

    def login(self, username, password):
        account = self.accounts.get(username)
        if account and account.check_password(password):
            print("Login Successful")
            return account
        print("Wrong username or password")
        return None


class LibraryApp:
    def __init__(self, library):
        self.library = library

    def run(self):
        while True:
            print(f"\nWELCOME to {self.library.name}")
            choice = input("1. Signup \n2. Login \n3. Exit \n: ")

            if choice == "1":
                self.signup_screen()
            elif choice == "2":
                self.login_screen()
            elif choice == "3":
                break
            else:
                print("Invalid input, Try again!")

                print(f"Thank you for visiting {self.library.name}")
    def signup_screen(self):
        username = input("Choose a Username: ")
        role_choice = input("Sign up as: \n1. Librarian \n2. User \n: ")
        if role_choice == "1":
            role = "librarian"
        elif role_choice == "2":
            role = "user"
        else:
            print("Invalid input, Try again!")
            return
        password = input("Choose a Password: ")
        self.library.signup(username, password, role)

    def login_screen(self):
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        account = self.library.login(username, password)
        if account:
            account.menu(self.library)


def main():
    library = Library("Himmaqulate Library")

    starting_books = [
        ("Making It Big", "Femi Otedola"),
        ("Rich Dad Poor Dad", "Robert Kiyosaki (co-authored with Sharon Lechter)"),
        ("The Seven Habits of Highly Effective People", "Stephen Covey"),
        ("She Stoops to Conquer", "Oliver Goldsmith"),
        ("A Raisin in the Sun", "Lorraine Hansberry"),
        ("The Power of Now", "Eckhart Tolle"),
    ]
    for title, author in starting_books:
        library.add_book(title, author)

    # Default librarian account
    library.signup("admin", "1234", "librarian")

    LibraryApp(library).run()


if __name__ == "__main__":
    main()