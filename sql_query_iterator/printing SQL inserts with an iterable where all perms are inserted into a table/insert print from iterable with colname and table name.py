# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 15:37:44 2019

@author: dreth
"""

#this would print inserts of all the iterations of the elements in a list given
from itertools import combinations as cb

def insert_iter(iterable,table_name,column_name):
    elemlist, all_elem = [], []
    for i in range(len(iterable)):
        elemlist.append(cb(iterable,i))
    for elem in elemlist:
        for comb in elem:
            all_elem.append(comb)
    del all_elem[0]
    all_elem = [list(tup) for tup in all_elem]
    data_to_insert = []
    for l in all_elem:
        days = str(l); days = days[1:len(days)-2].replace("'",'')
        data_to_insert.append('insert into {0} ({1}) values ("{2}")'.format(table_name,column_name,days))
    for k in data_to_insert:
        print(k)
    