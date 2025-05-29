import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd
import os
from tkinter import filedialog

# ---------- Database Setup ----------
def connect():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            year INTEGER,
            isbn TEXT)
    """)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM books")
    if cur.fetchone()[0] == 0 and os.path.exists("sample_books_dataset.csv"):
        df = pd.read_csv("sample_books_dataset.csv")
        for _, row in df.iterrows():
            cur.execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)",
                        (row['title'], row['author'], row['year'], row['isbn']))
        conn.commit()
    conn.close()

# ---------- CRUD Functions ----------
def view():
    with sqlite3.connect("books.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM books")
        return cur.fetchall()

def insert(title, author, year, isbn):
    with sqlite3.connect("books.db") as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", (title, author, year, isbn))

def delete(book_id):
    with sqlite3.connect("books.db") as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id=?", (book_id,))

def update(book_id, title, author, year, isbn):
    with sqlite3.connect("books.db") as conn:
        cur = conn.cursor()
        cur.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?",
                    (title, author, year, isbn, book_id))

def search(title="", author="", year="", isbn=""):
    with sqlite3.connect("books.db") as conn:
        cur = conn.cursor()
        query = "SELECT * FROM books WHERE 1=1"
        values = []
        if title: query += " AND title LIKE ?"; values.append(f"%{title}%")
        if author: query += " AND author LIKE ?"; values.append(f"%{author}%")
        if year: query += " AND year=?"; values.append(year)
        if isbn: query += " AND isbn LIKE ?"; values.append(f"%{isbn}%")
        cur.execute(query, values)
        return cur.fetchall()

# ---------- Modern GUI with Dark/Light Mode ----------
class LibraryApp:
    def __init__(self, root):  # ✅ FIXED THIS LINE
        self.root = root
        self.root.title("Library Admin Dashboard")
        self.root.geometry("1000x600")
        self.dark_mode = False
        self.selected_book = None

        self.colors = {
            "light": {"bg": "#F4F6F8", "fg": "#000", "entry": "#fff", "button": "#3498DB", "sidebar": "#2C3E50", "sidebar_fg": "#fff"},
            "dark": {"bg": "#1E1E2F", "fg": "#fff", "entry": "#2A2A3B", "button": "#2980B9", "sidebar": "#11111B", "sidebar_fg": "#fff"},
        }

        self.set_theme()
        self.build_ui()

    def set_theme(self):
        self.theme = self.colors["dark" if self.dark_mode else "light"]
        self.root.configure(bg=self.theme["bg"])

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.set_theme()
        self.root.destroy()
        root = tk.Tk()
        app = LibraryApp(root)
        root.mainloop()

    def build_ui(self):
        sidebar = tk.Frame(self.root, width=200, bg=self.theme["sidebar"])
        sidebar.pack(side="left", fill="y")
        tk.Label(sidebar, text="Library", fg=self.theme["sidebar_fg"], bg=self.theme["sidebar"],
                 font=("Arial", 20, "bold")).pack(pady=20)

        for label in ["Dashboard", "Books", "Members", "Settings"]:
            tk.Button(sidebar, text=label, bg=self.theme["sidebar"], fg=self.theme["sidebar_fg"],
                      activebackground="#34495E", relief="flat", font=("Arial", 12),
                      anchor="w", padx=20).pack(fill="x", pady=2)

        topbar = tk.Frame(self.root, height=50, bg=self.theme["entry"])
        topbar.pack(side="top", fill="x")
        tk.Label(topbar, text="Welcome, Admin!", font=("Arial", 12), bg=self.theme["entry"], fg=self.theme["fg"]).pack(side="right", padx=20)
        tk.Button(topbar, text="Toggle Theme", command=self.toggle_theme, bg=self.theme["button"], fg="white", relief="flat").pack(side="left", padx=10)

        content = tk.Frame(self.root, bg=self.theme["bg"])
        content.pack(expand=True, fill="both")

        form_frame = tk.Frame(content, bg=self.theme["bg"])
        form_frame.pack(pady=20)

        self.entries = {}
        for i, field in enumerate(["Title", "Author", "Year", "ISBN"]):
            tk.Label(form_frame, text=field, bg=self.theme["bg"], fg=self.theme["fg"], font=("Arial", 10)).grid(row=0, column=i, padx=10)
            entry = tk.Entry(form_frame, width=20, bg=self.theme["entry"], fg=self.theme["fg"])
            entry.grid(row=1, column=i, padx=10)
            self.entries[field.lower()] = entry

        btn_frame = tk.Frame(content, bg=self.theme["bg"])
        btn_frame.pack(pady=10)
        buttons = [
            ("Add Book", self.add_book),
            ("Update", self.update_book),
            ("Delete", self.delete_book),
            ("Search", self.search_books),
            ("Show All", self.load_books),
            ("Export", self.export_books)
        ]
        for txt, cmd in buttons:
            tk.Button(btn_frame, text=txt, command=cmd, width=12, bg=self.theme["button"], fg="white", font=("Arial", 10), relief="flat").pack(side="left", padx=5)

        table_frame = tk.Frame(content, bg=self.theme["bg"])
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("id", "title", "author", "year", "isbn"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.select_book)

        self.load_books()

    def get_inputs(self):
        return (self.entries['title'].get(), self.entries['author'].get(), self.entries['year'].get(), self.entries['isbn'].get())

    def select_book(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.selected_book = values[0]
            for i, key in enumerate(["title", "author", "year", "isbn"]):
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(tk.END, values[i+1])

    def load_books(self):
        self.tree.delete(*self.tree.get_children())
        for book in view():
            self.tree.insert("", tk.END, values=book)

    def add_book(self):
        insert(*self.get_inputs())
        self.load_books()
        messagebox.showinfo("Success", "Book added.")

    def update_book(self):
        if self.selected_book:
            update(self.selected_book, *self.get_inputs())
            self.load_books()
            messagebox.showinfo("Updated", "Book updated.")

    def delete_book(self):
        if self.selected_book:
            delete(self.selected_book)
            self.load_books()
            messagebox.showinfo("Deleted", "Book deleted.")

    def search_books(self):
        self.tree.delete(*self.tree.get_children())
        for book in search(*self.get_inputs()):
            self.tree.insert("", tk.END, values=book)

    def export_books(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            books = view()
            df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Year", "ISBN"])
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Exported", f"Books exported to {file_path}")

# ---------- Run App ----------
if __name__ == "__main__":
    connect()
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
