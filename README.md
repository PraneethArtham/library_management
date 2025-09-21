Library Management System (Supabase + Python)

A simple library management system using Python and Supabase.
It supports CRUD operations, borrow/return transactions, and reports for overdue books.

Features

Members Management

Add, update, delete members

View member details and borrowed books

Books Management

Add, update, delete books

Check available books

Search books by title, author, or category

Borrow & Return

Borrow books (reduces stock)

Return books (updates borrow record and increases stock)

Handles validation for already borrowed books

Reports

List overdue books (borrowed more than 14 days ago)

Tech Stack

Python 3.x

Supabase (PostgreSQL database)

Supabase Python Client (pip install supabase)

Python-dotenv (pip install python-dotenv) for environment variables

Project Structure
library-management/
│
├── library_functions.py      # All CRUD, borrow/return, and report functions
├── main.py                   # Menu-driven main program
├── .env                      # Environment variables (SUPABASE_URL, SUPABASE_KEY)
└── README.md
