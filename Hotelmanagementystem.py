import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime  # For handling dates

# Database setup
conn = sqlite3.connect('hotel.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS rooms (
    room_number INTEGER PRIMARY KEY,
    room_type TEXT,
    price REAL,
    is_available INTEGER DEFAULT 1  -- 1 for available, 0 for occupied
)''')

c.execute('''CREATE TABLE IF NOT EXISTS guests (
    guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number INTEGER,
    guest_id INTEGER,
    check_in_date TEXT,
    check_out_date TEXT,
    FOREIGN KEY (room_number) REFERENCES rooms(room_number),
    FOREIGN KEY (guest_id) REFERENCES guests(guest_id)
)''')

conn.commit()


class HotelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Hotel Management System")
        self.root.geometry("1000x700")  # Increased size
        self.style = ttk.Style()
        self.configure_style()
        self.create_widgets()
        self.load_rooms()  # Load rooms on startup
        self.load_bookings() # Load bookings on startup

    def configure_style(self):
        # Configure the style for a modern look
        self.style.theme_use('clam')  # Use a modern theme

        # Configure colors
        bg_color = "#f0f0f0"  # Light gray background
        fg_color = "#333333"  # Dark gray foreground
        accent_color = "#007acc"  # Blue accent color
        highlight_color = "#4CAF50"  # Green highlight color

        self.root.configure(bg=bg_color)

        # Configure LabelFrame
        self.style.configure("TLabelframe", background=bg_color, borderwidth=0)
        self.style.configure("TLabelframe.Label", foreground=fg_color, font=('Arial', 12, 'bold'), background=bg_color)

        # Configure Labels
        self.style.configure("TLabel", background=bg_color, foreground=fg_color, font=('Arial', 10))

        # Configure Entries
        self.style.configure("TEntry", fieldbackground="white", foreground=fg_color, borderwidth=1)

        # Configure Buttons
        self.style.configure("TButton", background=accent_color, foreground="white", font=('Arial', 10, 'bold'), borderwidth=0, padding=6)
        self.style.map("TButton",
                       background=[("active", highlight_color)],
                       foreground=[("active", "white")])

        # Configure Combobox
        self.style.configure("TCombobox", fieldbackground="white", foreground=fg_color, borderwidth=1)

        # Configure Treeview
        self.style.configure("Treeview", background="white", foreground=fg_color, fieldbackground="white")
        self.style.configure("Treeview.Heading", background=bg_color, foreground=fg_color, font=('Arial', 10, 'bold'))
        self.style.map("Treeview.Heading",
                       background=[('active', highlight_color)],
                       foreground=[('active', 'white')])

    def create_widgets(self):
        # --- Room Management Frame ---
        room_frame = ttk.LabelFrame(self.root, text="Room Management")
        room_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(room_frame, text="Room Number").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.room_number_var = tk.IntVar()
        ttk.Entry(room_frame, textvariable=self.room_number_var, width=10).grid(row=0, column=1, padx=5, sticky="w")

        ttk.Label(room_frame, text="Room Type").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.room_type_var = tk.StringVar()
        ttk.Combobox(room_frame, textvariable=self.room_type_var, values=["Single", "Double", "Suite"], width=10).grid(row=0, column=3, padx=5, sticky="w")

        ttk.Label(room_frame, text="Price").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.room_price_var = tk.DoubleVar()
        ttk.Entry(room_frame, textvariable=self.room_price_var, width=10).grid(row=0, column=5, padx=5, sticky="w")

        ttk.Button(room_frame, text="Add Room", command=self.add_room).grid(row=0, column=6, padx=10, pady=5, sticky="w")
        ttk.Button(room_frame, text="Delete Room", command=self.delete_room).grid(row=0, column=7, padx=10, pady=5, sticky="w")

        # --- Guest Management Frame ---
        guest_frame = ttk.LabelFrame(self.root, text="Guest Management")
        guest_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(guest_frame, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.guest_name_var = tk.StringVar()
        ttk.Entry(guest_frame, textvariable=self.guest_name_var, width=20).grid(row=0, column=1, padx=5, sticky="w")

        ttk.Label(guest_frame, text="Phone").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.guest_phone_var = tk.StringVar()
        ttk.Entry(guest_frame, textvariable=self.guest_phone_var, width=15).grid(row=0, column=3, padx=5, sticky="w")

        ttk.Label(guest_frame, text="Email").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.guest_email_var = tk.StringVar()
        ttk.Entry(guest_frame, textvariable=self.guest_email_var, width=25).grid(row=0, column=5, padx=5, sticky="w")

        ttk.Button(guest_frame, text="Add Guest", command=self.add_guest).grid(row=0, column=6, padx=10, pady=5, sticky="w")

        # --- Booking Management Frame ---
        booking_frame = ttk.LabelFrame(self.root, text="Booking Management")
        booking_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(booking_frame, text="Room Number").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.booking_room_number_var = tk.IntVar()
        ttk.Entry(booking_frame, textvariable=self.booking_room_number_var, width=10).grid(row=0, column=1, padx=5, sticky="w")

        ttk.Label(booking_frame, text="Guest ID").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.booking_guest_id_var = tk.IntVar()
        ttk.Entry(booking_frame, textvariable=self.booking_guest_id_var, width=10).grid(row=0, column=3, padx=5, sticky="w")

        ttk.Label(booking_frame, text="Check-in Date (YYYY-MM-DD)").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.check_in_date_var = tk.StringVar()
        ttk.Entry(booking_frame, textvariable=self.check_in_date_var, width=15).grid(row=0, column=5, padx=5, sticky="w")

        ttk.Label(booking_frame, text="Check-out Date (YYYY-MM-DD)").grid(row=0, column=6, padx=5, pady=5, sticky="e")
        self.check_out_date_var = tk.StringVar()
        ttk.Entry(booking_frame, textvariable=self.check_out_date_var, width=15).grid(row=0, column=7, padx=5, sticky="w")

        ttk.Button(booking_frame, text="Create Booking", command=self.create_booking).grid(row=0, column=8, padx=10, pady=5, sticky="w")
        ttk.Button(booking_frame, text="Delete Booking", command=self.delete_booking).grid(row=0, column=9, padx=10, pady=5, sticky="w")


        # --- Room List Frame ---
        room_list_frame = ttk.LabelFrame(self.root, text="Room List")
        room_list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        room_columns = ("room_number", "room_type", "price", "is_available")
        self.room_tree = ttk.Treeview(room_list_frame, columns=room_columns, show="headings")
        for col in room_columns:
            self.room_tree.heading(col, text=col.replace("_", " ").title())
            self.room_tree.column(col, anchor="center")
        self.room_tree.pack(fill="both", expand=True)

        # --- Booking List Frame ---
        booking_list_frame = ttk.LabelFrame(self.root, text="Booking List")
        booking_list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        booking_columns = ("booking_id", "room_number", "guest_id", "check_in_date", "check_out_date")
        self.booking_tree = ttk.Treeview(booking_list_frame, columns=booking_columns, show="headings")
        for col in booking_columns:
            self.booking_tree.heading(col, text=col.replace("_", " ").title())
            self.booking_tree.column(col, anchor="center")
        self.booking_tree.pack(fill="both", expand=True)


    # --- Room Management Functions ---
    def add_room(self):
        try:
            room_number = self.room_number_var.get()
            room_type = self.room_type_var.get()
            price = self.room_price_var.get()

            if not all([room_number, room_type, price]):
                raise ValueError("Please fill all room details.")

            c.execute("INSERT INTO rooms (room_number, room_type, price) VALUES (?, ?, ?)",
                      (room_number, room_type, price))
            conn.commit()
            self.load_rooms()
            messagebox.showinfo("Success", "Room added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Room number already exists.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def delete_room(self):
        try:
            room_number = self.room_number_var.get()
            if not room_number:
                raise ValueError("Please enter a room number to delete.")

            # Check if the room is currently booked
            c.execute("SELECT * FROM bookings WHERE room_number = ?", (room_number,))
            if c.fetchone():
                messagebox.showerror("Error", "Cannot delete room. It is currently booked.")
                return

            c.execute("DELETE FROM rooms WHERE room_number = ?", (room_number,))
            conn.commit()
            self.load_rooms()
            messagebox.showinfo("Success", "Room deleted successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def load_rooms(self):
        for row in self.room_tree.get_children():
            self.room_tree.delete(row)
        c.execute("SELECT * FROM rooms")
        for room in c.fetchall():
            self.room_tree.insert("", "end", values=room)

    # --- Guest Management Functions ---
    def add_guest(self):
        try:
            name = self.guest_name_var.get()
            phone = self.guest_phone_var.get()
            email = self.guest_email_var.get()

            if not all([name, phone, email]):
                raise ValueError("Please fill all guest details.")

            c.execute("INSERT INTO guests (name, phone, email) VALUES (?, ?, ?)",
                      (name, phone, email))
            conn.commit()
            messagebox.showinfo("Success", "Guest added successfully! Note the Guest ID for bookings.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # --- Booking Management Functions ---
    def create_booking(self):
        try:
            room_number = self.booking_room_number_var.get()
            guest_id = self.booking_guest_id_var.get()
            check_in_date = self.check_in_date_var.get()
            check_out_date = self.check_out_date_var.get()

            if not all([room_number, guest_id, check_in_date, check_out_date]):
                raise ValueError("Please fill all booking details.")

            # Validate date format (YYYY-MM-DD)
            try:
                datetime.datetime.strptime(check_in_date, '%Y-%m-%d')
                datetime.datetime.strptime(check_out_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Incorrect date format, should be YYYY-MM-DD")

            # Check if the room is available
            c.execute("SELECT is_available FROM rooms WHERE room_number = ?", (room_number,))
            result = c.fetchone()
            if not result or result[0] == 0:
                raise ValueError("Room is not available.")

            # Check if the guest exists
            c.execute("SELECT * FROM guests WHERE guest_id = ?", (guest_id,))
            if not c.fetchone():
                raise ValueError("Guest ID not found.")

            # Create the booking
            c.execute("INSERT INTO bookings (room_number, guest_id, check_in_date, check_out_date) VALUES (?, ?, ?, ?)",
                      (room_number, guest_id, check_in_date, check_out_date))

            # Update room availability
            c.execute("UPDATE rooms SET is_available = 0 WHERE room_number = ?", (room_number,))

            conn.commit()
            self.load_rooms()  # Refresh room list
            self.load_bookings() # Refresh booking list
            messagebox.showinfo("Success", "Booking created successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def delete_booking(self):
        try:
            room_number = self.booking_room_number_var.get()
            guest_id = self.booking_guest_id_var.get()
            check_in_date = self.check_in_date_var.get()
            check_out_date = self.check_out_date_var.get()

            if not all([room_number, guest_id, check_in_date, check_out_date]):
                raise ValueError("Please fill all booking details to delete.")

            # Delete the booking
            c.execute("DELETE FROM bookings WHERE room_number = ? AND guest_id = ? AND check_in_date = ? AND check_out_date = ?",
                      (room_number, guest_id, check_in_date, check_out_date))

            # Update room availability
            c.execute("UPDATE rooms SET is_available = 1 WHERE room_number = ?", (room_number,))

            conn.commit()
            self.load_rooms()  # Refresh room list
            self.load_bookings() # Refresh booking list
            messagebox.showinfo("Success", "Booking deleted successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def load_bookings(self):
        for row in self.booking_tree.get_children():
            self.booking_tree.delete(row)
        c.execute("SELECT * FROM bookings")
        for booking in c.fetchall():
            self.booking_tree.insert("", "end", values=booking)


if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementApp(root)
    root.mainloop()
