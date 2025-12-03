# Data Centric Programming Assignment 2025

- [Assignment Brief](assignment.md)

Name: Arshdip Chera

Student Number: C24385641

# Screenshots

# Description of the project
Program designed to read 2 folders containing ABC files representing different books
The program parses and stores the tunes in a dictionary which is saved in a list
A database is used to store a table that takes the contents of each tunes.
Pandas is used for analysis of the data and 
We can access this data using a GUI

# Instructions for use
Run the program
A window will be opened with the 3 boxes that will let u search by:
Book number
Title
Jig
Input into the search bar which books youd like to look up 
# How it works:
First we import our libraries

1. Establish connection to our database tunes2.db that will be used to store our table
if the already exists, it gets dropped


2. #### Reading the File
- File is opened, all the inesa are read using readlines()

#### Parsing tunes 
- As the for loop iterates, the inforation is being tracked using current_tune via dictionary and all completed tunes are stored inside a list called "tunes"

#### Identifying tune informatiom
- X: Tune number
- T: Title
- K: Key signature
- R: Rhythm/type (e.g., jig)
- When the loop detects one of these keys it stores the information in current_tune

#### Detecting a new tune
- When a newe x appears
- The previous tune in current_tunes is then saved in the list tunes
- The next current_tune dictionary is created to take in the information of the next tune

#### Storing the Body
- Any other line that does not contain the main keys (x,t,k,r) is considered the body, which is the remainder of the information of the tunes and stored in "body"
- Finally when the loop ends and the last tune is added to the list "tunes" the parsed list is then returned 



```Python
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
```

3. 
#### Function inserting()
- Takes the parsed data and stores them into the rows of the sql database. We can later retrieve this information for searching and analysis

#### Establishing a DB connection
- The function creates a sql db called tunes2.db
- Cursor is used to execute sql commands

#### Table
- We dont know if a table exists before hand so the function makes sure to specify that "IF NOT EXIST" and creates the table with the rows
- id — auto-incrementing primary key
- book_number — identifies the source book the tune came from
- title — tune title
- key — key signature
- type — tune type (e.g. jig, reel)
- body — remaining ABC notation

#### Inserting
- The function loops through the newly parsed tunes and inserts them into the table, it uses .get to retrieve the dictionary values

#### Commiting the changes to the Database
- The database changes are saved with commit() then the connection is closed

```Python
def inserting(book_number,tunes):
    conn = sqlite3.connect("tunes2.db")
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE IF NOT EXISTS tunes2 (id INTEGER PRIMARY KEY AUTOINCREMENT, book_number INTEGER, title TEXT, key TEXT, type TEXT, body TEXT)')
    
    for tune in tunes: #1 is used to insert the data into a table
        
        cursor.execute('INSERT INTO tunes2(book_number,title,key,type,body) VALUES (?,?,?,?,?)',(book_number,tune.get("title", ""),tune.get("key", ""),tune.get("type", ""),tune.get("body", "")))
    conn.commit()
    conn.close()

```

4. Defining a function that takes file and book_number as parameters
- tunes stores the function process_file(file)
- tunes is then used to insert the tunes in the databasse

```Python
def process(file, book_number):
    tunes = process_file(file)
    inserting(book_number, tunes)
```

5. i call the function my_sql_database to drop the table each time the program is ran to avoid duplicate entries and errors (this is just trouble shooting)
ctdb() is used to return the connection query  is used to get every row from the table.
- load_tunes_from_database() holds all of this
- df is created to take in the connection and query and is read into pandas using p.read_sql

```Python
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
```

6. df is used to store the function load_tunes_from_database()

7. 3 pandas functions are created to load the tune ddata from the datatbase into the pandas df and provide filtering

- get_tunes_by_book(df, book_number)
Returns all tunes from a specific book number.

- get_tune(df, tune_type)
Returns all tunes that match a given tune type (e.g., "Single jig").

- search(df, search_terms)
Searches for tunes whose titles contain a given keyword (case-insensitive).

```Python
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
```
# List of files in the project

| Files | Source |
|-----------|-----------|
| ashCode.py | Self written |


# References
* tkinter tutorial #1[hyperlink](https://youtu.be/w5JhFN0CwOE?si=ioK0tFfDjpQGgBNd)
* tkinter tutorial #2[hyperlink](https://youtu.be/w5JhFN0CwOE?si=1R1h7kVcAqZKhuoi)
* Codecademy [hyperlink](https://www.codecademy.com)

# What I am most proud of in the assignment

The thing im most proud of in this assignment are the parsing and pandas parts. For the parsing of the contents i looked back on old python files and labs i had used before, on top of this i used the skills i have been getting frok codecademys Python 2 course and pandas course available on the website. Im proud that i could apply my knowledge and quickly get past these parts with little use of ai assistance or youtube tutorials.

# What I learned

What i learned in this assignment is the connection of a database in which i created the table and columns using python. At first i struggled with this part alot as i struggled with this in php, howeever after emailing my lecturer i was able to find the resources available to connect my file data to a sql table.

## Below is how to use Markdown. You can delete this:

## This is how to markdown text:

This is *emphasis*

This is a bulleted list

- Item
- Item

This is a numbered list

1. Item
1. Item

This is a [hyperlink](http://bryanduggan.org)

# Headings
## Headings
#### Headings
##### Headings

This is code:

```Java
public void render()
{
	ui.noFill();
	ui.stroke(255);
	ui.rect(x, y, width, height);
	ui.textAlign(PApplet.CENTER, PApplet.CENTER);
	ui.text(text, x + width * 0.5f, y + height * 0.5f);
}
```

So is this without specifying the language:

```
public void render()
{
	ui.noFill();
	ui.stroke(255);
	ui.rect(x, y, width, height);
	ui.textAlign(PApplet.CENTER, PApplet.CENTER);
	ui.text(text, x + width * 0.5f, y + height * 0.5f);
}
```

This is an image using a relative URL:

![An image](images/p8.png)

This is an image using an absolute URL:

![A different image](https://bryanduggandotorg.files.wordpress.com/2019/02/infinite-forms-00045.png?w=595&h=&zoom=2)

This is a youtube video:

[![YouTube](http://img.youtube.com/vi/J2kHSSFA4NU/0.jpg)](https://www.youtube.com/watch?v=J2kHSSFA4NU)

This is a table:

| Heading 1 | Heading 2 |
|-----------|-----------|
|Some stuff | Some more stuff in this column |
|Some stuff | Some more stuff in this column |
|Some stuff | Some more stuff in this column |

|Some stuff | Some more stuff in this column |
