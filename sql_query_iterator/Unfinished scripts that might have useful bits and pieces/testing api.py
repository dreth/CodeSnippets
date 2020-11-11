# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 08:10:31 2019

@author: dreth
"""
# importing requests to gather the data
import requests
import pyodbc
import pandas as pd

# using the newsapi.org API, thanks to newsapi.org for the ability to use their API.
apikey = ''


# Connecting to the SQL server database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ACEITEDEOLIVA\SQLEXPRESS;'
                      'Database=test1;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
#setting the categories for the news to populate the database with
categoria = ['math','syria','sports','economy','brexit', 'nuclear','microsoft','programming','music','mexico']

# prints inserts with a table name as string, colname and values as lists of elements for
# each column in the table
def inserts(table_name, colname, values,FK=True):
    
    # creates a string with all the columns between parenthesis separated by a comma
    columns = ' ('
    for i in colname:
        if i == colname[len(colname)-1]:
            columns = columns + i
        else:
            columns = columns + i + ','
    columns = columns + ')'
    
    # creates a string with all the values between parenthesis separated by a comma
    vals = ' ('
    for i in values:
        if i == None:
            if i == values[len(values)-1]:
                vals = vals + 'NULL'
            else:
                vals = vals + 'NULL' + ','
        else:
            if i == values[len(values)-1]:
                vals = vals + "'" + str(i).replace("'","''").replace('-','') + "'"
            else:
                vals = vals + "'" + str(i).replace("'","''").replace('-','') + "'" + ','
    vals = vals + ')'
    
    # prints the inserts
    command = 'insert into ' + table_name + columns + ' values ' + vals
    cursor.execute(command)
    conn.commit()
    

# utilizes inserts receiving dictionary as a parameter and the names of the tables to use
# the names of the tables should reference the model used in SQL
#
# table_names should be a list
# the first table name should be the column with the information for the article
# the second table name should be the table with the source information for the article
# it is a requirement that you have at least two tables
#   
# pk_name and fk_name are primary and foreign keys respectively, both should be strings
#
# it is amount of categories
def get_article_info(table_names,pk_name=None,fk_name=None,it=1):
    
    list_data = []
    for cat in categoria:
        
        url = ('https://newsapi.org/v2/everything?'
       'q={0}&'
       'language=en&'
       'apiKey={1}'.format(cat,apikey))
        
        response = requests.get(url)
        dictionary = response.json()
        list_data.append(dictionary)
    
    for d in list_data:
        # we make a list with the fields so we can use it as a parameter for the inserts function as colname
        fields = [x for x in d['articles'][0].keys()][1:]
        
        # we make a list with the fields of the source keys so we can use it as a parameter in the inserts function
        # as colname
        source_fields = [x for x in d['articles'][0]['source'].keys()]
        
        # we make a loop to iterate over the elements for the articles column in the specified dictionary
        # from the news API
        for i in d['articles']:
            
            # we make a list with the values of the element we're iterating over
            values = [x for x in list(i.values())][1:]
            
            # we make a list with the values of the source dictionary of the element we're iterating over
            source_values = [x for x in list(i['source'].values())]
    
            # we call the inserts function so we can print out all the inputs for SQL
            inserts(table_names[1],source_fields,source_values)
            inserts(table_names[0],fields,values)
            
    # adding the foreign keys on table 1 from table 2
    if fk_name != None:    
        for i in range(1,len(categoria)*20):
            command = 'update ' + table_names[0] + ' set {0} = {1}'.format(fk_name,i) + ' where ' + pk_name + '=' + str(i)
            cursor.execute(command)
            conn.commit()

# Poblando TCategoriaArticulo
for cat in categoria:
    command = 'insert into TCategoriaArticulo (CategoriaArticulo) values ' + "('{0}')".format(cat)
    cursor.execute(command)
    conn.commit()

# importando la lista de usuarios
listausuarios = pd.read_csv('listausuarios.csv')
listausuarios.FechaNacimiento = pd.to_datetime(listausuarios.FechaNacimiento)

for k in range(len(listausuarios)):
    command = 'insert into TUsuario (NombreUsuario,Email,FechaNacimiento) values ' + "('{0}','{1}','{2}')".format(listausuarios.loc[k,:][0],listausuarios.loc[k,:][1],listausuarios.loc[k,:][2])
    cursor.execute(command)
    conn.commit()