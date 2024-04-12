import requests
import sqlite3
import json
import pandas as pd

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
r=requests.get("https://openlibrary.org/search.json?q=software")
data =r.json()
mdata=json.dumps(data,indent=4)


#addition of coulumns to the table "book_store"
dbase.execute("DROP TABLE IF EXISTS book_store")
input_columns = [x for x in input("What columns you want: ").split()]
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

#table to csv 
table_query="SELECT * FROM book_store"
data=pd.read_sql(table_query,dbase)
data.to_csv("table3.csv",index=False)