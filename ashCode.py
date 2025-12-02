
import os 
import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import scrolledtext

def my_sql_database():
    ''' 
    old code 
    conn = sqlite3.connect("tunes2.db")

    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS tunes2")
    conn.commit()
    conn.close()
    '''
    #improvement recc by ai 
    conn = sqlite3.connect("tunes2.db")

    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS tunes2")
    conn.commit()
    conn.close()
    
    
    

books_dir = "abc_books"



def process_file(file):
    
    tunes = [] #1
    current_tune = {}
    
    with open(file, 'r') as f:
        lines = f.readlines()
    # list comprehension to strip the \n's
    lines = [line.strip() for line in lines]

    # just print the files for now
    for line in lines:
        
        
        #if the line starts with X, we are on a tune
        if line.startswith("X:"):
            #saving previous tune 
            if current_tune:
                tunes.append(current_tune)
                
            #new tune present 
            current_tune = {"X": line[2:].strip(),"body":""}
            print(line)  
                
        elif line.startswith("T:"):
            current_tune["title"] = line[2:].strip()
            
        elif line.startswith("K:"):
            current_tune["key"] = line[2:].strip()
            
        elif line.startswith("R:"):
            current_tune["type"] = line[2:].strip()
            
        #current_tune["body"] taking "body from the dictionary and adding the lines that dont have x t k or r
        else:
            
            
            if "body" not in current_tune:
                #making body a key
                current_tune["body"] = ""
                #adding on body to a new line
            current_tune["body"] += line + "\n"
                
                
    if current_tune:
        tunes.append(current_tune)
        
    return tunes #returns to #1


def inserting(book_number,tunes):
    conn = sqlite3.connect("tunes2.db")
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE IF NOT EXISTS tunes2 (id INTEGER PRIMARY KEY AUTOINCREMENT, book_number INTEGER, title TEXT, key TEXT, type TEXT, body TEXT)')
    
    for tune in tunes: #1 is used to insert the data into a table
        
        cursor.execute('INSERT INTO tunes2(book_number,title,key,type,body) VALUES (?,?,?,?,?)',(book_number,tune.get("title", ""),tune.get("key", ""),tune.get("type", ""),tune.get("body", "")))
    conn.commit()
    conn.close()

def process(file, book_number):
    tunes = process_file(file)
    inserting(book_number, tunes)


my_sql_database()


# Iterate over directories in abc_books
for item in os.listdir(books_dir):
    # item is the dir name, this makes it into a path
    item_path = os.path.join(books_dir, item)
    
    # Check if it's a directory and has a numeric name
    if os.path.isdir(item_path) and item.isdigit():
        book_number = int(item)
        print(f"Found numbered directory: {item}")
        
        # Iterate over files in the numbered directory
        for file in os.listdir(item_path):
            # Check if file has .abc extension
            if file.endswith('.abc'):
                file_path = os.path.join(item_path, file)
                print(f"  Found abc file: {file}")
                process(file_path,book_number)
                
def ctdb():
    conn = sqlite3.connect('tunes2.db')
    return conn

def load_tunes_from_database():
    #variable conn holds the function ctdb
    conn = ctdb()
    #selecting all columns from tunes
    query = "SELECT * FROM tunes2"
    #creating a data from 
    df = pd.read_sql(query, conn)
    conn.close()
    
    return df

#df holds the function above
df = load_tunes_from_database()

#displays the values of each book file
print(df["book_number"].value_counts())

def get_tunes_by_book(df, book_number):
    """Get all tunes from a specific book"""
    df = df[df["book_number"] ==  book_number]
    return df

#displays all the tunes from 3400 onwards as this is book2 (abc files)

def get_tune(df, tune_type):
    df_2 = df[df["type"]==tune_type]
    return df_2

#printing the title and key
book2_t = get_tunes_by_book(df, 2)
print(book2_t[["title","key"]].head())


#function to return the title of a song
def search(df, search_terms):
    df_3 = df[df["title"].str.contains(search_terms, case = False)]
    return df_3
#returning rthe title andd jig of a song

book3_t = get_tune(df, "Single jig")
print(book3_t[["title","type"]].head())

#tkinter menu
def launch_gui(df):
    
    #main window
    my_w = tk.Tk()
    my_w.title("ABC Tune Database")
    my_w.geometry("750x600")

    output = scrolledtext.ScrolledText(my_w, width=90, height=25)
    output.pack(pady=10)

    def show(df):
        #clears text box
        output.delete(1.0, tk.END)
        
        if df.empty:
            #if the df has no rows/ data it displays no
            output.insert(tk.END, "No results found.\n")
            #returning no result to df
            return
        
        for i, row in df.iterrows():
            #outputting (printing) the rows in the main window
            output.insert(tk.END, f"Title: {row['title']}\n")
            
            output.insert(tk.END, f"Type: {row['type']}\n")
            
            output.insert(tk.END, f"Key: {row['key']}\n")
            
            output.insert(tk.END, f"Book: {row['book_number']}\n")
            
            #adding lines to seperate 
            output.insert(tk.END, "-"*50 + "\n")
    

    #search by book number
    #.pack is used to horiztonally or vertically place the widgets after another 
    #.pack() lets me stack the name and asearch bar on top of eachother
    
    tk.Label (my_w, text="Search by Book Number:", font=("Arial",10)).pack()
    
    book_entry = tk.Entry(my_w)
    book_entry.pack()
    
    #creating a button, using lambda to create a mini function name (tkinter cant take calls) inserting the dataframe and using .get() to return the specified key
    #FOR FUTURE: user types into entry > when u click the button mini funcyion runs > returns number > get_tunes_by_book filters dataframe to book (1)or(2)
    
    tk.Button(my_w, text="Search", command=lambda:show(get_tunes_by_book(df, int(book_entry.get())))).pack()

    #search by tune type
    tk.Label(my_w, text="\nSearch by Type:").pack()
    type_entry = tk.Entry(my_w)
    
    type_entry.pack()
    tk.Button(my_w, text="Search", command=lambda: show(get_tune(df, type_entry.get()))).pack()

    # Search by title
    tk.Label(my_w, text="\nSearch by Title:").pack()
    title_entry = tk.Entry(my_w)
    title_entry.pack()
    tk.Button(my_w, text="Search", command=lambda: show(search(df, title_entry.get()))).pack()

    my_w.mainloop()


# REPLACE TEXT UI WITH TKINTER
launch_gui(df)
