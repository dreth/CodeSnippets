# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 18:41:36 2019

@author: dreth
"""
import pandas as pd
import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ACEITEDEOLIVA\SQLEXPRESS;'
                      'Database=test1;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

listausuarios = pd.read_csv('listausuarios.csv')
listausuarios.FechaNacimiento = pd.to_datetime(listausuarios.FechaNacimiento)

for k in range(len(listausuarios)):
    command = 'insert into TUsuario (NombreUsuario,Email,FechaNacimiento) values ' + "('{0}','{1}','{2}')".format(listausuarios.loc[k,:][0],listausuarios.loc[k,:][1],listausuarios.loc[k,:][2])
    cursor.execute(command)
    conn.commit()