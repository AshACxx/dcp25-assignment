#IMPORTANT, I HAD TO DELETE MY REPO AND RETSART EVERYTHING, LOTS OF PROGRESS MAY BE MADE IN A SHORT TIME

# Starter code for Data Centric Programming Assignment 2025

# os is a module that lets us access the file system

# Bryan Duggan likes Star Trek
# Bryan Duggan is a great flute player

import os 
import sqlite3
import pandas as pd

# sqlite for connecting to sqlite databases

# An example of how to create a table, insert data
# and run a select query
'''
def do_databasse_stuff():

    conn = sqlite3.connect('tunes.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, age INTEGER)')

    # Insert data
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('John', 30))

    # Save changes
    conn.commit()

    cursor.execute('SELECT * FROM users')

    # Get all results
    results = cursor.fetchall()

    # Print results
    for row in results:
        print(row)    
        print(row[0])
        print(row[1])
    # Close
    
    df = pd.read_sql("SELECT * FROM users", conn)
    print(df.head())
    conn.close()
'''
def my_sql_database():
    conn = sqlite3.connect("tunes.db")
    conn = conn = sqlite3.connect('tunes.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tunes")
    conn.commit()
    conn.close()
    
    

books_dir = "abc_books"



def process_file(file):
    
    tunes = []
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
            
        
        else:
            if current_tune:
                current_tune["body"] += line + "\n"
                
                
    if current_tune:
        tunes.append(current_tune)
        
    return tunes


def inserting(book_number,tunes):
    conn = sqlite3.connect("tunes.db")
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE IF NOT EXISTS tunes (id INTEGER PRIMARY KEY AUTOINCREMENT, book_number INTEGER, title TEXT, key TEXT, body TEXT)')
    
    for tune in tunes:
        
        cursor.execute('INSERT INTO tunes(book_number,title,key, body) VALUES (?,?,?,?)',(book_number,tune.get("title", ""),tune.get("key", ""),tune.get("body", "")))

    conn.commit()
    conn.close()

def process(file, book_number):
    tunes = process_file(file)
    inserting(book_number, tunes)


my_sql_database()
# do_databasse_stuff()

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
    conn = sqlite3.connect('tunes.db')
    return conn

def load_tunes_from_database():
    #variable conn holds the function ctdb
    conn = ctdb()
    #selecting all columns from tunes
    query = "SELECT * FROM tunes"
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


book2_t = get_tunes_by_book(df, book_number)
print(book2_t[["title","key"]].head())