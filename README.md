# Software-engineering-code
*Created in year 2 semester 4 -> 2025*

This repository contains two desktop-based applications developed using **Python**, **Tkinter**, and **SQLite3**:

- 🏨 Hotel Management System
- 📚 Library Management System

These projects were developed as part of the **Software Engineering** course completed in **Year 2, Semester 4**. The aim was to apply software engineering principles in real-world applications through clean code structure, effective UI/UX, and database integration.

---

## 🏨 Hotel Management System

### 📌 Description

The **Hotel Management System** is a desktop application designed to streamline hotel operations like room tracking, guest registration, and booking management. It uses the `clam` theme for a modern user interface and stores all data using SQLite3.

### ✅ Features

- **Room Management**: Add rooms with type and price, view availability, delete if not booked.
- **Guest Management**: Register guests with name, phone, and email.
- **Booking Management**: Book or cancel rooms with validation for availability and date format.
- **Database**: Uses `hotel.db` with room, guest, and booking tables.
- **User Interface**: Clean Tkinter UI with Treeview display for tabular data.

### ⚙️ Requirements

- Python 3.6 or higher
- Tkinter (included with Python)
- SQLite3 (included with Python)

---

## Library Management System

### Description
The Library Management System is a desktop application built to simplify the management of books in a library. It features book tracking, dynamic search, and the ability to export data. The application also supports switching between light and dark themes and uses SQLite3 for data storage.

### Features
Book Management: Add, update, delete, and search for books using title, author, year, or ISBN.

Export Functionality: Export the book records to a CSV file using Pandas.

Theme Toggle: Switch between dark and light UI modes for better user experience.

Database: Uses books.db to store book records with automatic table creation.

User Interface: Modern Tkinter-based GUI with Treeview for tabular display and interactive elements.

### Requirements
Python 3.6 or higher

Tkinter (included with Python)

SQLite3 (included with Python)

Pandas (install using pip install pandas)
