# 507-w20-final-project
This program aggregates crime data from https://spotcrime.com/mi/ann+arbor/daily and allows a user to select one or more crime types to see a graph of crime frequency by month. Data is displayed using HTML within a Flask App.

create_table.py is used to create tables in sql.
crawler.py crawls and scrapes data, preprocess the data and insert the data into the database.
display.py is used for data presentation.

First run create_table.py and crawler.py to create dabase.

Run display.py to lauch the web.
