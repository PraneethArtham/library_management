from library_functions import *

def main():
    while True:
        print("\n=== Library Management ===")
        print("1. Add Member")
        print("2. Add Book")
        print("3. Display Members")
        print("4. Available Books")
        print("5. Search Book")
        print("6. Member Details")
        print("7. Update Book")
        print("8. Update Member")
        print("9. Delete Member")
        print("10. Delete Book")
        print("11. Borrow Book")
        print("12. Return Book")
        print("13. Overdue Books")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        actions = {
            "1": lambda: add_members(
                int(input("Member ID: ")),
                input("Name: "),
                input("Email: "),
                input("Join Date (YYYY-MM-DD): ")
            ),
            "2": lambda: add_books(
                int(input("Book ID: ")),
                input("Title: "),
                input("Author: "),
                input("Category: "),
                int(input("Stock: "))
            ),
            "3": display,
            "4": available_books,
            "5": lambda: search(input("Enter title/author/category: ")),
            "6": lambda: member_details(int(input("Member ID: "))),
            "7": lambda: update_book(input("Title: "), int(input("New Stock: "))),
            "8": lambda: update_member(input("Name: "), input("New Email: ")),
            "9": lambda: delete_member(int(input("Member ID: "))),
            "10": lambda: delete_book(int(input("Book ID: "))),
            "11": lambda: borrow_book(int(input("Member ID: ")), int(input("Book ID: "))),
            "12": lambda: return_book(int(input("Member ID: ")), int(input("Book ID: "))),
            "13": overdue_books
        }

        func = actions.get(choice)
        if func:
            result = func()
            print("Result:", result)
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
