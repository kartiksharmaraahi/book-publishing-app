import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a database to store book information
def create_db():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author TEXT,
                    genre TEXT
                )''')
    conn.commit()
    conn.close()

# Add a book to the database
def add_book(title, author, genre):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('INSERT INTO books (title, author, genre) VALUES (?, ?, ?)', (title, author, genre))
    conn.commit()
    conn.close()

# Fetch all books from the database
def get_books():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books')
    books = c.fetchall()
    conn.close()
    return books

# Delete a book from the database by ID
def delete_book(book_id):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

# Function to handle book addition
def on_add_button_click():
    title = title_entry.get()
    author = author_entry.get()
    genre = genre_entry.get()
    
    if not title or not author or not genre:
        messagebox.showerror("Input Error", "All fields must be filled!")
    else:
        add_book(title, author, genre)
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        genre_entry.delete(0, tk.END)
        update_book_list()

# Function to handle book deletion
def on_delete_button_click():
    try:
        selected_item = book_listbox.curselection()
        book_id = book_listbox.get(selected_item[0]).split(" - ")[0]  # Get book ID from the list
        delete_book(book_id)
        update_book_list()
    except IndexError:
        messagebox.showerror("Selection Error", "Please select a book to delete.")

# Update the listbox with the current books in the database
def update_book_list():
    book_listbox.delete(0, tk.END)  # Clear current list
    books = get_books()
    for book in books:
        book_listbox.insert(tk.END, f"{book[0]} - {book[1]} by {book[2]} (Genre: {book[3]})")

# Initialize the database
create_db()

# Set up the main window
root = tk.Tk()
root.title("Book Publishing App")
root.geometry("500x400")

# Add UI components
title_label = tk.Label(root, text="Title:")
title_label.pack()

title_entry = tk.Entry(root, width=40)
title_entry.pack()

author_label = tk.Label(root, text="Author:")
author_label.pack()

author_entry = tk.Entry(root, width=40)
author_entry.pack()

genre_label = tk.Label(root, text="Genre:")
genre_label.pack()

genre_entry = tk.Entry(root, width=40)
genre_entry.pack()

add_button = tk.Button(root, text="Add Book", command=on_add_button_click)
add_button.pack()

# Listbox to display books
book_listbox = tk.Listbox(root, width=60, height=10)
book_listbox.pack()

# Delete Button
delete_button = tk.Button(root, text="Delete Selected Book", command=on_delete_button_click)
delete_button.pack()

# Update the book list at the start
update_book_list()

# Run the application
root.mainloop()
