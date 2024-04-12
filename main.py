import requests
import sqlite3
import json
import pandas as pd
import matplotlib.pyplot as plt

#Insertion of all coulumns 
def make_table(dbase,data):
    columns = ', '.join(f"{key} TEXT" for key in data)
    dbase.execute(f"CREATE TABLE IF NOT EXISTS book_store ({columns})")
#for Insertion of one row
def insert_data_table(dbase,data):
    placeholders = ', '.join('?' for _ in data)
    tuple_data=[]
    for h in data:
        if type(h) ==list:
            tuple_data1=",".join(f"{key} "for key in h)
            tuple_data.append(tuple_data1)
        else:
            tuple_data.append(h)
    dbase.execute(f"INSERT INTO book_store VALUES ({placeholders})", tuple_data)

#database and api connections
dbase=sqlite3.connect("database.db")
r=requests.get("https://openlibrary.org/search.json?q=game+google")
data =r.json()
mdata=json.dumps(data,indent=4)


#addition of coulumns to the table "book_store"
dbase.execute("DROP TABLE IF EXISTS book_store")
print(f"you have these columns to access:\n Integer_type: edition_count,last_modified_i,ebook_count_i,_version_\n String_type: key, type, title, ebook_access\n List_type:author_name,etc...u can check it on =>data_format.txt")
input_columns = [x for x in input("What columns you want(seperated by space): ").split()]
make_table(dbase,input_columns)

#Creation of all rows
book_data=data["docs"]
i=0
for book_key in book_data:
    new_row=[]
    for column in input_columns:
        if column in book_key:
            new_row.append(book_key[column])
        else:
            new_row.append("Not found ")
    insert_data_table(dbase,new_row)


desire=input(f"do you want to find average(yes/no)  ")
if desire =="yes":
    value=input("for which coulumn, you want  average: ")
    if value in input_columns:
        average_query=f"SELECT AVG({value}) AS average_value FROM book_store"
        df=pd.read_sql_query(average_query,dbase)
        ans=df["average_value"][0]
        print(f"average value for {value} = {ans}")
    else:
        print(f"{value} is not present in columns")
elif desire=="no":
    exit
else:
    print(f"Invalid Input")





#Bar chart creation and showing
desire=input(f"do you want bar chart(yes/no) ")

if desire=="yes":
    category=input("for what coulumn you want bar chart: ")
    if category in input_columns:
        bar_query=f"SELECT {category},COUNT(*) AS count FROM book_store GROUP BY {category}"
        df=pd.read_sql_query(bar_query,dbase)
        plt.bar(df[category], df['count'])
        plt.xlabel(category)
        plt.ylabel('Count')
        plt.title(f"Bar Chart of {category}")
        plt.savefig("bar_chart.png")
        print(f"{category} Bar chart created")
        exit
    else:
        print(f"{category} is not present in columns")
elif desire=="no":
    exit
else:
    print(f"Invalid Input")

#table to csv 
table_query="SELECT * FROM book_store"
data=pd.read_sql(table_query,dbase)
data.to_csv("table3.csv",index=False)
dbase.close()