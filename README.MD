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

2. We parse through the data, i created a list called "tunes" and a dictionary called "current_tunes" that will be used to store each tune
	i open the the file and read it, using .readlines() and store it in a variable called lines, lines is then used within the for loop to iterate through the tunes contents.
	I filter out 4 main keys 
	X: tune number
	T: title
	K: key
	R: type (jig)
	The loop firstly checks if the line begins with x, if not it saves the current tune its working on and stores it into the list "tunes".
	The loop also removes any whitespaces and trailing lines from the keys.
	Body is used to take the remainder of the information within each tune and store it in "body" after the main keys are finished being parsed

# List of files in the project

| Files | Source |
|-----------|-----------|
| ashCode.py | Self written |


# References
* Item 1
* Item 2

# What I am most proud of in the assignment

Bla bla bla

# What I learned

Bla bla bla

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
