# BOOK_API_MODEL
This is the Model that fetch Data from "https://openlibrary.org/search.json"
and then ask for query in "input_query">>>>if you having any issue just try "game ggoogle" at once.
you can extract  data  from whatever coulumn you want >>>>It will be shown in csv file after the execution. 
It create bar_chart for any column you want from entered at intial
1.There is a file data_format - It contains how data is stored in JSON format in this perticular API.
2.By running this main.py file -
    It will ask you about the coulumns you want to show in CSV file and also add data to the file database.db
    to check what columns you can access -Goto(data_format.txt)->and every atributes of data["docs"] you can access
    "Only space seprated arguments can pass through input process"
    after Entring all coulumns you want to have it will save table3.csv for your reference