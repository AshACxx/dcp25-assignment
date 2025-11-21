import sqlite3
import tkinter as tk
from tkinter import ttk

def db():
    conn = sqlite3.connect("example.db")
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS people(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            city TEXT
        )
    """)

    cur.execute("SELECT COUNT(*) FROM people")

    if cur.fetchone()[0] == 0:
        data = [
            ("Alice", 23, "Dublin"),
            ("Bob", 31, "Cork"),
            ("Charlie", 29, "Galway"),
            ("Daniel", 40, "Limerick"),
            ("Eve", 22, "Waterford")
        ]
        cur.executemany("INSERT INTO people (name, age, city) VALUES (?, ?, ?)", data)
        conn.commit()

    conn.close()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Table")

        # Correct — store connection & cursor in class
        self.conn = sqlite3.connect("example.db")
        self.cur = self.conn.cursor()

        # Search bar
        self.search_var = tk.StringVar()
        search_frame = tk.Frame(root)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT)
        tk.Button(search_frame, text="Filter", command=self.filter_table).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Reset", command=self.load_tab).pack(side=tk.LEFT)

        # Table
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Age", "City"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("City", text="City")

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Age", width=60)
        self.tree.column("City", width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_tab()

    def load_tab(self):
        # Clear old rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Load all
        self.cur.execute("SELECT * FROM people")
        rows = self.cur.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def filter_table(self):
        query = self.search_var.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cur.execute("""
            SELECT * FROM people 
            WHERE name LIKE ? OR city LIKE ?
        """, (f"%{query}%", f"%{query}%"))

        for row in self.cur.fetchall():
            self.tree.insert("", tk.END, values=row)


# Run app
if __name__ == "__main__":
    db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
