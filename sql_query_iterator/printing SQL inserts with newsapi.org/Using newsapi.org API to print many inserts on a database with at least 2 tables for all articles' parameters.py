# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 08:10:31 2019

@author: dreth
"""


# importing requests to gather the data
import requests

# using the newsapi.org API, thanks to newsapi.org for the ability to use their API.
apikey = '<INSERT YOUR API KEY HERE>'
url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey={0}'.format(apikey))

response = requests.get(url)
info = response.json()

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
                vals = vals + "'" + str(i).replace("'","''") + "'"
            else:
                vals = vals + "'" + str(i).replace("'","''") + "'" + ','
    vals = vals + ')'
    
    # prints the inserts
    print('insert into ' + table_name + columns + ' values ' + vals)
    

# utilizes inserts receiving dictionary as a parameter and the names of the tables to use
# the names of the tables should reference the model used in SQL
#
# the first table name should be the column with the information for the article
# the second table name should be the table with the source information for the article
# it is a requirement that you have at least two tables
def get_article_info(dictionary,table_names):
    
    # we make a list with the fields so we can use it as a parameter for the inserts function as colname
    fields = [x for x in dictionary['articles'][0].keys()][1:]
    
    # we make a list with the fields of the source keys so we can use it as a parameter in the inserts function
    # as colname
    source_fields = [x for x in dictionary['articles'][0]['source'].keys()]
    
    # we make a loop to iterate over the elements for the articles column in the specified dictionary
    # from the news API
    for i in dictionary['articles']:
        
        # we make a list with the values of the element we're iterating over
        values = [x for x in list(i.values())][1:]
        
        # we make a list with the values of the source dictionary of the element we're iterating over
        source_values = [x for x in list(i['source'].values())]

        # we call the inserts function so we can print out all the inputs for SQL
        inserts(table_names[1],source_fields,source_values)
        inserts(table_names[0],fields,values)
        
    
